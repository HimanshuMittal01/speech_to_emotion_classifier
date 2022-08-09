## Speech to emotion classifier

## Setup

```zsh
$ git clone https://github.com/HimanshuMittal01/speech_to_emotion_classifier.git
$ cd speech_to_emotion_classifier/
$ python3 -m venv venv
$ source vevn/bin/activate
$ pip install -r requirements.txt
```

## Training code

In order to train the models, you need to download RAVDESS dataset - speech audio only.

Go through the following notebooks in order.
1. split_process_data.ipynb
2. train.ipynb
3. inference.ipynb

## How to run

```bash
$ sh run.sh
```

## Evaluation

Evaluated 3 models trained on RAVDESS dataset (excluding song audio).

Accuracy observed on 8 classes in train/validation/test datasets.
1. XGBoost: ~95% / ~41% / ~25%
2. LSTM (3 layers - 64-64-64): ~76% / ~46% / ~26%
3. CNN (3 layers - 32-64-128): ~93% / ~50% / ~30%

## Future work
- Improving accuracy of the speech models
    - By using extra training datasey, maybe including song set and other datasets
    - Cross validation
- Real time smooth animation of different faces
