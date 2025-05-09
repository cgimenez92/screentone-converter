import numpy as np
from PIL import Image, ImageDraw

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
