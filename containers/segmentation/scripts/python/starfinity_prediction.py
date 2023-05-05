#!/usr/bin/env python

import numpy as np
from tifffile import imsave
from csbdeep.utils import normalize
from stardist.models import StarDist3D
import argparse, sys, z5py


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i','--input', type=str, help = "z5 input directory")
    parser.add_argument('-m','--model', type=str, help = "model directory")
    parser.add_argument('-o','--output', type=str, help = "output file")
    parser.add_argument('-c','--channel', type=str, help = "channel")
    parser.add_argument('-s','--scale', type=str, help = "scale")
    
    args = parser.parse_args()
    
    print("reading ...", args.input, args.channel + '/' + args.scale)
    im = z5py.File(args.input, use_zarr_format=False)
    img = im[args.channel + '/' + args.scale][:, :, :]
    
    n_tiles = tuple(int(np.ceil(s/128)) for s in img.shape)
    print("estimated tiling:", n_tiles)

    print("normalizing input...")
    img_normed = normalize(img, 4, 99.8)

    
    model = StarDist3D(None, name=args.model, basedir=args.model)

    
    print("predicting...")
    # the affinity based labels 
    label_starfinity, res_dict = model.predict_instances_big(img_normed, block_size=(512,1024,1024),min_overlap=(96,96,96), affinity=True, affinity_thresh=0.1, n_tiles=n_tiles, candidate_grid=2, verbose=True)
    # the normal stardist labels are implicitly calculated and
    # can be accessed from the results dict
    label_stardist = res_dict["markers"]

    print("saving...")
    
    imsave(args.output, label_starfinity, compress=3)
    
    print("done")
