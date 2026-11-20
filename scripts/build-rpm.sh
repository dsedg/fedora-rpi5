#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
spec_file="${repo_dir}/SPECS/kernel-rpi5.spec"
topdir="${repo_dir}/rpmbuild"
source_dir="${topdir}/SOURCES"
default_commit="$(grep -F '%{!?kernel_commit:%global kernel_commit ' "${spec_file}" \
    | sed 's/^.*kernel_commit //; s/}$//')"
default_version="$(grep -F '%{!?kernel_version:%global kernel_version ' "${spec_file}" \
    | sed 's/^.*kernel_version //; s/}$//')"
commit="${KERNEL_COMMIT:-${default_commit}}"
version="${KERNEL_VERSION:-${default_version}}"
flavor="${KERNEL_FLAVOR:-standard}"

if [[ ! "${commit}" =~ ^[[:xdigit:]]{40}$ ]]; then
    printf 'KERNEL_COMMIT must be a 40-character hexadecimal commit.\n' >&2
    exit 1
fi

if [[ "${flavor}" != "standard" && "${flavor}" != "bigscreen" ]]; then
    printf 'KERNEL_FLAVOR must be standard or bigscreen.\n' >&2
    exit 1
fi

if [[ "${flavor}" == "bigscreen" && ! "${version}" =~ ^7\.3\.[0-9]+$ ]]; then
    printf 'The Bigscreen kernel variant is only supported on rpi-7.3.y.\n' >&2
    exit 1
fi

if [[ ! "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    printf 'KERNEL_VERSION must have the form major.minor.patch.\n' >&2
    exit 1
fi

source_archive="${source_dir}/${commit}.tar.gz"
source_url="https://github.com/raspberrypi/linux/archive/${commit}.tar.gz"
srpm_only="${BUILD_SRPM_ONLY:-false}"

if [[ "${srpm_only}" != "true" && "${srpm_only}" != "false" ]]; then
    printf 'BUILD_SRPM_ONLY must be true or false.\n' >&2
    exit 1
fi

if [[ "${srpm_only}" == "true" && -z "${COPR_SRPM_OUTDIR:-}" ]]; then
    printf 'COPR_SRPM_OUTDIR is required when BUILD_SRPM_ONLY=true.\n' >&2
    exit 1
fi

if [[ "${srpm_only}" != "true" && "$(uname -m)" != "aarch64" ]]; then
    printf 'Build on an aarch64 Fedora host; found %s.\n' "$(uname -m)" >&2
    exit 1
fi

for tool in curl rpmbuild; do
    if ! command -v "${tool}" >/dev/null 2>&1; then
        printf 'Required build tool not found: %s\n' "${tool}" >&2
        exit 1
    fi
done

mkdir -p "${source_dir}" \
    "${topdir}/BUILD" \
    "${topdir}/BUILDROOT" \
    "${topdir}/RPMS" \
    "${topdir}/SPECS" \
    "${topdir}/SRPMS"

cp "${repo_dir}/SOURCES/kernel-aarch64-fedora.config" "${source_dir}/"
cp "${repo_dir}/SOURCES/kernel-rpi5.config" "${source_dir}/"
cp "${repo_dir}/SOURCES/kernel-rpi5-host-uapi-types.h" "${source_dir}/"
cp "${repo_dir}/SOURCES/kernel-rpi5-bigscreen.config" "${source_dir}/"

if [[ ! -s "${source_archive}" ]]; then
    curl --fail --location --retry 3 "${source_url}" --output "${source_archive}"
fi

build_mode=-ba
build_spec="${spec_file}"
if [[ "${srpm_only}" == "true" ]]; then
    build_mode=-bs
    build_spec="${topdir}/SPECS/kernel-rpi5.spec"
    python3 - "${spec_file}" "${build_spec}" "${commit}" "${version}" <<'PY'
import sys
from pathlib import Path

source, destination, commit, version = sys.argv[1:]
lines = Path(source).read_text().splitlines()
for name, value in (("kernel_commit", commit), ("kernel_version", version)):
    prefix = f"%{{!?{name}:%global {name} "
    matches = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1 or not lines[matches[0]].endswith("}"):
        raise SystemExit(f"Expected exactly one {name} default in {source}")
    lines[matches[0]] = f"%global {name} {value}"

Path(destination).write_text("\n".join(lines) + "\n")
PY
fi

rpmbuild \
    --define "_topdir ${topdir}" \
    --define "kernel_commit ${commit}" \
    --define "kernel_version ${version}" \
    --define "kernel_flavor ${flavor}" \
    "${build_mode}" \
    "${build_spec}"

if [[ "${srpm_only}" == "true" ]]; then
    rpm_name=kernel
    if [[ "${flavor}" == "bigscreen" ]]; then
        rpm_name=kernel-rpi5-bigscreen
    fi
    mapfile -t srpms < <(
        find "${topdir}/SRPMS" -maxdepth 1 -type f \
            -name "${rpm_name}-${version}-*.src.rpm" -print | sort
    )
    if [[ "${#srpms[@]}" -ne 1 ]]; then
        printf 'Expected exactly one source RPM for %s (%s); found %s.\n' \
            "${version}" "${rpm_name}" "${#srpms[@]}" >&2
        exit 1
    fi

    mkdir -p "${COPR_SRPM_OUTDIR}"
    cp "${srpms[0]}" "${COPR_SRPM_OUTDIR}/"
fi
