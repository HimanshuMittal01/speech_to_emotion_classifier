'''
 @author    : Himanshu Mittal
 @contact   : https://www.linkedin.com/in/himanshumittal13/
 @created on: 30-07-2022 10:59:09
'''

import os, json
import torch
import joblib
import numpy as np
import librosa.core
from sklearn.preprocessing import StandardScaler
from src.lstm_model import lstm_model
from src.cnn_model import cnn_model

# Import config
with open("config.json", "r") as f:
    config = json.load(f)

# Import model
if config["model_name"]=="xgboost":
    xgb_model = joblib.load(config["model_file"])
elif config["model_name"]=="lstm":
    lstm_model.load_state_dict(torch.load(config["model_file"]))
elif config["model_name"]=="cnn":
    cnn_model.load_state_dict(torch.load(config["model_file"]))

# Read streaming audio
# 110250 samples in 2.5s at 44100 sample rate
X = librosa.core.stream(config.get("input_audio_file"), block_length=1, frame_length=110250, hop_length=22050, fill_value=0)

def get_mfcc_features(signal, postfeatures="standardize", return_dims=1):
    assert(postfeatures in ["standardize","normalize"])
    assert(return_dims in [1,2])

    # Get MFCC
    x = librosa.feature.mfcc(y=signal)

    # Postprocess
    if postfeatures=="standardize":
        x = StandardScaler().fit_transform(x.T).T
    elif postfeatures=="normalize":
        x = 2.*(x - x.min(axis=1).reshape(-1,1))/(x.max(axis=1)-x.min(axis=1)).reshape(-1,1) - 1
    
    # Return
    return x.ravel() if return_dims==1 else x

# predict emotions
output = {}
for idx, x in enumerate(X):
    if config["model_name"]=="xgboost":
        x = get_mfcc_features(x, postfeatures="standardize", return_dims=1)
        x = np.expand_dims(x, axis=0)
        y_pred = xgb_model.predict(x)[0]
        y_pred = [1.0 if i==y_pred else 0.0 for i in range(16)]

    elif config["model_name"]=="lstm":
        x = get_mfcc_features(x, postfeatures="standardize", return_dims=2).T
        y_pred = lstm_model(torch.tensor(x).unsqueeze(axis=0))
        y_pred = torch.nn.functional.softmax(y_pred, dim=1)[0]
        y_pred = y_pred.cpu().detach().numpy()

    elif config["model_name"]=="cnn":
        x = librosa.feature.melspectrogram(y=x, sr=44100, n_fft=1380, hop_length=345)/255.
        y_pred = cnn_model(torch.tensor(x).unsqueeze(axis=0).unsqueeze(axis=1))
        y_pred = torch.nn.functional.softmax(y_pred, dim=1)[0]
        y_pred = y_pred.cpu().detach().numpy()

    output[idx] = list(map(float, y_pred))

# Save output
with open(config["output_json_file"], "w") as f:
    json.dump(output, f)
