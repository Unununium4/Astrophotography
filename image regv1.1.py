# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 09:47:14 2022

@author: Andrew Morrow
"""
from skimage.color import rgb2gray
import numpy as np
from skimage.registration import phase_cross_correlation
from skimage.transform import warp_polar, rotate
from skimage import io
from scipy.ndimage import fourier_shift
from os import listdir, mkdir, stat
from os.path import isfile, join
import scipy
#import rawpy

mypath = r'C:\Users\Andrew Morrow\Desktop\astronomy\pics\19feb22\andromeda'
files = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]

newpath = join(mypath,"sr")#sr means shifted rotated
mkdir(newpath)

timestart = stat(files[0]).st_mtime
timelast= stat(files[-1]).st_mtime
deltadeg= 57.7-49#last minus first
degpersec = deltadeg/(timelast-timestart)

#refnum = round(len(files)/2)
refnum = 137
time0 = stat(files[refnum]).st_mtime
#just to keep everyone happy i'll make sure the reference image is exactly the same as the others

#baseimg = rawpy.imread(files[refnum]).postprocess(output_bps=16)
baseimg = io.imread(files[refnum])
seclapsed = stat(files[refnum]).st_mtime - time0
baseimg = rotate(baseimg,seclapsed*degpersec)

io.imsave(join(newpath,'ref.tif'),((baseimg/np.max(baseimg))*(2**8-1)).astype(np.uint8))
del files[refnum]

grey1 = rgb2gray(baseimg)
radius = 2300
warped_image = warp_polar(grey1, radius=radius, scaling='log')


for i in range(len(files)):

    #thisimg = rawpy.imread(files[i]).postprocess(output_bps=16)
    thisimg = io.imread(files[i])
    seclapsed = stat(files[i]).st_mtime - time0
    
    thisimg = rotate(thisimg,seclapsed*degpersec)
    grey2 = rgb2gray(thisimg)
    shiftr=1
    n=0
    skipflag = False
    print('on image '+ str(i) + ' of ' + str(len(files)-1))
    while abs(shiftr)>0.1:
        'first correct translation then rotation'
        print("shift attempt " +str(n))
        shift, error, diffphase = phase_cross_correlation(grey1, grey2,upsample_factor=100)

        grey2 = fourier_shift(np.fft.fftn(grey2), shift)
        grey2 = np.fft.ifftn(grey2).real
        
        warped_rts = warp_polar(grey2, radius=radius, scaling='log')
        shifts, error, phxxsediff = phase_cross_correlation(warped_image,warped_rts,upsample_factor=100)

        shiftr = shifts[0]
        
        
        grey2=rotate(grey2,-shiftr)
        
        thisimg = scipy.ndimage.shift(thisimg,[shift[0],shift[1],0],order=0)
        thisimg = rotate(thisimg,-shiftr)
        n+=1
        print("rotation found: " +str(shiftr))
        if n==6:
            skipflag =True
            break
    if skipflag:
        print('skipping image, too many tries (6)')
        continue

    
    io.imsave(join(newpath,str(i)+'.tif'),((thisimg/np.max(thisimg))*(2**8-1)).astype(np.uint8))