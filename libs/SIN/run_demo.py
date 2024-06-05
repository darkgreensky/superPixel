import argparse
import os
import torch.backends.cudnn as cudnn
from . import models
import torchvision.transforms as transforms
from . import flow_transforms
# import flow_transforms
from imageio import imread, imsave
from skimage import img_as_ubyte
# from scipy.misc import imsave
# from loss import *
from .loss import *

import time
import random
from glob import glob
from .models.model_util import update_spixel_map

import matplotlib.pyplot as plt

# import sys
# sys.path.append('../cython')
# from connectivity import enforce_connectivity


'''
Infer from custom dataset:
author:Fengting Yang 
last modification: Mar.5th 2020

usage:
1. set the ckpt path (--pretrained) and output
2. comment the output if do not need

results will be saved at the args.output

'''

# os.environ['CUDA_VISIBLE_DEVICES'] = '1'

model_names = sorted(name for name in models.__dict__
                     if name.islower() and not name.startswith("__"))

parser = argparse.ArgumentParser(description='PyTorch SPixelNet inference on a folder of imgs',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--data_dir', metavar='DIR', default='./libs/SIN/demo/inputs', help='path to images folder')
parser.add_argument('--data_suffix', default='jpg', help='suffix of the testing image')
parser.add_argument('--pretrained', metavar='PTH', help='path to pre-trained model',
                    default='./libs/SIN/pretrain_ckpt/300000_step.tar')
parser.add_argument('--output', metavar='DIR', default='./libs/SIN/demo', help='path to output folder')

parser.add_argument('--downsize', default=16, type=float, help='superpixel grid cell, must be same as training setting')

parser.add_argument('-nw', '--num_threads', default=1, type=int, help='num_threads')
parser.add_argument('-b', '--batch-size', default=1, type=int, metavar='N', help='mini-batch size')

args = parser.parse_args()

random.seed(100)


@torch.no_grad()
def test(args, model, img_paths, save_path, idx):
    # Data loading code
    input_transform = transforms.Compose([
        flow_transforms.ArrayToTensor(),
        transforms.Normalize(mean=[0, 0, 0], std=[255, 255, 255]),
        transforms.Normalize(mean=[0.411, 0.432, 0.45], std=[1, 1, 1])
    ])

    img_file = img_paths[idx]
    load_path = img_file
    imgId = os.path.basename(img_file)[:-4]

    # may get 4 channel (alpha channel) for some format
    img_ = imread(load_path)[:, :, :3]
    H, W, _ = img_.shape
    H_, W_ = int(np.ceil(H / 16.) * 16 - 15), int(np.ceil(W / 16.) * 16 - 15)

    img1 = cv2.resize(img_, (W_, H_), interpolation=cv2.INTER_CUBIC)
    img1 = input_transform(img1)
    ori_img = input_transform(img_)

    # compute output
    tic = time.time()
    prob0_v, prob0_h, prob1_v, prob1_h, prob2_v, prob2_h, prob3_v, prob3_h = model(
        img1.to(torch.device("cpu")).unsqueeze(0))
    toc = time.time() - tic

    # assign the spixel map
    curr_spixl_map = update_spixel_map(img1.to(torch.device("cpu")).unsqueeze(0), prob0_v, prob0_h, prob1_v, prob1_h,
                                       prob2_v, prob2_h, prob3_v, prob3_h)
    # curr_spixl_map = map0
    ori_sz_spixel_map = F.interpolate(curr_spixl_map.type(torch.float), size=(H_, W_), mode='nearest').type(torch.int)

    mean_values = torch.tensor([0.411, 0.432, 0.45], dtype=img1.to(torch.device("cpu")).unsqueeze(0).dtype).view(3, 1,
                                                                                                                 1)
    spixel_viz, spixel_label_map = get_spixel_image((ori_img + mean_values).clamp(0, 1), ori_sz_spixel_map.squeeze(),
                                                    n_spixels=0, b_enforce_connect=False)

    # ************************ Save all result********************************************
    # save img, uncomment it if needed
    # if not os.path.isdir(os.path.join(save_path, 'img')):
    #     os.makedirs(os.path.join(save_path, 'img'))
    # spixl_save_name = os.path.join(save_path, 'img', imgId + '.jpg')
    # img_save = (ori_img + mean_values).clamp(0, 1)
    # imsave(spixl_save_name, img_save.detach().cpu().numpy().transpose(1, 2, 0))

    # save spixel viz
    if not os.path.isdir(os.path.join(save_path, 'spixel_viz')):
        os.makedirs(os.path.join(save_path, 'spixel_viz'))
    spixl_save_name = os.path.join(save_path, 'spixel_viz', imgId + '_sPixel.png')
    imsave(spixl_save_name, spixel_viz.transpose(1, 2, 0))

    # save the unique maps as csv, uncomment it if needed
    if not os.path.isdir(os.path.join(save_path, 'map_csv')):
        os.makedirs(os.path.join(save_path, 'map_csv'))
    output_path = os.path.join(save_path, 'map_csv', imgId + '.csv')
    # plus 1 to make it consistent with the toolkit format
    np.savetxt(output_path, spixel_label_map.astype(int), fmt='%i', delimiter=",")
    print(spixel_label_map)

    if idx % 10 == 0:
        print("processing %d" % idx)

    return toc


def main():
    global args, save_path
    data_dir = args.data_dir
    print(data_dir)
    print("=> fetching img pairs in '{}'".format(data_dir))

    save_path = args.output
    print('=> will save everything to {}'.format(save_path))
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    tst_lst = glob(args.data_dir + '/*.' + args.data_suffix)
    print("tst:", (args.data_dir + '/*.' + args.data_suffix))
    tst_lst.sort()

    if len(tst_lst) == 0:
        print('Wrong data dir or suffix!')
        exit(1)

    print('{} samples found'.format(len(tst_lst)))

    # create model
    network_data = torch.load(args.pretrained, map_location=torch.device('cpu'), weights_only=True)
    print("=> using pre-trained model '{}'".format(network_data['arch']))
    model = models.__dict__[network_data['arch']](data=network_data).to(torch.device("cpu"))
    model.eval()
    args.arch = network_data['arch']
    cudnn.benchmark = True

    mean_time = 0
    for n in range(len(tst_lst)):
        time = test(args, model, tst_lst, save_path, n)
        mean_time += time
    print("avg_time per img: %.3f" % (mean_time / len(tst_lst)))


@torch.no_grad()
def test_1(args, model, img):
    # Data loading code
    input_transform = transforms.Compose([
        flow_transforms.ArrayToTensor(),
        transforms.Normalize(mean=[0, 0, 0], std=[255, 255, 255]),
        transforms.Normalize(mean=[0.411, 0.432, 0.45], std=[1, 1, 1])
    ])

    if img.shape[2] == 4:
        # 图像有 4 个通道（RGBA），需要转换为 RGB
        img_rgb = img[:, :, :3]
    elif img.shape[2] == 3:
        # 图像已经是 RGB 格式
        img_rgb = img
    elif img.shape[2] == 1:
        # 图像是灰度图，将其转换为 RGB 格式
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        raise ValueError("Unexpected number of channels in the image")
    img_ = img_rgb

    # img_file = img_paths[idx]
    # load_path = img_file
    # imgId = os.path.basename(img_file)[:-4]

    # may get 4 channel (alpha channel) for some format
    # img_ = imread(load_path)[:, :, :3]
    H, W, _ = img_.shape
    H_, W_ = int(np.ceil(H / 16.) * 16 - 15), int(np.ceil(W / 16.) * 16 - 15)

    img1 = cv2.resize(img_, (W_, H_), interpolation=cv2.INTER_CUBIC)
    img1 = input_transform(img1)
    ori_img = input_transform(img_)

    # compute output
    tic = time.time()
    prob0_v, prob0_h, prob1_v, prob1_h, prob2_v, prob2_h, prob3_v, prob3_h = model(
        img1.to(torch.device("cpu")).unsqueeze(0))
    toc = time.time() - tic

    # assign the spixel map
    curr_spixl_map = update_spixel_map(img1.to(torch.device("cpu")).unsqueeze(0), prob0_v, prob0_h, prob1_v, prob1_h,
                                       prob2_v, prob2_h, prob3_v, prob3_h)
    # curr_spixl_map = map0
    ori_sz_spixel_map = F.interpolate(curr_spixl_map.type(torch.float), size=(H_, W_), mode='nearest').type(torch.int)

    mean_values = torch.tensor([0.411, 0.432, 0.45], dtype=img1.to(torch.device("cpu")).unsqueeze(0).dtype).view(3, 1,
                                                                                                                 1)
    spixel_viz, spixel_label_map = get_spixel_image((ori_img + mean_values).clamp(0, 1), ori_sz_spixel_map.squeeze(),
                                                    n_spixels=0, b_enforce_connect=False)
    # print("SIN successfully")
    # ************************ Save all result********************************************
    # save img, uncomment it if needed
    # if not os.path.isdir(os.path.join(save_path, 'img')):
    #     os.makedirs(os.path.join(save_path, 'img'))
    # spixl_save_name = os.path.join(save_path, 'img', imgId + '.jpg')
    # img_save = (ori_img + mean_values).clamp(0, 1)
    # imsave(spixl_save_name, img_save.detach().cpu().numpy().transpose(1, 2, 0))

    # save spixel viz
    # if not os.path.isdir(os.path.join(save_path, 'spixel_viz')):
    #     os.makedirs(os.path.join(save_path, 'spixel_viz'))
    # spixl_save_name = os.path.join(save_path, 'spixel_viz', imgId + '_sPixel.png')
    # imsave(spixl_save_name, spixel_viz.transpose(1, 2, 0))
    #
    # # save the unique maps as csv, uncomment it if needed
    # if not os.path.isdir(os.path.join(save_path, 'map_csv')):
    #     os.makedirs(os.path.join(save_path, 'map_csv'))
    # output_path = os.path.join(save_path, 'map_csv', imgId + '.csv')
    #   # plus 1 to make it consistent with the toolkit format
    # np.savetxt(output_path, spixel_label_map.astype(int), fmt='%i',delimiter=",")
    # opencv_image = cv2.cvtColor(spixel_viz.transpose(1, 2, 0), cv2.COLOR_RGB2BGR)


    opencv_image = spixel_viz.transpose(1, 2, 0)

    if opencv_image.dtype == np.float32 or opencv_image.dtype == np.float64:
        # 假设浮点数在 0.0 到 1.0 范围内
        opencv_image_uint8 = (opencv_image * 255).astype(np.uint8)
        # print(f"Converted dtype: {opencv_image_uint8.dtype}")
    else:
        opencv_image_uint8 = opencv_image

    return opencv_image_uint8, spixel_label_map, toc


def SIN_handle(img):
    global args, save_path
    # data_dir = args.data_dir
    # print("=> fetching img pairs in '{}'".format(data_dir))
    #
    # save_path = args.output
    # print('=> will save everything to {}'.format(save_path))
    # if not os.path.isdir(save_path):
    #     os.makedirs(save_path)

    # tst_lst = glob(args.data_dir + '/*.' + args.data_suffix)
    # tst_lst.sort()

    # if len(tst_lst) == 0:
    #     print('Wrong data dir or suffix!')
    #     exit(1)
    #
    # print('{} samples found'.format(len(tst_lst)))

    # create model
    network_data = torch.load(args.pretrained, map_location=torch.device('cpu'), weights_only=True)
    # print("=> using pre-trained model '{}'".format(network_data['arch']))
    model = models.__dict__[network_data['arch']](data=network_data).to(torch.device("cpu"))
    model.eval()
    args.arch = network_data['arch']
    cudnn.benchmark = True

    mean_time = 0
    return test_1(args, model, img)
    # for n in range(len(tst_lst)):
    #     time = test(args, model, tst_lst, save_path, n)
    #     mean_time += time
    # print("avg_time per img: %.3f" % (mean_time / len(tst_lst)))


if __name__ == '__main__':
    main()
