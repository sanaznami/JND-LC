# Copyright (c) 2021-2022, InterDigital Communications, Inc
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted (subject to the limitations in the disclaimer
# below) provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of InterDigital Communications, Inc nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.

# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import math

import torch
import torch.nn as nn

from pytorch_msssim import ms_ssim

from compressai.registry import register_criterion

import torchvision.models as models

@register_criterion("RateFWLDistortionLoss")
class RateFWLDistortionLoss(nn.Module):
    """Custom rate distortion loss with a Lagrangian parameter."""

    def __init__(self, lmbda=0.01, weight=0.9, metric="mse", return_type="all"):
        super().__init__()
        self.metric = metric
        if metric == "mse":
            self.metric = nn.MSELoss()
        elif metric == "ms-ssim":
            self.metric = ms_ssim
        else:
            raise NotImplementedError(f"{metric} is not implemented!")
        self.lmbda = lmbda
        self.return_type = return_type
        self.weight = weight
        
        # Initialize VGG16 model for feature extraction
        vgg16 = models.vgg16(pretrained=True)
        self.feature_extractor = nn.Sequential(*list(vgg16.features.children())[:-1])

        # Freeze the parameters in the feature extraction layers
        for param in self.feature_extractor.parameters():
            param.requires_grad_(False)

    def forward(self, output, target, jnd_target):
        N, _, H, W = target.size()
        out = {}
        num_pixels = N * H * W

        out["bpp_loss"] = sum(
            (torch.log(likelihoods).sum() / (-math.log(2) * num_pixels))
            for likelihoods in output["likelihoods"].values()
        )
        if self.metric == ms_ssim:
            out["ms_ssim_loss"] = self.metric(output["x_hat"], target, data_range=1)
            distortion1 = 1 - out["ms_ssim_loss"]
        else:
            out["mse_loss"] = self.metric(output["x_hat"], target)
            distortion1 = 255**2 * out["mse_loss"]
        
        # Ensure both input and weight tensors are on the same device
        output_x_hat = output["x_hat"]
        device = jnd_target.device
        output_x_hat = output_x_hat.to(device)
        
        # Ensure the feature extractor is on the same device
        self.feature_extractor.to(device)
        # Extract features from the VGG16 for both images
        predicted_features = self.feature_extractor(output_x_hat)
        jnd_features = self.feature_extractor(jnd_target)

        # Calculate Mean Squared Error (MSE) between the features
        MyMSEL = nn.MSELoss()
        distortion2 = MyMSEL(predicted_features, jnd_features)
        
        out["loss"] = self.lmbda * ((self.weight * distortion1) + ((1 - self.weight) * distortion2)) + out["bpp_loss"]

        if self.return_type == "all":
            return out
        else:
            return out[self.return_type]
