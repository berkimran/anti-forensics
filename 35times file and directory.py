import os
import random
import argparse
import subprocess

def gutmann_wipe(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    file_size = os.path.getsize(file_path)

    try:
        with open(file_path, 'r+b') as f:
            for pass_num in range(35):
                random_data = os.urandom(file_size)
                f.seek(0)
                f.write(random_data)
                print(f"Pass {pass_num + 1}/35 completed.")

        with open(file_path, 'w') as f:
            pass

        os.remove(file_path)
        print(f"File {file_path} securely deleted.")

    except Exception as e:
        print(f"Error while wiping file: {e}")

def gutmann_wipe_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    if not os.path.isdir(directory_path):
        print(f"Provided path is not a directory: {directory_path}")
        return

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            gutmann_wipe(file_path)

def gutmann_wipe_shadow_copies():
    try:
        result = subprocess.run(["vssadmin", "list", "shadows"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Failed to list shadow copies. Ensure you have administrative privileges.")
            return

        shadow_lines = [line for line in result.stdout.splitlines() if "Shadow Copy Volume" in line]
        shadow_ids = [line.split(":")[-1].strip() for line in shadow_lines]

        if not shadow_ids:
            print("No shadow copies found.")
            return

        for shadow_id in shadow_ids:
            print(f"Wiping shadow copy: {shadow_id}")
            for _ in range(35):
                subprocess.run(["vssadmin", "delete", "shadows", "/Shadow={}".format(shadow_id), "/Quiet"], check=True)
                print(f"Pass completed for shadow copy {shadow_id}.")

        print("All shadow copies securely deleted.")

    except Exception as e:
        print(f"Error while wiping shadow copies: {e}")

def main():
    parser = argparse.ArgumentParser(description="Securely delete files, directories, or shadow copies using the Gutmann method.")
    parser.add_argument("-f", "--file", type=str, help="Path to the file to securely delete.")
    parser.add_argument("-d", "--directory", type=str, help="Path to the directory to securely delete files from.")
    parser.add_argument("-s", "--shadow", action="store_true", help="Securely delete all shadow copies on the system.")

    args = parser.parse_args()

    if args.file:
        gutmann_wipe(args.file)
    elif args.directory:
        gutmann_wipe_directory(args.directory)
    elif args.shadow:
        gutmann_wipe_shadow_copies()
    else:
        print("Please specify a file with -f, a directory with -d, or use -s to wipe shadow copies.")

if __name__ == "__main__":
    main()
