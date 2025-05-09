import cv2
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import os
from image_loader import ImageLoader
from patterns import create_pattern
from color_ranges import color_ranges

class ScreentoneProcessor:
    def __init__(self):
        self.pattern_map = {
                            'red1': create_pattern('horizontal_stripes'),
                            'red2': create_pattern('vertical_stripes'),
                            'orange': create_pattern('grid'),
                            'yellow': create_pattern('small_dots'),
                            'green': create_pattern('large_dots'),
                            'cyan': create_pattern('double_diagonals'),
                            'blue': create_pattern('diagonal_stripes'),
                            'purple': create_pattern('zigzag'),
                            'pink': create_pattern('waves'),
                            }

    def apply(self, hsv_image, rgb_image):
        result_image = np.ones(rgb_image.shape[:2], dtype=np.uint8) * 255

        for color, (low, high) in color_ranges.items():
            mask = cv2.inRange(hsv_image, np.array(low), np.array(high))
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            _, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)
            mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

            tile = np.tile(self.pattern_map[color], (result_image.shape[0] // self.pattern_map[color].shape[0] + 1,
                                                     result_image.shape[1] // self.pattern_map[color].shape[1] + 1))
            tile = tile[:result_image.shape[0], :result_image.shape[1]]

            result_image = np.where(mask == 255, tile, result_image)

        return cv2.convertScaleAbs(result_image, alpha=1.2, beta=0)

    def show(self, rgb_image, processed_image):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        ax1.imshow(rgb_image)
        ax1.set_title('Original Image')
        ax1.axis('off')
        ax2.imshow(processed_image, cmap='gray')
        ax2.set_title('Screentone Result')
        ax2.axis('off')
        plt.tight_layout()
        plt.show()

    def save(self, processed_image, original_path):
        base = os.path.splitext(os.path.basename(original_path))[0]
        folder = os.path.dirname(original_path)
        Image.fromarray(processed_image).save(os.path.join(folder, f"{base}_processed.jpg"), format='JPEG')

# Main function
def main():
    rgb_image, path = ImageLoader.load()
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    
    processor = ScreentoneProcessor()  # Create an instance of the class
    processed_image = processor.apply(hsv_image, rgb_image)
    
    processor.show(rgb_image, processed_image)
    processor.save(processed_image, path)

if __name__ == "__main__":
    main()