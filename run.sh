#!/bin/sh

# TODO: Pass config file as argument (internally)

# Run prediction
python predict.py

# Generate scene
blender --background --python generate.py

# Acknowledge
echo "DONE !!!"