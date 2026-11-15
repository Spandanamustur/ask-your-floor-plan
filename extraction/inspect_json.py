import json
from pathlib import Path
file_path=Path( r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell\floorplan.json")
with open(file_path,"r",encoding="utf-8") as file:
    data=json.load(file)
shapes=data["shapes"]
label_counts={}
for shape in shapes:
    label=shape["label"]
    if label in label_counts:
        label_counts[label]+=1
    else:
        label_counts[label]=1
print("TOTAL ANNOTATED OBJECTS",len(shapes))
print("\nLABEL COUNTS:")
for label,count in label_counts.items():
    print(label, ":",count)