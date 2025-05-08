import cv2
from tkinter import Tk, filedialog

class ImageLoader:
    def load():
        Tk().withdraw()
        filename = filedialog.askopenfilename(title="Select Image")
        if not filename:
            raise FileNotFoundError("No image selected.")
        image_bgr = cv2.imread(filename)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        return image_rgb, filename
