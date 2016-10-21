# -*- coding:utf-8 -*-
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import glob
import os
sys.path.append("../lib/")
import yam
import file_read as f_r
import math
from numpy.linalg import inv, cholesky
import time
import Prob_Cal

result_dir = sys.argv[1]
env_para=np.genfromtxt(result_dir+"/Parameter.txt",dtype= None,delimiter =": ")
pi=np.loadtxt(result_dir+"pi.csv")

pi_row=np.sum(pi,axis=0)
pi=np.array(([[1.0 for j in range(100)] for i in range(50)]))
map_cut=150
color=np.array(
[[21,0,219],[65,255,0],[143,15,239],[0,47,168],[76,183,254]
,[204,0,135],[200,0,12],[135,22,25],[167,227,156],[0,254,254]
,[96,53,124],[224,196,183],[166,172,123],[0,204,142],[70,53,119]
,[94,25,255],[255,65,0],[255,127,171],[96,69,51],[224,81,109]
,[38,45,63],[179,37,240],[73,45,107],[64,130,22],[111,67,136]
,[22,206,172],[29,0,254],[82,188,15],[161,143,243],[232,41,209]]
)
local_color=np.loadtxt("../parameter/local_color.txt")
y=yam.Yaml()
y.yaml_read(glob.glob(env_para[8][1]+"/map/""*.yaml")[0])
param_mu=f_r.mu_read(result_dir)
param_sigma=f_r.sigma_read(result_dir)
param_ramda=np.array(f_r.ramda_read(result_dir))
Boundary=0
#os.mkdir(result_dir+"/color_map")
print env_para[8][1]+"/map/"+y.file
im = cv2.imread(env_para[8][1]+"/map/"+y.file)

height, width, channels = im.shape

for angle in range(4):
    start = time.time()
    img_prob = im.copy()
    img = im.copy()
    img_local = im.copy()
    if angle==0:
        cordinate=[y.origin[0],y.origin[1]+(map_cut*0.05),0,1]
    elif angle==1:
        cordinate=[y.origin[0],y.origin[1]+(map_cut*0.05),1,0]
    elif angle==2:
        cordinate=[y.origin[0],y.origin[1]+(map_cut*0.05),0,-1]
    elif angle==3:
        cordinate=[y.origin[0],y.origin[1]+(map_cut*0.05),-1,0]
    print cordinate[0],cordinate[1]
    all_class=[]
    h=height-1-map_cut
    
    while(h>=100):
        cordinate[0]=y.origin[0]+(0.05*map_cut)
        for i in range(map_cut,width-map_cut,1):
        #for i in range(0,width,1):

            word_prob=np.array([0.0 for k in xrange(len(param_ramda[0]))])
            r_prob=np.array([1.0 for k in xrange(len(param_mu))])
            max=np.array([0.0])
            if im[h][i][0]==254:
                for r in xrange(len(param_mu)):

                    r_prob[r]+=Prob_Cal.multi_gaussian_log(cordinate,param_mu[r],param_sigma[r]) #p(x_t|r_t)
                    r_prob[r]+=math.log(pi_row[r]) #p(r_t)

                r_prob -=np.max(r_prob)
                r_prob =np.exp(r_prob)
                r_prob =Prob_Cal.normalize(r_prob)
                class_index=np.argmax(r_prob)
                #print class_index
                img_local[h][i]=list(local_color[class_index])
                r_prob=Prob_Cal.normalize(r_prob)
                for r in xrange(len(param_mu)):
                    for c in range(len(param_ramda)):
                        for w in range(len(param_ramda[0])):
                             
                            word_prob[w] +=param_ramda[c][w]*pi[c][r]*r_prob[r] #p(w_t|C_t)p(r_t|C_t)p(r_t|x_t)
                            #word_prob[w] +=param_ramda[c][w]*r_prob[r]
                word_prob=Prob_Cal.normalize(word_prob)
                print word_prob
                if np.max(word_prob)>Boundary:
                    class_index=np.argmax(word_prob)
                    p=np.max(word_prob)
                    
                    img_prob[h][i]=list(color[class_index]*(p+0.3))
                    img[h][i]=list(color[class_index])
                    print h,i,class_index
            cordinate[0] +=0.05
        h-=1
        cordinate[1] +=0.05

    print("Done in %.2f s." % (time.time() - start))
    
    cv2.imwrite(result_dir+"/color_map/place_color_local_class_map"+repr(angle)+".png", img_local)
    cv2.imwrite(result_dir+"/color_map/place_color_map"+repr(angle)+".png", img)
    cv2.imwrite(result_dir+"/color_map/place_color_prob_map"+repr(angle)+".png", img_prob)
    