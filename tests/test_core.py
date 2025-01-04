import os
import tempfile

from flatten.core import flatten_folder


def test_flatten_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Hello world")

        result = flatten_folder(tmpdir)
        assert "test.txt" in result
        assert "Hello world" in result


def test_flatten_ignore():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.txt")
        secret = "This is secret"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(secret)

        file_path = os.path.join(tmpdir, "test.md")
        not_secret = "Cool!"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(not_secret)

        # Pass an additional ignore for *.txt
        result = flatten_folder(tmpdir, ignores=["*.txt"])
        assert secret not in result
        assert "test.txt" not in result

        assert not_secret in result
        assert "test.md" in result


def test_ignore_git_and_env():
    """
    Ensures .git/ and .env file are ignored by default
    due to ignoring all dotfiles and dotdirs.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .git dir
        git_dir = os.path.join(tmpdir, ".git")
        os.mkdir(git_dir)
        git_test_file = os.path.join(git_dir, "somefile")
        with open(git_test_file, "w", encoding="utf-8") as f:
            f.write("this should be ignored")

        # Create .env file
        env_file = os.path.join(tmpdir, ".env")
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("should also be ignored")

        # Create a normal file
        normal_file = os.path.join(tmpdir, "hello.txt")
        with open(normal_file, "w", encoding="utf-8") as f:
            f.write("should appear in flatten output")

        result = flatten_folder(tmpdir)
        assert "this should be ignored" not in result
        assert "should also be ignored" not in result
        assert "hello.txt\n---\nshould appear in flatten output" in result


def test_ignore_tests_folder():
    """
    Ensures that if we pass `tests/` as an ignore pattern,
    any 'tests' folder and its contents are excluded.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create tests folder
        tests_dir = os.path.join(tmpdir, "tests")
        os.mkdir(tests_dir)
        test_file = os.path.join(tests_dir, "test1.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("this is in tests folder")

        # Create a normal file
        normal_file = os.path.join(tmpdir, "keepme.txt")
        with open(normal_file, "w", encoding="utf-8") as f:
            f.write("keep me")

        result = flatten_folder(tmpdir, ignores=["tests/"])
        # Confirm tests folder is ignored
        assert "this is in tests folder" not in result
        assert "tests/test1.txt" not in result
        # Confirm keepme is present
        assert "keepme.txt\n---\nkeep me" in result
