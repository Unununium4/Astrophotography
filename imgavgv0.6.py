# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:38:38 2022

@author: Andrew Morrow
"""
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join
from skimage import io
#import rawpy
#import matplotlib.pyplot as plt

mypath = r'C:\Users\Andrew Morrow\Desktop\astronomy\pics\05feb22\raws\sr'
files = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]

#raw = rawpy.imread(files[0]).postprocess()

raw=io.imread(files[0])

sumimg=np.ndarray(raw.shape)
narr=np.ndarray(raw.shape)

newpath = join(mypath,"final")#sr means shifted rotated
mkdir(newpath)

for i in range(len(files)):
    thisimg = io.imread(files[i])
    #thisimg = rawpy.imread(files[i]).postprocess(output_bps=16)
    sumimg += thisimg
    narr[np.sum(thisimg,axis=2)!=0]+=1
    print('on image '+ str(i) + ' of ' + str(len(files)))

narr[np.sum(thisimg,axis=2)==0]=1
sumimg/=narr

sumimg[sumimg<0]=0
sumimg[sumimg>2**16-1]=2**16-1

allmean=np.mean(sumimg)
rmoff=np.mean(sumimg[:,:,0])-allmean
gmoff=np.mean(sumimg[:,:,1])-allmean
bmoff=np.mean(sumimg[:,:,2])-allmean
normimg = sumimg.astype(np.float64)
normimg[:,:,0]-=rmoff
normimg[:,:,1]-=gmoff
normimg[:,:,2]-=bmoff
normimg[normimg<0]=0
normimg[normimg>2**16-1]=2**16-1
normimg=np.round(normimg).astype(np.uint16)

normimg = normimg.astype(np.uint16)
io.imsave(join(newpath,'normavg.tif'),normimg)
avg8bit = (np.round(255*normimg.astype(np.float64)/np.max(normimg))).astype(np.uint8)
io.imsave(join(newpath,'normavg.jpg'),avg8bit)