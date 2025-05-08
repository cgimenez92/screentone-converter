import cv2
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import os
from image_loader import ImageLoader

# Function to create grayscale screentone patterns
def create_pattern(pattern_type, size=12):
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)

    if pattern_type == 'horizontal_stripes':
        for i in range(0, size, 2):
            draw.line((0, i, size, i), fill=0, width=1)
    elif pattern_type == 'vertical_stripes':
        for i in range(0, size, 2):
            draw.line((i, 0, i, size), fill=0, width=1)
    elif pattern_type == 'diagonal_stripes':
        for i in range(-size, size, 2):
            draw.line((i, size, i + size, 0), fill=0, width=1)
    elif pattern_type == 'large_dots':
        for x in range(1, size, 6):
            for y in range(1, size, 6):
                draw.ellipse((x, y, x+3, y+3), fill=0)
    elif pattern_type == 'small_dots':
        for x in range(1, size, 3):
            for y in range(1, size, 3):
                draw.ellipse((x, y, x+1, y+1), fill=0)
    elif pattern_type == 'double_diagonals':
        for i in range(-size, size, 2):
            draw.line((i, size, i+size, 0), fill=0, width=1)
            draw.line((i, 0, i+size, size), fill=0, width=1)
    elif pattern_type == 'grid':
        for x in range(0, size, 2):
            for y in range(0, size, 2):
                draw.rectangle((x, y, x+2, y+2), outline=0, width=1)
    elif pattern_type == 'zigzag':
        for i in range(0, size, 2):
            draw.line((i, 0, i+1, size), fill=0, width=1)
            draw.line((i+1, 0, i, size), fill=0, width=1)
    elif pattern_type == 'waves':
        for i in range(0, size, 2):
            draw.line((i, int(size/2), i+2, int(size/2)-2), fill=0, width=1)
            draw.line((i+2, int(size/2)-2, i+4, int(size/2)), fill=0, width=1)

    return np.array(img)

# Function to apply screentones to each color based on HSV ranges
def apply_screentones(hsv_image, rgb_image):
    color_ranges = {
        'red1':     [(0, 100, 100), (5, 255, 255)],
        'red2':     [(175, 100, 100), (180, 255, 255)],
        'orange':   [(6, 120, 120), (20, 255, 255)],
        'yellow':   [(21, 100, 100), (30, 255, 255)],
        'green':    [(36, 80, 80), (85, 255, 255)],
        'cyan':     [(86, 80, 80), (95, 255, 255)],
        'blue':     [(96, 80, 80), (130, 255, 255)],
        'purple':   [(131, 80, 80), (160, 255, 255)],
        'pink':     [(161, 80, 80), (169, 255, 255)],
    }

    patterns = {
        'red1': create_pattern('horizontal_stripes'),
        'red2': create_pattern('vertical_stripes'),
        'orange': create_pattern('grid'),
        'yellow': create_pattern('small_dots'),
        'green': create_pattern('large_dots'),
        'cyan': create_pattern('double_diagonals'),
        'blue': create_pattern('diagonal_stripes'),
        'purple': create_pattern('zigzag'),
        'pink': create_pattern('waves')
    }

    result_image = np.ones(rgb_image.shape[:2], dtype=np.uint8) * 255

    for color, (low, high) in color_ranges.items():
        mask = cv2.inRange(hsv_image, np.array(low), np.array(high))
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        _, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

        tile = np.tile(patterns[color], (result_image.shape[0] // patterns[color].shape[0] + 1,
                                         result_image.shape[1] // patterns[color].shape[1] + 1))
        tile = tile[:result_image.shape[0], :result_image.shape[1]]

        result_image = np.where(mask == 255, tile, result_image)

    result_image = cv2.convertScaleAbs(result_image, alpha=1.2, beta=0)
    return result_image

# Function to display the original and processed images side by side
def show_result(rgb_image, processed_image):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.imshow(rgb_image)
    ax1.set_title('Original Image')
    ax1.axis('off')
    ax2.imshow(processed_image, cmap='gray')
    ax2.set_title('Result with Screentones')
    ax2.axis('off')
    plt.tight_layout()
    plt.show()

# Function to save the result image next to the original one
def save_result(processed_image, original_path):
    base_name = os.path.splitext(os.path.basename(original_path))[0]
    folder = os.path.dirname(original_path)
    result_img = Image.fromarray(processed_image)
    save_path = os.path.join(folder, f"{base_name}_processed.jpg")
    result_img.save(save_path, format='JPEG')
    print(f"Image saved as {save_path}")

# Main function
def main():
    rgb_image, path = ImageLoader.load()
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    processed_image = apply_screentones(hsv_image, rgb_image)
    show_result(rgb_image, processed_image)
    save_result(processed_image, path)

if __name__ == "__main__":
    main()
