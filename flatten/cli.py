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
    parser.add_argument(
        "--top-tokens",
        action="store_true",
        help="Print the top 10 files by approximate token count",
    )
    args = parser.parse_args()

    # Convert comma-separated ignore patterns into a list
    additional_ignores = []
    if args.ignore:
        additional_ignores = [
            pat.strip() for pat in args.ignore.split(",") if pat.strip()
        ]

    # Run flatten_folder with stats if top-tokens is requested
    if args.top_tokens:
        flattened_str, file_stats = flatten_folder(
            folder_path=args.folder, 
            ignores=additional_ignores,
            include_stats=True
        )
    else:
        flattened_str = flatten_folder(
            folder_path=args.folder, 
            ignores=additional_ignores
        )
    
    total_words = len(flattened_str.split())

    # Print top 10 files by token count if requested
    if args.top_tokens:
        print("\nTop 10 files by token count:")
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (file_path, token_count) in enumerate(sorted_files, 1):
            print(f"{i}. {file_path}: {token_count} tokens")
        print()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(flattened_str)
        print(f"{total_words} words saved.")
    else:
        pyperclip.copy(flattened_str)
        print(f"Copied to clipboard ({total_words} words).")
