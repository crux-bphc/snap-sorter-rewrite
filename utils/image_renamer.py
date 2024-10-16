import os

INPUT_DIR = r"data\alpha"

images = os.listdir(INPUT_DIR)
start = len(os.listdir(r'data\images'))

for i, image in enumerate(images):
    os.rename(os.path.join(INPUT_DIR, image), os.path.join(INPUT_DIR, f"{str(start+i).zfill(4)}.jpg"))
    print(f"Renamed {image} to {str(start+i).zfill(4)}.jpg")