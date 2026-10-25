# Feetech-Servo-SDK [![Platforms](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white) [![Language](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) [![IDE](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white) [![adam package](https://img.shields.io/badge/adam_package-red?style=for-the-badge&logo=python&logoColor=white)](https://github.com/Adam-Software)

## Fork release and automated tests

This fork starts at upstream tag `v.1.0.0` and validates response lengths before
returning register data. Related upstream report:
https://github.com/Adam-Software/Feetech-Servo-SDK/issues/5

With the SDK's PySerial dependency installed, run the hardware-free tests:

```sh
python -m unittest discover -s tests -v
```

The tests use synthetic serial bytes with the real checksum parser. They do not
open a serial device or command motors. Valid high-temperature readings are
preserved. Length checks cannot identify stale replies of the same size.

Fork wheels use a distinct local version, currently `1.0.0+johnmu.1`. Releases
retain the wheel, source commit, and SHA-256. Rebuild from the exact tagged source
in an isolated environment with `setuptools==81.0.0`, `wheel==0.45.1`, and
`pyserial==3.5`:

```sh
python - <<'PY'
import os
import subprocess
import sys
epoch = subprocess.check_output(
    ['git', 'show', '-s', '--format=%ct', 'HEAD'], text=True).strip()
subprocess.run([sys.executable, 'setup.py', 'bdist_wheel'],
               env=dict(os.environ, SOURCE_DATE_EPOCH=epoch), check=True)
PY
```

Consumers should pin the release wheel URL and SHA-256 rather than an unversioned
branch. Installation and packet tests do not qualify physical thermal behavior.


[![License](https://img.shields.io/github/license/Adam-Software/Feetech-Servo-SDK.svg)](https://img.shields.io/github/license/Adam-Software/Feetech-Servo-SDK.svg)
[![PyPI version](https://badge.fury.io/py/feetech-servo-sdk.svg)](https://badge.fury.io/py/feetech-servo-sdk) 


This is source code from [official feetech repository](https://gitee.com/ftservo/SCServoSDK).
The repository structure copies the structure of the [original library](https://gitee.com/ftservo/SCServoSDK/blob/e4d07f43c4c34827b2e226cf5cc706576504ebeb/SCServo_Python_200831.7z)

## Structure

```
root dirrectory
     |---scservo_sdk 
     |---scsservo_sdk_example
```
The `scsservo_sdk_example` directories contain examples of using the library.

The source code of the library is located in the `scservo_sdk` directory.

The `scsservo_sdk_source` directory contains the original archive with the source code of the library from the developer.

## Usage

Tested on `Linux raspberrypi 5.15.61-v8+ #1579 SMP PREEMPT Fri Aug 26 11:16:44 BST 2022 aarch64`.
Python version `Python 3.9.2`.

### Method 1. Clone repositry

```
$ cd /usr/src/
$ sudo git clone https://github.com/Adam-Software/Feetech-Servo-SDK.git
$ sudo chown -R pi Feetech-Servo-SDK
$ cd Feetech-Servo-SDK/scsservo_sdk_example
$ python3 ping.py
Succeeded to open the port
Succeeded to change the baudrate
[ID:001] ping Succeeded. SCServo model number : 1540
```

### Method 2. Install pip package

Copy the sample file to any location convenient for you. In the example I use `/home/pi/FeetechTestFiles`

```
$ pip install feetech-servo-sdk
$ cd /home/pi/FeetechTestFiles
$ python3 ping.py
Succeeded to open the port
Succeeded to change the baudrate
[ID:001] ping Succeeded. SCServo model number : 1540
```
