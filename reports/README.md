## Results

8 labels as it is -> stratify split (70/22/8) on label+actorid -> mfcc -> standardize/normalize -> c-major flatten -> xgboost -> ~42% validation accuracy
8 labels as it is -> stratify split (70/22/8) on label+actorid -> mfcc -> standardize/normalize -> lstm -> ~38% validation accuracy
16 labels (bifuracate labels by gender) -> stratify split (70/22/8) on label -> mfcc -> standardize/normalize -> c-major flatten -> xgboost -> ~41% validation accuracy
16 labels (bifuracate labels by gender) -> stratify split (70/22/8) on label -> mfcc -> standardize/normalize -> lstm -> ~45% validation accuracy