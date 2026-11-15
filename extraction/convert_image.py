
from pathlib import Path
from PIL import Image
import cv2

# Original image
source = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell\loopnet3.png"
)

# Save converted image separately
destination = source.parent / "loopnet3_converted.png"

# Open original image
with Image.open(source) as img:

    print("Original format:", img.format)
    print("Original dimensions:", img.size)

    # Convert to RGB
    rgb_image = img.convert("RGB")

    # Save as genuine PNG
    rgb_image.save(destination, format="PNG")

print("\nConverted image saved:", destination)

# Verify with OpenCV
image = cv2.imread(str(destination))

if image is not None:
    print("OpenCV verification: SUCCESS")
    print("Converted dimensions:", image.shape)
else:
    print("OpenCV verification: FAILED")
