import os

# Set the directory containing the files
directory = "fixed_rain"

# Define the old and new prefixes
old_prefix = "hiv00223"
new_prefix = "fixed_rain"

# Iterate through the files in the directory
for filename in os.listdir(directory):
    if filename.startswith(old_prefix):  # Only rename files that start with the old prefix
        new_filename = filename.replace(old_prefix, new_prefix, 1)  # Replace only the first occurrence
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)

        os.rename(old_path, new_path)  # Rename the file
        print(f"Renamed: {filename} → {new_filename}")

print("Batch renaming completed successfully!")
