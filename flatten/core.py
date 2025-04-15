import os

from pathspec import PathSpec


def flatten_folder(folder_path, ignores=None, include_stats=False):
    """Flattens a folder's contents and returns a formatted string
    ignoring `ignores` and .gitignore files.

    Args:
        folder_path (str): Root folder to flatten.
        ignores (list[str]): Optional list of patterns to ignore.
        include_stats (bool): If True, return file statistics along with flattened content.

    Returns:
        If include_stats is False: The flattened string of all non-ignored files.
        If include_stats is True: A tuple of (flattened_string, file_stats_dict) where
                                  file_stats_dict maps file paths to token counts.
    """
    base_patterns = ignores or []
    base_pathspec = PathSpec.from_lines("gitwildmatch", base_patterns)
    flat = _walk_and_flatten(folder_path, base_pathspec)

    flattened_str = "\n".join(
        f"{os.path.relpath(path, folder_path)}\n```\n{content}\n```\n"
        for path, content in flat.items()
    )

    if include_stats:
        # Create a dictionary mapping relative file paths to token counts
        file_stats = {
            os.path.relpath(path, folder_path): len(content.encode('utf-8')) // 10
            for path, content in flat.items()
        }
        return flattened_str, file_stats

    return flattened_str, {}


def _walk_and_flatten(path, parent_pathspec):
    local_pathspec = parent_pathspec
    local_gitignore = os.path.join(path, ".gitignore")
    if os.path.isfile(local_gitignore):
        with open(local_gitignore, "r", encoding="utf-8") as f:
            local_pathspec += PathSpec.from_lines("gitwildmatch", f)

    results = {}
    for item in os.listdir(path):
        if item.startswith("."):
            continue

        abs_item_path = os.path.join(path, item)
        if local_pathspec.match_file(abs_item_path):
            continue

        if os.path.isdir(abs_item_path):
            results.update(_walk_and_flatten(abs_item_path, local_pathspec))
        else:
            content = _read_file_or_binary_placeholder(abs_item_path)
            results[abs_item_path] = content

    return results


def _read_file_or_binary_placeholder(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return "<binary or unreadable file>"
