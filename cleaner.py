#!/usr/bin/env python3

import os
import sys
import re

def choose_pattern():
    print("""
What do you want to remove?
1) Anything inside square brackets [ ... ]
2) Anything inside parentheses ( ... )
3) Anything inside double quotes " ... "
4) A custom literal pattern
5) Quit
""")
    choice = input("Enter your choice (1-5): ").strip()
    return choice

def get_custom_pattern():
    pat = input("Enter the exact literal pattern to remove (no regex): ").strip()
    return re.escape(pat)  # treat as literal

def main():
    infile = input("Enter the input file name (with .txt etc): ").strip()
    if not os.path.isfile(infile):
        print(f"File '{infile}' does not exist! Exiting.")
        sys.exit(1)

    try:
        with open(infile, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    patterns = []

    while True:
        choice = choose_pattern()
        if choice == "1":
            patterns.append(r"\[[^\]]*\]")
            print("Pattern to remove: anything inside square brackets [ ... ]")
        elif choice == "2":
            patterns.append(r"\([^)]*\)")
            print("Pattern to remove: anything inside parentheses ( ... )")
        elif choice == "3":
            patterns.append(r'"[^"]*"')
            print('Pattern to remove: anything inside double quotes " ..."')
        elif choice == "4":
            pat = get_custom_pattern()
            patterns.append(pat)
            print(f"Custom pattern '{pat}' added.")
        elif choice == "5":
            print("Quitting pattern selection.")
            break
        else:
            print("Invalid choice. Try again.")

        more = input("Do you want to add another pattern? (y/n): ").strip().lower()
        if more != "y":
            break

    if not patterns:
        print("No patterns selected. Exiting.")
        sys.exit(0)

    outfile = input("Enter the output file name: ").strip()
    if not outfile:
        print("No output file given. Exiting.")
        sys.exit(1)

    with open(outfile, "w", encoding="utf-8") as out:
        for line in lines:
            orig_line = line
            for pat in patterns:
                line = re.sub(pat, "", line)
            out.write(line)

    print(f"\n✅ Done! Cleaned file saved as '{outfile}'.")

if __name__ == "__main__":
    main()
