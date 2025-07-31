# Rawfile LocalPV FIPS compliance analysis

The following document summarizes the current state of [FIPS 140-3] compliance for Rawfile LocalPV, focusing on its cryptographic components and build requirements. This overview is intended to guide users and developers in understanding the compliance status and necessary steps for achieving FIPS mode operation.

> **Note:** As of now, pebble is not built in a FIPS-compliant way. This document will be updated once it is.
## Abbreviations

This document uses a set of abbreviations which are explained below:

- **Federal Information Processing Standards (FIPS)**: A set of standards for cryptographic modules published by the U.S. government.

## FIPS Compliance Status

Python links to the system OpenSSL by default. On a FIPS-enabled host, algorithms that use the OpenSSL implementation will be FIPS compliant. However, Python contains builtin
hashing algorithms that are not FIPS compliant (e.g. MD5). Building Python with `--wihout-builtin-hashlib-hashes` will remove these non-FIPS compliant algorithms.
Rawfile LocalPV does not use any of these non-FIPS compliant algorithms, so it is FIPS compliant.

In order to confirm Python is referencing the system OpenSSL, you can run the following command:

```bash
python3 -c 'import _ssl; print(_ssl.__file__)'
```

You will see something like `/usr/lib/python3.13/lib-dynload/_ssl.cpython-313-x86_64-linux-gnu.so`. Run `ldd` and look for `libssl.so` and `libcrypto.so`:

```bash
ldd /usr/lib/python3.13/lib-dynload/_ssl.cpython-313-x86_64-linux-gnu.so | grep -E 'libssl|libcrypto'
```

You should see something like:

```
libssl.so.3 => /lib/x86_64-linux-gnu/libssl.so.3 (0x000075b68a51f000)
libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x000075b689e00000)
```

If that's not the case, you need to ensure the Python that's going to run this ROCK, 
is either built with a FIPS-compliant OpenSSL, or is referencing the host's OpenSSL.

### Future work

* Using a custom Python build without the builtin hashes, and possibly linked to a static FIPS-compliant OpenSSL. 

### Required Build Modifications

To build Rawfile LocalPV in FIPS-compliant mode:

1. **Prerequisites**:
   - Ubuntu Pro enabled machine
   - rockcraft on `edge/pro-sources` channel, see [this discourse post]

2. **Build Command**:

   ```bash
   sudo rockcraft pack --pro=fips-updates
   ```

<!-- LINKS -->

[FIPS 140-3]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.140-3.pdf
[this discourse post]: https://discourse.ubuntu.com/t/build-rocks-with-ubuntu-pro-services/57578
