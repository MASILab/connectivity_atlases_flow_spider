#!/usr/bin/env python

import sys

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from skimage.util import montage
from PIL import Image, ImageChops

img_labels = nib.load(sys.argv[1])
data_labels = img_labels.get_fdata()
data_labels = np.rot90(data_labels, axes=(0,2))

unique = np.unique(data_labels)[1:]
random = np.random.random(len(unique)) * 10000000
for i in range(len(unique)):
    data_labels[data_labels == unique[i]] = int(random[i])
montage_labels = montage(data_labels[::5, :, :], fill=0)

img_t1 = nib.load(sys.argv[2])
data_t1 = img_t1.get_fdata()
data_t1 = np.rot90(data_t1, axes=(0,2))
montage_t1 = montage(data_t1[::5, :, :], fill=0)

mask = np.zeros(montage_labels.shape, dtype=bool)
mask[montage_labels > 0] = 1

plt.imshow(montage_labels, cmap ='hsv')
plt.axis('off')
plt.savefig('tmp_labels.png', bbox_inches='tight', pad_inches=0, dpi=600)

plt.imshow(montage_t1, cmap ='gray')
plt.axis('off')
plt.savefig('tmp_t1.png', bbox_inches='tight', pad_inches=0, dpi=600)

plt.imshow(mask, cmap ='gray')
plt.axis('off')
plt.savefig('tmp_mask.png', bbox_inches='tight', pad_inches=0, dpi=600)

img = Image.open('tmp_labels.png')
background = Image.open('tmp_t1.png')
mask = Image.open('tmp_mask.png').convert('L').resize(img.size)

im = Image.composite(img, background, mask)
im.save(sys.argv[3])