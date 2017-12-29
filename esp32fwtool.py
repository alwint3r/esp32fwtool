#!/usr/bin/env python

import os

def main():
    base_dir = os.getcwd()
    project_name = os.path.basename(base_dir)

    # let's assume that build directory is exist
    # also assume that the project is using arduin as one of the components
    boot_app0_path = os.path.join(base_dir, 'components/arduino-esp32/tools/partitions/boot_app0.bin')
    bootloader_path = os.path.join(base_dir, 'build/bootloader/bootloader.bin')
    app_path = os.path.join(base_dir, 'build/%s.bin' % (project_name))
    default_path = os.path.join(base_dir, 'build/default.bin')

    boot_app0_offset = 0xe000
    bootloader_offset = 0x1000
    app_offset = 0x10000
    default_offset = 0x8000

    firmware_ingredients = [
        (bootloader_path, bootloader_offset),
        (default_path, default_offset),
        (boot_app0_path, boot_app0_offset),
        (app_path, app_offset),
    ]

    firmware_directory = os.path.join(base_dir, 'esp32fw')
    firmware_out_file = os.path.join(firmware_directory, 'firmware.bin')

    os.mkdir(firmware_directory)

    current_offset = 0x1000
    with open(firmware_out_file, 'wb') as fout:
        for bin_path, bin_offset in firmware_ingredients:
            assert bin_offset >= current_offset
            fout.write(b'\xff' * (bin_offset - current_offset))
            current_offset = bin_offset

            with open(bin_path, 'rb') as fin:
                data = fin.read()
                fout.write(data)
                current_offset += len(data)
            print("%s - %d" % (bin_path, bin_offset))

if __name__ == "__main__":
    main()
