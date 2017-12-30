#!/usr/bin/env python

import os
import sys
import argparse

__version__ = '0.1.0'

def parse_arguments():
    parser = argparse.ArgumentParser(description='ESP32 firmware tool')
    cwd = os.getcwd()
    default_output_dir = os.path.join(cwd, 'firmware')
    default_output_filename = 'firmware.bin'

    parser.add_argument('-a', '--use-arduino', action='store_true', dest='use_arduino', default=False, help='Use Arduino for ESP32 as component')
    parser.add_argument('-n', '--arduino-directory-name', action='store', dest='arduino_directory_name', default='arduino-esp32', help='Directory name of Arduino component')
    parser.add_argument('--output-dir', action='store', dest='firmware_output_dir', default=default_output_dir, help='Output directory')
    parser.add_argument('--output-filename', action='store', dest='firmware_output_filename', default=default_output_filename, help='Output filename')
    parser.add_argument('project_directory', action='store', default=cwd, help='ESP32 project directory')

    return parser.parse_args()

def find_partition_binary(project_dir):
    sdkconfig_file = open(os.path.join(project_dir, 'sdkconfig'))

    for line in sdkconfig_file.readlines():
        if line.startswith('CONFIG_PARTITION_TABLE_FILENAME'):
            key, value = line.strip().split('=')
            value = value.replace('\"', '')

            return value.split('.')[0]

    return None


def get_arduino_ingredients(project_name, project_dir, arduino_component):
    return [
        (os.path.join(project_dir, 'build/bootloader/bootloader.bin'), 0x1000),
        (os.path.join(project_dir, 'build/default.bin'), 0x8000),
        (os.path.join(project_dir, 'components/%s/tools/partitions/boot_app0.bin' % (arduino_component)), 0xe000),
        (os.path.join(project_dir, 'build/%s.bin' % project_name), 0x10000),
    ]

def get_idf_only_ingredients(project_name, project_dir):
    partition_binary_file = find_partition_binary(project_dir)
    if partition_binary_file is None:
        return []

    return [
        (os.path.join(project_dir, 'build/bootloader/bootloader.bin'), 0x1000),
        (os.path.join(project_dir, 'build/%s.bin' % partition_binary_file), 0x8000),
        (os.path.join(project_dir, 'build/%s.bin' % project_name), 0x10000),
    ]

def main():
    parse_result = parse_arguments()

    project_dir = os.getcwd() if parse_result.project_directory == '.' else parse_result.project_directory
    project_name = os.path.basename(project_dir)

    firmware_ingredients = []
    if parse_result.use_arduino:
        firmware_ingredients = get_arduino_ingredients(project_name, project_dir, parse_result.arduino_directory_name)
    else:
        firmware_ingredients = get_idf_only_ingredients(project_name, project_dir)

    if len(firmware_ingredients) < 1:
        sys.exit(-1)

    firmware_directory = parse_result.firmware_output_dir
    firmware_out_file = os.path.join(firmware_directory, parse_result.firmware_output_filename)

    if not os.path.isdir(firmware_directory):
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
            print('%s - %d' % (bin_path, bin_offset))

if __name__ == '__main__':
    main()
