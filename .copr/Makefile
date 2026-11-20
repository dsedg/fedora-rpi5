SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

.PHONY: srpm
srpm:
	@case "$(notdir $(spec))" in \
		kernel-rpi5-6.18.spec) branch="rpi-6.18.y" ;; \
		kernel-rpi5-7.3.spec) branch="rpi-7.3.y" ;; \
		*) echo "Unsupported COPR spec selector: $(spec)" >&2; exit 1 ;; \
	esac; \
	dnf install -y curl python3 rpm-build; \
	COPR_SRPM_OUTDIR="$(outdir)" ./scripts/build-copr-srpm.sh "$$branch"
