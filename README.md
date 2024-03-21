<h1 align="center"> PERCEPTUAL LEARNED IMAGE COMPRESSION VIA END-TO-END JND-BASED OPTIMIZATION 


## Introduction

This is the implementation of [PERCEPTUAL LEARNED IMAGE COMPRESSION VIA END-TO-END JND-BASED OPTIMIZATION](https://arxiv.org/abs/2402.02836) paper in Pytorch.

## Acknowledgement

The framework is based on [CompressAI](https://github.com/InterDigitalInc/CompressAI). We modify ...........

**Abstract**

Emerging Learned image Compression (LC) achieves significant improvements in coding efficiency by end-to-end training of neural networks for compression. An important benefit of this approach over traditional codecs is that any optimization criteria can be directly applied to the encoder-decoder networks during training. Perceptual optimization of LC to comply with the Human Visual System (HVS) is among such criteria, which has not been fully explored yet. This paper addresses this gap by proposing a novel framework to integrate Just Noticeable Distortion (JND) principles into LC. Leveraging existing JND datasets, three perceptual optimization methods are proposed to integrate JND into the LC training process: (1) Pixel-Wise JND Loss (PWL) prioritizes pixel-by-pixel fidelity in reproducing JND characteristics, (2) Image-Wise JND Loss (IWL) emphasizes on overall imperceptible degradation levels, and (3) Feature-Wise JND Loss (FWL) aligns the reconstructed image features with perceptually significant features. Experimental evaluations demonstrate the effectiveness of JND integration, highlighting improvements in rate-distortion performance and visual quality, compared to baseline methods. The proposed methods add no extra complexity after training.


**The proposed framework**


![image](https://github.com/sanaznami/JND-LC/assets/59918141/54b0af4c-fe51-4037-a111-7107cfba6124)

<p align="center">The proposed learned image compression framework and JND-based perceptual loss functions. (a) overall framework. (b) Pixel-wise Loss (PWL). (c) Image-wise Loss (IWL). (d) Feature-wise Loss (FWL).


## Pre-trained Models
Our pre-trained models can be downloaded using this link.


## Dataset Structure
The dataset used for training and testing should have the following structure. Original images are stored in the "Ref" subfolder, while JND-quality images are located in the "JND1" subfolder.


    - rootdir/
         - train/
             - Ref/
                  - img#1
                  - ...             
             - JND1/
                  - img#1
                  - ...

         - test/
             - Ref/
                  - img#1
                  - ...             
             - JND1/
                  - img#1
                  - ...


	     



## Evaluation


## Train


## Citation

If our work is useful for your research, please cite our paper:


## Contact

If you have any question, leave a message here or contact Sanaz Nami (snami@ut.ac.ir, sanaz.nami@tuni.fi).


