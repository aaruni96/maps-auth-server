# Testing MaPS Upload

This document provides a short guide on how to "field test" the upload functionality of MaPS.

## Before you start

Check the following:

- Make sure you are on Linux 5.11+
- Make sure that your version of bubblewrap is up to date (stored in
  `$HOME/.var/org.maps.mardi/deps`). Latest version will be downloaded and compiled automaticaly if
  bubblewrap is not found, but will not be auto updated if an older build is found.
- Clone `https://github.com/aaruni96/maps`, and checkout `ak96/upload`.
- `libostree-dev`, `libgirepository1.0-dev`, and `libcairo2-dev` (or equivalents) need to be
  installed using your system's package manager.
- Set up a python virtual environment, and install python pre requisites :
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade -r requirements.txt
  ```
- Export environment variables `XDG_DATA_HOME` and `HOME` to a filesystem which supports extended
  attributes, if needed.
- Export environment variable `MAPS_UPLOAD_SERVER` and `MTDAUTH` to values shared to you privately.

## Upload Process

### Make and upload a runtime

We only allow uploading runtimes you have freshly created. Therefore, you need to make a runtime
before you can upload.

```bash
# set up a minimal runtime tree
mkdir ostree
maps package --initialise ostree/new-runtime
# commit runtime to maps
maps package --commit ostree/new-runtime test-runtime-for-upload-testing
# upload runtime
maps package --upload test-runtime-for-upload-testing
```
