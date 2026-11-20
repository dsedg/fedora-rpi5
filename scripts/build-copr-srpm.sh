#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
branch="${1:-}"

case "${branch}" in
    rpi-6.18.y) flavor=standard ;;
    rpi-7.3.y) flavor=bigscreen ;;
    *)
        printf 'Unsupported Raspberry Pi kernel branch: %s\n' "${branch}" >&2
        exit 1
        ;;
esac

if [[ -z "${COPR_SRPM_OUTDIR:-}" ]]; then
    printf 'COPR_SRPM_OUTDIR is required.\n' >&2
    exit 1
fi

read -r commit version < <(
    python3 - "${repo_dir}/SOURCES/kernel-branch-pins.json" "${branch}" <<'PY'
import json
import re
import sys
from pathlib import Path

pins = json.loads(Path(sys.argv[1]).read_text())
pin = pins.get(sys.argv[2])
if not isinstance(pin, dict):
    raise SystemExit(f"Missing kernel pin for {sys.argv[2]}")

commit = pin.get("commit", "")
version = pin.get("version", "")
if not re.fullmatch(r"[0-9a-f]{40}", commit):
    raise SystemExit(f"Invalid commit pin for {sys.argv[2]}")
if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
    raise SystemExit(f"Invalid kernel version for {sys.argv[2]}")

print(commit, version)
PY
)

cd "${repo_dir}"
BUILD_SRPM_ONLY=true \
KERNEL_COMMIT="${commit}" \
KERNEL_VERSION="${version}" \
KERNEL_FLAVOR="${flavor}" \
COPR_SRPM_OUTDIR="${COPR_SRPM_OUTDIR}" \
    ./scripts/build-rpm.sh
