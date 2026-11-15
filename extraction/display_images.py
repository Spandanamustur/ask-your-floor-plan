
from pathlib import Path
import cv2
import matplotlib.pyplot as plt


dataset_folder = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)


original_path = dataset_folder / "floorplan.jpg"
mask_path = dataset_folder / "floorplan_mask_image.png"


original = cv2.imread(str(original_path))
mask = cv2.imread(str(mask_path), cv2.IMREAD_UNCHANGED)


if original is None:
    raise FileNotFoundError(
        f"Original image not found: {original_path}"
    )

if mask is None:
    raise FileNotFoundError(
        f"Mask image not found: {mask_path}"
    )


print("Original image dimensions:", original.shape)
print("Mask image dimensions:", mask.shape)


original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)


plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(original_rgb)
plt.title("Original Floor Plan")
plt.axis("off")

plt.subplot(1, 2, 2)

if len(mask.shape) == 2:
    plt.imshow(mask, cmap="gray")
elif mask.shape[2] == 3:
    plt.imshow(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
else:
    plt.imshow(mask[:, :, :3])

plt.title("Segmentation Mask")
plt.axis("off")

plt.tight_layout()
plt.show()

import numpy as np


print("\nMASK INFORMATION")

print("Mask dimensions:", mask.shape)
print("Data type:", mask.dtype)

print("Minimum pixel value:", mask.min())
print("Maximum pixel value:", mask.max())


unique_values = np.unique(mask)

print("Unique pixel values:", unique_values)
print("Total unique values:", len(unique_values))
#analysis
import numpy as np

print("\n--- MASK ANALYSIS ---")

print("Mask shape:", mask.shape)
print("Mask data type:", mask.dtype)

print("Minimum value:", mask.min())
print("Maximum value:", mask.max())

unique_values = np.unique(mask)

print("Unique pixel values:", unique_values)
print("Number of unique values:", len(unique_values))

#pixcel freq
print("\n--- PIXEL VALUE FREQUENCY ---")

values, counts = np.unique(mask, return_counts=True)

for value, count in zip(values, counts):
    percentage = (count / mask.size) * 100

    print(
        f"Pixel value {value}: "
        f"{count} pixels "
        f"({percentage:.2f}%)"
    )
