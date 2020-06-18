# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
from os import listdir, getcwd
from os.path import join
import os
import random
import shutil


# basedir = r'/home/data/'
# xmlfilepath = r'/home/data/Annotations'
# txtsavepath = r'/home/data/ImageSets'
# labelspath = r'/home/data/labels'
# JPEGspath = r'/home/data/JPEGImages'
# imagespath = r'/home/data/images'


basedir = r'G:/dataset/maskdata/'
rootdir=r'F:/deep/mask_dect/data2/'
xmlfilepath = rootdir+'Annotations'
txtsavepath = rootdir+'ImageSets'
labelspath = rootdir+'labels'
JPEGspath = rootdir+'JPEGImages'
imagespath = rootdir+'images'

'''
dirs=[xmlfilepath,txtsavepath,labelspath,JPEGspath,imagespath]
for dir in dirs:
    os.makedirs(dir,exist_ok=True)
folds=os.listdir(basedir)
for fold in folds:
    if os.path.isdir(os.path.join(basedir,fold)):
        files=os.listdir(os.path.join(basedir,fold))
        for i in range(len(files)):
            if files[i].split('.')[-1]=='xml':
                shutil.copy(os.path.join(basedir,fold,files[i]),xmlfilepath)
            else:
                shutil.copy(os.path.join(basedir,fold,files[i]),JPEGspath)
                shutil.copy(os.path.join(basedir,fold,files[i]),imagespath)

'''
trainval_percent = 0.1
train_percent = 0.9


total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(txtsavepath+os.sep+'trainval.txt', 'w')
ftest = open(txtsavepath+os.sep+'test.txt', 'w')
ftrain = open(txtsavepath+os.sep+'train.txt', 'w')
fval = open(txtsavepath+os.sep+'val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftest.write(name)
        else:
            fval.write(name)
    else:
        ftrain.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()

# -------------------------------voc_label--------------------


sets = ['train', 'test', 'val']

classes = ["face_mask", "face"]  #

tmp=[]
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open(xmlfilepath+'/%s.xml' % (image_id))
    print(xmlfilepath+'/%s.xml' % (image_id))
    out_file = open(labelspath+'/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    if size is None:
        return
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w is None or h is None:
        return

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in tmp:
            tmp.append(cls)
        if cls not in classes or int(difficult) == 1:
            continue
        if cls == "face_nask":
            cls = "face_mask"
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        if w==0 or h==0:
            continue
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()
print(wd)
for image_set in sets:
    if not os.path.exists(labelspath+'/'):
        os.makedirs(labelspath+'/')
    image_ids = open(txtsavepath+'/%s.txt' % (image_set)).read().strip().split()

    list_file = open(rootdir+'%s.txt' % (image_set), 'w')
    for image_id in image_ids:

        list_file.write(imagespath+'/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    print(tmp)
    list_file.close()
