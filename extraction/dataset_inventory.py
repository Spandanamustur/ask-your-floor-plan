
from pathlib import Path

# Dataset location
dataset_folder = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)

# Check folder
if not dataset_folder.exists():
    print("Dataset folder not found!")
    raise SystemExit

# Get all files
files = sorted(dataset_folder.iterdir())

json_files = []
original_images = []
mask_images = []
overlay_images = []
other_files = []

# Classify files
for file in files:

    if not file.is_file():
        continue

    name = file.name.lower()

    if file.suffix.lower() == ".json":
        json_files.append(file.name)

    elif name.endswith("_mask_image.png"):
        mask_images.append(file.name)

    elif name.endswith("_overlay.png"):
        overlay_images.append(file.name)

    elif file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        original_images.append(file.name)

    else:
        other_files.append(file.name)

# Display results
print("\n===== DATASET INVENTORY =====")

print("\nJSON FILES:", len(json_files))
for name in json_files:
    print(name)

print("\nORIGINAL IMAGE CANDIDATES:", len(original_images))
for name in original_images:
    print(name)

print("\nMASK IMAGES:", len(mask_images))
for name in mask_images:
    print(name)

print("\nOVERLAY IMAGES:", len(overlay_images))
for name in overlay_images:
    print(name)

print("\nOTHER FILES:", len(other_files))
for name in other_files:
    print(name)
