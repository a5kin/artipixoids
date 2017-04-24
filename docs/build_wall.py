#!/usr/bin/env python

import glob
import os
import random
from PIL import Image

CELLS_IN_ROW = 4
CELL_WIDTH = 300
IMG_PATH = "assets/img/gallery/mod2c/minies/*.png"

images = sorted(glob.glob(IMG_PATH), key=os.path.getmtime)
images = glob.glob(IMG_PATH)
random.shuffle(images)
cells = [['' for i in range(CELLS_IN_ROW)],]
img_id = 0
for img in images:
    width, height = Image.open(img).size
    width, height = width // CELL_WIDTH, height // CELL_WIDTH
    y = 0
    is_fit = False
    while y < len(cells) or not is_fit:
        for x in range(CELLS_IN_ROW - width + 1):
            for i in range(max(0, y + height - len(cells))):
                cells.append(['' for i in range(CELLS_IN_ROW)])
            is_fit = True
            for dy in range(height):
                for dx in range(width):
                    if cells[y + dy][x + dx]:
                        is_fit = False
            if is_fit:
                for dy in range(height):
                    for dx in range(width):
                        cells[y + dy][x + dx] = (img_id, img, width, height)
                break
        if is_fit:
            break
        y += 1
    print(img, width, height)
    img_id += 1

visited = set()
with open('mod2c_wall.html', 'w') as f:
    for row in cells:
        f.write("<tr>\n")
        for cell in row:
            if not cell:
                f.write("  <td>&nbsp;</td>\n")
                continue
            img_id, img, width, height = cell
            if img_id in visited:
                continue
            visited.add(img_id)
            f.write("  <td colspan='%s' rowspan='%s'><img src='%s' width='100%%'/></td>\n" % (width, height, img))
        f.write("</tr>\n")
        
for row in cells:
    print(" ".join(map(lambda x: str(x[0] if x else '  ').zfill(2), row)))
