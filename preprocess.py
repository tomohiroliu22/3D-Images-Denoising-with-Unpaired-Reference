import os
import numpy as np
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataroot', required=True, help='path to c-scan dataset')
parser.add_argument('--saveroot', required=True, help='path to save processed images')
opts = parser.parse_args()

def normal(data,MIN,MAX):
    w,h=data.shape
    data=data.ravel()
    vmin,vmax=np.percentile(data,(MIN,MAX))
    data[data<vmin]=vmin
    data[data>vmax]=vmax
    data=(data-vmin)/(vmax-vmin)
    data=data.reshape(w,h)
    return data

def c_scan_prepro(filename, vertical_savepath, horizontal_savepath, opts):
    # open the C-scan bin file
    A = np.fromfile(opts.dataroot+"/"+filename, dtype='float32', sep="").reshape(384,1000,1000)

    # Polynomial fitting normalization
    y = np.zeros(384)
    for i in range(384):
        y[i] = np.mean(A[i].ravel())
    x = np.arange(384)/384
    z = np.polyfit(x, y, 12)
    p = np.poly1d(z)
    y_pred = p(x)

    title = filename[:-4]

    # Vertical cross-sectional images processing
    print("Processing for vertical direction")
    for a in range(1000):
        new_img = np.zeros((384,1000))
        if(a < 2):
            img = normal(A[:,:,a],2,98)
            for i in range(384):
                new_img[i] = A[i,:,a] + (y_pred[i]-y[i])
        elif(a > 997):
            img = normal(A[:,:,a],2,98)
            for i in range(384):
                new_img[i] = A[i,:,a] + (y_pred[i]-y[i])
        else:
            img = normal(np.mean(A[:,:,a-2:a+3],axis=2),2,98)
            for i in range(384):
                new_img[i] = np.mean(A[i,:,a-2:a+3],axis=1) + (y_pred[i]-y[i])
        new_img = normal(new_img,2,98)
        img_l = np.zeros((384,512))
        img_r = np.zeros((384,512))
        img_l[:,6:506] = new_img[:,:500]
        img_r[:,6:506] = new_img[:,500:]
        img_l = Image.fromarray(np.uint8(img_l*255))
        img_r = Image.fromarray(np.uint8(img_r*255))
        img_l.save(vertical_savepath+title+"_"+str(a).zfill(4)+"_1"+".png")
        img_r.save(vertical_savepath+title+"_"+str(a).zfill(4)+"_2"+".png")
        break

    # Horizontal cross-sectional images processing
    print("Processing for horizontal direction")
    for a in range(1000):
        new_img = np.zeros((384,1000))
        if(a < 2):
            img = normal(A[:,a,:],2,98)
            for i in range(384):
                new_img[i] = A[i,a,:] + (y_pred[i]-y[i])
        elif(a > 997):
            img = normal(A[:,a,:],2,98)
            for i in range(384):
                new_img[i] = A[i,a,:] + (y_pred[i]-y[i])
        else:
            img = normal(np.mean(A[:,a-2:a+3,:],axis=1),2,98)
            for i in range(384):
                new_img[i] = np.mean(A[i,a-2:a+3,:],axis=0) + (y_pred[i]-y[i])
        new_img = normal(new_img,2,98)
        img_l = np.zeros((384,512))
        img_r = np.zeros((384,512))
        img_l[:,6:506] = new_img[:,:500]
        img_r[:,6:506] = new_img[:,500:]
        img_l = Image.fromarray(np.uint8(img_l*255))
        img_r = Image.fromarray(np.uint8(img_r*255))
        img_l.save(horizontal_savepath+title+"_"+str(a).zfill(4)+"_1"+".png")
        img_r.save(horizontal_savepath+title+"_"+str(a).zfill(4)+"_2"+".png")
        break


for filename in sorted(os.listdir(opts.dataroot)):
    print("Processing for "+filename)
    c_scan_prepro(filename, opts.saveroot+"/vertical/", opts.saveroot+"/horizontal/",opts)
print("Processing End")
