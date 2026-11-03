import csv
from pathlib import Path
import sys
import time


# ==========================================================
# Project root
# ==========================================================

root_folder = Path(__file__).resolve().parents[2]

# Data folder
data_folder = root_folder / "data"


# ==========================================================
# Find CSV files
# ==========================================================

csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    print("No CSV files found in the data folder.")
    sys.exit()


# ==========================================================
# Show available files
# ==========================================================

print("Available CSV files:\n")

for i, file in enumerate(csv_files, start=1):
    print(f"{i}. {file.name}")


# ==========================================================
# Choose file
# ==========================================================

while True:
    try:
        choice = int(input("\nChoose a file: "))

        if 1 <= choice <= len(csv_files):
            csv_file = csv_files[choice - 1]
            break

        print("Invalid choice. Please select a number.")

    except ValueError:
        print("Please enter a number.")


print(f"\nSelected: {csv_file.name}")


# ==========================================================
# Count rows
# ==========================================================

print("\nPreparing file...")

with open(csv_file, mode="r", encoding="utf-8", newline="") as file:
    total_rows = sum(1 for _ in file) - 1  # subtract header


# ==========================================================
# Process CSV
# ==========================================================

print(f"Processing {total_rows:,} rows...\n")

with open(csv_file, mode="r", encoding="utf-8", newline="") as file:

    reader = csv.reader(file)

    # Skip header
    header = next(reader)

    for current_row, row in enumerate(reader, start=1):

        # ----------------------------------------------
        # Your actual processing goes here
        # ----------------------------------------------

        # Example:
        # print(row)

        # ----------------------------------------------
        # Progress
        # ----------------------------------------------

        percentage = current_row / total_rows
        bar_length = 40

        filled = int(bar_length * percentage)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(
            f"\rProcessing: |{bar}| "
            f"{percentage * 100:6.2f}% "
            f"({current_row:,}/{total_rows:,})",
            end="",
            flush=True
        )

        # Only here to make the loading visible during testing
        # Remove this in your real pipeline
        # time.sleep(0.01)


print("\n\nProcessing complete!")