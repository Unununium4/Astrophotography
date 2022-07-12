# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 18:31:02 2022

@author: Andrew Morrow
"""

import numpy as np
from os import listdir, mkdir
from os.path import isfile, join
from skimage import io
from skimage.color import rgb2gray

sumimg=np.ndarray([3000,3000,3])

mypath = r'C:/Users/Andrew Morrow/Desktop/astronomy/pics/28jan22/jupiter/ok2/sr'
files = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]

newpath = join(mypath,"final")#sr means shifted rotated
mkdir(newpath)

sharpnessarray = []
for i in range(len(files)):
    thisimg = io.imread(files[i])
    gray = rgb2gray(thisimg)
    gy, gx = np.gradient(gray)
    gnorm = np.sqrt(gx**2 + gy**2)
    sharpness = np.average(gnorm)
    sharpnessarray.append([files[i],sharpness])
    
    if sharpness >0.002: #i choose this arbitrarily
        sumimg += thisimg
        print("added image: "+str (i))
    
    print("on image: "+ str(i))

sumimg=(sumimg*255/np.max(sumimg)).astype(np.uint8)
io.imsave(join(newpath,'sum.jpg'),sumimg)