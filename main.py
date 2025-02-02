import argparse
import datetime
import os
import shutil


def main():
    parser = argparse.ArgumentParser(
        prog="YGOLOTD-Buy-Any-Pack",
        description="""Patch the "Yu-Gi-Oh! Legacy of the Duelist: Link
        Evolution" game executable start the game with all cards available""",
    )
    parser.add_argument("filepath", help="Path to the executable file to patch/unpatch")
    args = parser.parse_args()
    patch_executable(parser, os.path.abspath(args.filepath))


def patch_executable(
    parser: argparse.ArgumentParser, executable_path: str
) -> None:
    backup_path = (
         f"{executable_path}.bak_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    shutil.copy2(executable_path, backup_path)
    print(f"Backup created at {backup_path}")

    patches = [
        (
            0x754B04,
            b"\x0f\x1f\x40\x00\x0f\x1f\x84\x00\x00\x00\x00\x00",
            b"\x66\xe9\x28\x00\x00\x00\xcc\xcc\xcc\xcc\xcc\xcc",
        ),
        (
            0x754B2F,
            b"\xe0\xc3\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc",
            b"\xd4\xc3\xcc\x4c\x8d\xa3\xc8\x5d\x00\x00\xe9\xa8\x05\x00\x00",
        ),
        (
            0x7550E6,
            b"\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc",
            b"\x4d\x39\xe2\xe9\xe4\x00\x00\x00",
        ),
        (
            0x7551D2,
            b"\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc",
            b"\x0f\x82\x38\xf9\xff\xff\xeb\x48",
        ),
        (
            0x755222,
            b"\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc",
            b"\x41\xc6\x02\x0b\xe9\xe5\xf8\xff\xff",
        ),
    ]

    try:
        with open(executable_path, "r+b") as f:
            for offset, original, patched in patches:
                f.seek(offset)
                current_value = f.read(len(original))
                if current_value != original:
                    raise ValueError(
                        f"Unexpected value at offset {hex(offset)}: "
                        f"{current_value.hex()}. The file is either already patched or "
                        "is incompatible"
                    )
                f.seek(offset)
                f.write(patched)
        print("Patching completed successfully.")
    except Exception as e:
        shutil.copy2(backup_path, executable_path)
        parser.error(f"Failed to patch the executable: {e}")


if __name__ == "__main__":
    main()
