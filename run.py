import argparse
import cv2
from main import stitching
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('left', help="Path of left image.")
parser.add_argument('right', help="Path of right image.")
args = parser.parse_args()

left_image = cv2.imread(args.left)
right_image = cv2.imread(args.right)

result = stitching(left_image, right_image)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(2, 2, 1)
ax.set_title('(a) Left Image')
ax.imshow(left_image)
ax = fig.add_subplot(2, 2, 2)
ax.set_title('(b) Right Image')
ax.imshow(right_image)
ax = fig.add_subplot(2, 2, 3)
ax.set_title('(c) Stitching Image')
ax.imshow(result[1])
ax = fig.add_subplot(2, 2, 4)
ax.set_title('(d) Stitching Image(seamless)')
ax.imshow(result[0])

plt.tight_layout()	
plt.show()