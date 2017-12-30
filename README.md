ESP32 Firmware Tool
===================

Tool for dealing with ESP32 firmware binary. Only support projects built with ESP IoT Development Framework.


## Features

* Combining firmware binaries into single binary file.

## Supported OS

* GNU/Linux Ubuntu

## Supported Python Version

Currently, only Python v2 is supported. I plan to add the support for both v3 and v2.

## How to Use

For complete usage information, run the command below:

```
esp32fwtool.py --help
```

**Combining binary files**

* Generating binary file from an ESP-IDF only (without Arduino) project

```
esp32fwtool.py .
```

or

```
esp32fwtol.py /path/to/espidf/project
```

* Generating binary file from an ESP-IDF + Arduino as component project.

```
esp32fwtool.py -a -n "arduino-esp32" . 
```

or 

```
esp32fwtool.py --use-arduino --arduino-directory-name "arduino-esp32" .
```

Where `arduino-esp32` is the default name for the arduino for esp32 directory inside `components` directory. If you use different name for the arduino directory then you must change the command line argument as well.

By default, the tool will generate a binary file called `firmware.bin` inside `firmware` directory inside the current working directory.

If you want to change the output directory and output filename, then you must provide an arguments to `--output-dir` and `--output-filename` respectively.
