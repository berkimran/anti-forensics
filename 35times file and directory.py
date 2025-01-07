import os
import random
import argparse

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

def main():
    parser = argparse.ArgumentParser(description="Securely delete files or directories using the Gutmann method.")
    parser.add_argument("-f", "--file", type=str, help="Path to the file to securely delete.")
    parser.add_argument("-d", "--directory", type=str, help="Path to the directory to securely delete files from.")

    args = parser.parse_args()

    if args.file:
        gutmann_wipe(args.file)
    elif args.directory:
        gutmann_wipe_directory(args.directory)
    else:
        print("Please specify a file with -f or a directory with -d.")

if __name__ == "__main__":
    main()