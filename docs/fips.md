# Rawfile LocalPV FIPS compliance analysis

The following document summarizes the current state of [FIPS 140-3] compliance for Rawfile LocalPV, focusing on its cryptographic components and build requirements. This overview is intended to guide users and developers in understanding the compliance status and necessary steps for achieving FIPS mode operation.

> **Note:** As of now, pebble is not built in a FIPS-compliant way. This document will be updated once it is.

## Abbreviations

This document uses a set of abbreviations which are explained below:

- **Federal Information Processing Standards (FIPS)**: A set of standards for cryptographic modules published by the U.S. government.

## FIPS Compliance Status

Python by default links to the OpenSSL of the environment in which it's running (e.g. a ROCK). In a FIPS-enabled environment, 
algorithms that use the OpenSSL implementation will be FIPS compliant. However, Python contains built-in
hashing algorithms that are not FIPS compliant (e.g. MD5). Building Python with `--wihout-builtin-hashlib-hashes` will remove these non-FIPS compliant algorithms.
Rawfile LocalPV does not use any of these built-in and non-FIPS compliant algorithms, and the ROCK is shipped with a FIPS-compliant OpenSSL,
so it is FIPS-compliant.

In order to confirm Python is referencing the host's OpenSSL, you can run the following command:

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

**NOTE**: This ROCK is bundled with a FIPS-validated OpenSSL library which is 
described in the ROCK manifest (see [this discourse post]).
```yaml
...
parts:
  openssl:
    plugin: nil
    stage-packages:
      - openssl-fips-module-3
      - openssl
...
```

### Required Build Modifications

To build Rawfile LocalPV in FIPS-compliant mode:

**Prerequisites**:

- a `rockcraft` version that allows building with Ubuntu Pro services (refer to [this discourse post]).

**Building the Image**:

Use the following command to build the image:

```bash
sudo rockcraft pack --pro=fips-updates
```

### Future work

* Using a custom Python build without the built-in hashes, and possibly linked to a static FIPS-compliant OpenSSL. 

<!-- LINKS -->

[FIPS 140-3]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.140-3.pdf
[this discourse post]: https://discourse.ubuntu.com/t/build-rocks-with-ubuntu-pro-services/57578
