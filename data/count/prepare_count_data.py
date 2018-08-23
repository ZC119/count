import os
import os.path as osp
import re
import random

devkit_dir = './count/data/count/count/'


def get_dir(devkit_dir, type):
    return osp.join(devkit_dir, type)


def walk_dir(devkit_dir):
    annotation_dir = get_dir(devkit_dir, 'bbox')
    img_dir = get_dir(devkit_dir, 'bbox_image')
    trainval_list = []
    test_list = []
    
    files = os.listdir(img_dir)

    files.remove('label_list')

    random.shuffle(files)
    test_num = len(files) * 0.1

    i = 0
    for fname in files:    
        name_prefix = fname[:-4]

        ann_path = osp.join(annotation_dir, name_prefix + '.txt')
        img_path = osp.join(img_dir, name_prefix + '.jpg')
        try:
            os.path.isfile(img_path)
        except:
            img_path = osp.join(img_dir, name_prefix + '.png')
        
        assert os.path.isfile(ann_path), 'file %s not found.' % ann_path
        assert os.path.isfile(img_path), 'file %s not found.' % img_path
        
        if i < test_num:
            test_list.append([img_path, ann_path])
        else:
            trainval_list.append([img_path, ann_path])
        i += 1
    return trainval_list, test_list


def prepare_filelist(devkit_dir, output_dir):
    trainval_list = []
    test_list = []
    trainval_list, test_list = walk_dir(devkit_dir)
    random.shuffle(trainval_list)
    random.shuffle(test_list)
    with open(osp.join(output_dir, 'trainval.txt'), 'w') as ftrainval:
        for item in trainval_list:
            ftrainval.write(item[0] + ' ' + item[1] + '\n')

    with open(osp.join(output_dir, 'test.txt'), 'w') as ftest:
        for item in test_list:
            ftest.write(item[0] + ' ' + item[1] + '\n')
    
    files = os.listdir(osp.join(devkit_dir, 'test'))

    files.remove('label_list')

    files = sorted(files, key=lambda x: int(x[:-4]))

    file_names = []

    for file in files:
        file_name = os.path.join(devkit_dir, 'test', file)
        file_names.append(file_name)

    with open('infer.txt', 'w') as f:
        for file_name in file_names:
            f.write(file_name + '\n')

prepare_filelist(devkit_dir, './count/data/count/')
