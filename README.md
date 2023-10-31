# 3D Images Denoising with Unpaired Reference Image
This project descibes the codes for 3D C-scan data corss-sectional profile denosing model training program.

The each cross-sectional images are denoised in the following step
1. Tradtional compution vision denosing
2. Deap learning-based denosing

## Dataset Format

### Dataset for initial denoising process
3D dataset
```
./[your own path]/3D_dataset
----/train   % Training 3D data files [bin]
--------/20210315_102747C.bin
--------/20210412_111018C.bin
--------/1_20180326_111332_foot.png
----/test    % Testing 3D data files [bin]
--------/20210115_145149C.bin
```

2D processed dataset
```
./[your own path]/2D_dataset
----/train % Training 2D data files [png]
--------/vertical   
------------/20210315_102747C_0000_1.png
------------/20210315_102747C_0000_2.png
--------/horizontal 
------------/20210315_102747C_0000_1.png
------------/20210315_102747C_0000_2.png
----/test  % Testing 2D data files [png]
--------/horizontal 
------------/20210315_102747C_0000_1.png
------------/20210315_102747C_0000_2.png
--------/horizontal 
------------/20210315_102747C_0000_1.png
------------/20210315_102747C_0000_2.png
```

## Installation

* Clone this repo:
```
git clone https://github.com/tomohiroliu22/s3D-Images-Denoising-with-Unpaired-Reference
cd 3D-Images-Denoising-with-Unpaired-Reference
```

### Dataset for deep learning model denoising process
To build up this dataset, you may pick 2D B-scan (high quality reference) images as the A domain, and choose C-sacn cross-sectional profiles (low quality) as the B-domain. Therefore, you may need to pick the images from `./2D_dataset/train` and `./2D_dataset/test`, and assign them to `./DL_dataset/trainB`  and `./DL_dataset/testB`, respectively.

```
./[your own path]/DL_dataset
----/trainA % B-scan training images (2D) [png]
----/trainB % C-scan training images (2D) [png]
----/testA  % B-scan testing images (2D) [png]
----/testB  % C-scan testing images (2D) [png]
```


## Tradtional Computer Vision Denoising
* Training set
```
python preprocess.py --dataroot ./[your own path]/3D_dataset/train --saveroot ./[your own path]/2D_dataset/train
```

* Testing set
```
python preprocess.py --dataroot ./[your own path]/3D_dataset/test --saveroot ./[your own path]/2D_dataset/test
```

## Deep Leanring Denoising with Unpaired Reference
The project is modified from

> junyanz/pytorch-CycleGAN-and-pix2pix
> Link: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix

### Overview
* Model Training: Trained with A domain images, where the noise is extracted from B domain images.
* Model Testing: Infer on B domain images, and the model would output the denoised B domain images.

### Model Training

```
python train.py --dataroot ./[your own path]/DL_dataset --name [your own model name] --model 'pix2pix' --netG 'unet_128' --batch_size 1 --n_epochs 10 --lr 0.0002 --gan_mode 'lsgan' 
```

### Model Testing

```
python test.py --dataroot ./[your own path]/DL_dataset --name [your own model name] --model 'pix2pix' --netG 'unet_128' --num_test [number of evaluation testing images] --epoch 'latest'
```

### Checkpoint and Result

During the training process, the training process and details are recorded in the directory
```
./[your own path]/checkpoints
```

During the testing process, the testing result and details are recorded in the directory
```
./[your own path]/results
```
