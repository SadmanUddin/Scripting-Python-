import os
import cv2
import requests
import datetime
from ultralytics import YOLO
import io
from contextlib import redirect_stdout
import sys

I_dir = "Images"
R_dir = "runs/detect"

def downloadAndDetect():
    os.makedirs(I_dir, exist_ok=True)
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, "w")
    model = YOLO("yolov8n.pt")
    sys.stderr.close()
    sys.stderr = old_stderr

    detection = {}
    idx = 0  
    for i in range(641, 673):
        width, height = 1000, 900
        url = f"https://picsum.photos/id/{i}/{width}/{height}"

        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            continue

        filename = f"{I_dir}/original_{idx}.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        img = cv2.imread(filename)
        if img is None:
            os.remove(filename)
            continue
        old_stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")
        saving = model(filename, save=True)
        sys.stderr.close()
        sys.stderr = old_stderr

        detected_imgs = []
        for j in saving:
            if j.boxes is not None:
                for k in j.boxes.cls:
                    detected_imgs.append(model.names[int(k)])

        detection[filename] = detected_imgs
        idx += 1 

    return detection

def painting(filename):
    api_key = "" # create an apikey from cloudmersive...usefull
    url = "https://api.cloudmersive.com/image/artistic/wave"
    headers = {"Apikey": api_key}

    with open(filename, "rb") as f:
        response = requests.post(url, headers=headers, files={"imageFile": f})

    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outname = f"painting_{now}.jpg"

    with open(outname, "wb") as f:
        f.write(response.content)

    return f"Image successfully saved as {outname}"
    
def grayscale(filename):
    img = cv2.imread(filename)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    base = os.path.basename(filename).replace(".jpg","")
    realname = f"{base}_gray.jpg"
    cv2.imwrite(realname, gray)
    
    return f"Grayscale image saved as {realname}"

def blur(filename):
    img = cv2.imread(filename)
    if img is None:
        return None
    blur = cv2.GaussianBlur(img, (21,21),0)

    base2 = os.path.basename(filename).replace(".jpg","")
    realname2 = f"{base2}_blurred.jpg"
    cv2.imwrite(realname2, blur)

    return f"Blurred image saved as {realname2}"

def main():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        detection = downloadAndDetect()
    print(detection)

    for filepath, objects in detection.items():
        fname = os.path.basename(filepath)
        print(fname, objects)
        msg = None
        if "person" in objects:
            msg = painting(filepath)
        elif len(objects) == 0:
            msg = grayscale(filepath)
        else:
            msg = blur(filepath)
        if msg is not None:
            print(msg)

if __name__ == "__main__":
    main()