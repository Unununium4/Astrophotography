# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:38:38 2022

@author: Andrew Morrow
"""
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join
from skimage import io
import cv2
#import rawpy
#import matplotlib.pyplot as plt


mypath = r'C:\Users\Andrew Morrow\Desktop\astronomy\pics\19feb22\andromeda\sr'
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

narr[np.sum(sumimg,axis=2)==0]=1
sumimg/=narr

sumimg[sumimg<0]=0
sumimg[sumimg>1]=1
#sumimg[sumimg>2**16-1]=2**16-1

# #allmean=np.mean(sumimg)
# #rmoff=np.mean(sumimg[:,:,0])-allmean
# #gmoff=np.mean(sumimg[:,:,1])-allmean
# #bmoff=np.mean(sumimg[:,:,2])-allmean
# #normimg[:,:,0]-=rmoff
# #normimg[:,:,1]-=gmoff
# #normimg[:,:,2]-=bmoff
# normimg[normimg<0]=0
# normimg[normimg>2**16-1]=2**16-1

normimg=cv2.normalize(src=sumimg,dst=None,alpha=0,beta=2**16-1,norm_type=cv2.NORM_MINMAX,dtype = cv2.CV_16U)
avg8bit=cv2.normalize(src=sumimg,dst=None,alpha=0,beta=2**16-1,norm_type=cv2.NORM_MINMAX,dtype = cv2.CV_8U)
io.imsave(join(newpath,'normavg.tif'),normimg)
io.imsave(join(newpath,'normavg.jpg'),avg8bit)

