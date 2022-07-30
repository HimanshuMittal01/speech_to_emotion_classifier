'''
 @author    : Himanshu Mittal
 @contact   : https://www.linkedin.com/in/himanshumittal13/
 @created on: 30-07-2022 10:59:09
'''

import os, json
import joblib
import numpy as np
import librosa.core

# Import config
with open("config.json", "r") as f:
    config = json.load(f)

# Import model
model = joblib.load(config["model_file"])

# Load audio
X,_ = librosa.core.load(config.get("input_audio_file"), sr=22050*2, offset=0.25, duration=2.5)

# Preprocess audio
X = librosa.feature.mfcc(y=X)
X = 2.*(X - X.min(axis=1).reshape(-1,1))/(X.max(axis=1)-X.min(axis=1)).reshape(-1,1) - 1
X = np.array([X.ravel()], dtype=np.float32)

# Predict emotion
y_pred = model.predict(X)

# Get meaningful format
id2emotion = {
    0: "neutral",
    1: "calm",
    2: "happy",
    3: "sad",
    4: "angry",
    5: "fearful",
    6: "disgust",
    7: "surprised"
}
emotion = {id2emotion[i]:0.0 for i in range(8)}
emotion[id2emotion[y_pred[0]]] = 1.0

# Save output
with open(config["output_json_file"], "w") as f:
    json.dump(emotion, f)
