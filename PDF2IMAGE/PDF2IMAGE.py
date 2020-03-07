from pdf2image import convert_from_path
import sys
import os
import numpy as np
from PIL import Image, ImageDraw
import PIL
import tkinter as tk
from tkinter import filedialog
import math

#OPTIONS AND PARAMETERS
imgperRow = 10
masterDPI = 100

#SETUP
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
pages = convert_from_path(file_path, masterDPI)
blankpages = convert_from_path('D:\PDF\RESOURCES\BlankTemplate.pdf', masterDPI)
PageCount = 0
imgperRow = round(math.sqrt(len(pages)) + 0.01)

#IMAGE LISTS
image_Export = []
active_Row = []
rowIMGs = []

#IMAGE NUMBERS
master_Tracker = -1
rowNum = 0
lengthofPDF = len(pages)


#CACHE CLEAR
os.system('echo "y" | del /S D:\PDF\DUMP\out\ROWs\*.*')

#####################################################################################################################################################################################################
for page in blankpages:
    page.save('D:\PDF\DUMP' + '\BLANK.jpg', 'JPEG')
    blanker = 'D:\PDF\DUMP' + '\BLANK.jpg'

for page in pages:
    PageCount += 1
    page.save('D:\PDF\DUMP' + '\out' + str(PageCount) + '.jpg', 'JPEG')
    image_Export.append('D:\PDF\DUMP' + '\out' + str(PageCount) + '.jpg')

    print((PageCount / lengthofPDF) * 100)

sizeMain = 1062, 1375

#MAIN ROWS
for pageNumber in range(lengthofPDF // imgperRow):
    active_Row = []


    for x in range(imgperRow):

        master_Tracker += 1
        active_Row.append(image_Export[master_Tracker])



    #add images to row
    list_im = active_Row
    imgs    = [ PIL.Image.open(i) for i in list_im ]
    #matches images to smallest image
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    imgs_comb = PIL.Image.fromarray( imgs_comb)
    rowNum += 1 
    imgs_comb.save('D:\PDF\DUMP\out\ROWs\Row' + str(rowNum) + '.jpg' )
    rowIMGs.append('D:\PDF\DUMP\out\ROWs\Row' + str(rowNum) + '.jpg' )

#LEFT OVERS 

for pageNumber in range(lengthofPDF % imgperRow):
    active_RowF = []
    
    for x in range(imgperRow):
        
       try:
           master_Tracker += 1
           active_RowF.append(image_Export[master_Tracker])
       except:
           active_RowF.append(blanker)

    #add images to row
    list_imSECOND = active_RowF
    imgsSECOND    = [ PIL.Image.open(i) for i in list_imSECOND ]
    #matches images to smallest image
    min_shapeSECOND = sorted( [(np.sum(i.size), i.size ) for i in imgsSECOND])[0][1]
    imgs_combSECOND = np.hstack( (np.asarray( i.resize(min_shapeSECOND) ) for i in imgsSECOND ) )

    imgs_combSECOND = PIL.Image.fromarray( imgs_combSECOND)
    rowNum += 1 
    imgs_combSECOND.save('D:\PDF\DUMP\out\ROWs\Row' + str(rowNum) + '.jpg' )
    rowIMGs.append('D:\PDF\DUMP\out\ROWs\Row' + str(rowNum) + '.jpg' )
    

#FINAL VERTICAL ROW STACKER
list_im = rowIMGs
imgs    = [ PIL.Image.open(i) for i in list_im ]
#matches images to smallest image
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

#stacks horizontal rows vertically
imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( 'D:\PDF\DUMP\out\FINAL.png' )
