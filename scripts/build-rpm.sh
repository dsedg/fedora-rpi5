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

if [[ ! "${commit}" =~ ^[[:xdigit:]]{40}$ ]]; then
    printf 'KERNEL_COMMIT must be a 40-character hexadecimal commit.\n' >&2
    exit 1
fi

if [[ ! "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    printf 'KERNEL_VERSION must have the form major.minor.patch.\n' >&2
    exit 1
fi

source_archive="${source_dir}/${commit}.tar.gz"
source_url="https://github.com/raspberrypi/linux/archive/${commit}.tar.gz"

if [[ "$(uname -m)" != "aarch64" ]]; then
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

if [[ ! -s "${source_archive}" ]]; then
    curl --fail --location --retry 3 "${source_url}" --output "${source_archive}"
fi

rpmbuild \
    --define "_topdir ${topdir}" \
    --define "kernel_commit ${commit}" \
    --define "kernel_version ${version}" \
    -ba "${spec_file}"
