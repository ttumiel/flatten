import argparse

import pyperclip

from flatten.core import flatten_folder


def main():
    parser = argparse.ArgumentParser(
        description="Flatten a folder's contents into one string, ignoring .gitignore and user-provided patterns."
    )
    parser.add_argument("folder", type=str, help="Path to the folder to flatten")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (if not provided, copies to clipboard)",
    )
    parser.add_argument(
        "--ignore",
        type=str,
        default=None,
        help="Comma-separated list of additional ignore patterns (e.g. '*.log,secret/*')",
    )
    args = parser.parse_args()

    # Convert comma-separated ignore patterns into a list
    additional_ignores = []
    if args.ignore:
        additional_ignores = [
            pat.strip() for pat in args.ignore.split(",") if pat.strip()
        ]

    # Run flatten_folder
    flattened_str = flatten_folder(folder_path=args.folder, ignores=additional_ignores)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(flattened_str)
    else:
        pyperclip.copy(flattened_str)
        print("Copied to clipboard.")
