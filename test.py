import os
from PIL import Image

src = r"C:\PersonalProjects\DifSteam\resources"  # change if needed

for file in os.listdir(src):
    if file.lower().endswith(".png"):
        continue
    path = os.path.join(src, file)
    try:
        img = Image.open(path)
        largest = max(img.ico.sizes(), key=lambda s: s[0] * s[1])
        icon256 = img.ico.getimage(largest)
        png_path = os.path.join(src, os.path.splitext(file)[0] + ".png")
        icon256.save(png_path, format="PNG")
        print(f"Converted: {file} → {os.path.basename(png_path)}")
    except Exception as e:
        print(f"Failed {file}: {e}")
