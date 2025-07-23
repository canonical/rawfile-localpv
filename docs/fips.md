# Rawfile LocalPV FIPS compliance analysis

The following document summarizes the current state of [FIPS 140-3] compliance for Rawfile LocalPV, focusing on its cryptographic components and build requirements. This overview is intended to guide users and developers in understanding the compliance status and necessary steps for achieving FIPS mode operation.

> **Note:** As of now, pebble is not built in a FIPS-compliant way. This document will be updated once it is.
## Abbreviations

This document uses a set of abbreviations which are explained below:

- **Federal Information Processing Standards (FIPS)**: A set of standards for cryptographic modules published by the U.S. government.
- **Transport Layer Security (TLS)**: A cryptographic protocol designed to provide secure communication over a computer network.
- **Advanced Package Tool (APT)**: A package management system used by Debian-based Linux distributions.

## FIPS Compliance Status

Python links to the system OpenSSL by default. On a FIPS host, this will automatically be FIPS compliant. The following requirements must be met:

1. **OpenSSL**: Must link against a FIPS-validated OpenSSL implementation, e.g. from `core22/fips`.
2. **Build Environment**: Must be built on an Ubuntu Pro machine with FIPS updates enabled, see below.

### Required Build Modifications

To build Rawfile LocalPV in FIPS-compliant mode:

1. **Prerequisites**:
   - Ubuntu Pro enabled machine
   - FIPS updates enabled (`sudo pro enable fips-updates`)
   - rockcraft on `edge/pro-sources` channel, see [this discourse post]

2. **Build Command**:

   ```bash
   sudo rockcraft pack --pro=fips-updates
   ```

<!-- LINKS -->

[FIPS 140-3]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.140-3.pdf
[Go toolchain from Microsoft]: https://github.com/microsoft/go/blob/microsoft/release-branch.go1.23/eng/doc/fips/README.md
[this discourse post]: https://discourse.ubuntu.com/t/build-rocks-with-ubuntu-pro-services/57578
