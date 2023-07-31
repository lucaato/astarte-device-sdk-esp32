"""
Main generation script. Handles the generation of code for the project using this espressif component
"""
import argparse
import os
from pathlib import Path

from jinja2 import PackageLoader, Environment, FileSystemLoader
from astarte.device import Device
from astarte.interface import Interface

def load_interface(interface_file: Path) -> Interface:
	if not interface_file.is_file():
        raise InterfaceFileNotFoundError(f'"{interface_file}" does not exist or is not a file')

    try:
        with open(interface_file, "r", encoding="utf-8") as interface_fp:
            return Interface(json.load(interface_fp))
    except json.JSONDecodeError as exc:
        raise InterfaceFileDecodeError(
            f'"{interface_file}" is not a parsable json file'
        ) from exc

def load_interfaces(dir: Path) -> list[Interface]:
	interfaces = []

    if not dir.exists():
        raise InterfaceFileNotFoundError(f'"{interfaces_dir}" does not exist')
    if not dir.is_dir():
        raise InterfaceFileNotFoundError(f'"{interfaces_dir}" is not a directory')

	for interface_file in [i for i in dir.iterdir() if i.suffix == ".json"]:
		interfaces.append(load_interface(interface_file))

	return interfaces

def main(args: dict):
	env = Environment(loader = FileSystemLoader(os.path.abspath(".")))
	template = env.get_template("interfaces.c.j2")

	interface_dir = os.path.abspath(args.interface_dir)

    if not interfaces_dir.exists():
        raise InterfaceFileNotFoundError(f'"{interfaces_dir}" does not exist')
    if not interfaces_dir.is_dir():
        raise InterfaceFileNotFoundError(f'"{interfaces_dir}" is not a directory')
 
	generated = template.render(load_interfaces(interface_dir))

	print(generated)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--interface_dir',
        type=str,
		required=True,
        help='The directory where the interfaces json descriptors are stored.')

    args = parser.parse_args()

    main(args)
