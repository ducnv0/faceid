#!/bin/bash
# pre-download models from https://github.com/serengil/deepface_models/releases
weights_dir=~/.deepface/weights/
mkdir -p ${weights_dir}
cd ${weights_dir}
wget https://github.com/serengil/deepface_models/releases/download/v1.0/facenet_weights.h5
