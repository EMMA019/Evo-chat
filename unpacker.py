# unpacker.py V2.0 (Improved Security & Performance)
import re
import os
import sys

def unpack_project(markdown_file_path: str):
    print(f"--- Evo Unpacker v2.0 ---")
    print(f"Reading: {markdown_file_path}\n")

    try:
        with open(markdown_file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ [Error] Cannot read file: {e}", file=sys.stderr)
        return

    # File header pattern
    HEADER_PATTERN = re.compile(
        r"^(?:# === FILENAME:|### file:|# --- FILENAME:|# FILENAME:)\s*(.*?)\s*$",
        re.MULTILINE | re.IGNORECASE
    )

    CLEAN_DELIMITER = "\n---EVO-FILE-START---\n"

    def replace_header(match):
        filename = match.group(1).strip().replace("===", "").strip()
        return f"{CLEAN_DELIMITER}{filename}\n"

    content = HEADER_PATTERN.sub(replace_header, content)
    file_blocks = [b for b in content.split(CLEAN_DELIMITER) if b.strip()]

    if not file_blocks:
        print("Error: Could not find file blocks in markdown.", file=sys.stderr)
        return

    created_count = 0

    for block in file_blocks:
        parts = block.strip().split('\n', 1)
        if len(parts) < 2:
            continue

        file_path = parts[0].strip()
        file_content = parts[1].rstrip() + "\n"

        if not file_path:
            continue

        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"   [Directory Created] {directory}/")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

            print(f"✅ [File Created] {file_path}")
            created_count += 1

        except Exception as e:
            print(f"❌ [Error] Failed to create {file_path}: {e}", file=sys.stderr)

    print(f"\n--- Complete ---")
    print(f"Total {created_count} files successfully unpacked.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python unpacker.py [markdown_filename]")
        print("Example: python unpacker.py blackjack.md")
    else:
        unpack_project(sys.argv[1])