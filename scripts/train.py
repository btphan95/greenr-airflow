from fastai.vision import Path, ImageDataBunch, cnn_learner, get_transforms, imagenet_stats, models, error_rate
import numpy as np

path = Path('/usr/local/airflow/data')
np.random.seed(42)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, num_workers=0).normalize(imagenet_stats)

learn = cnn_learner(data, models.resnet34, metrics=error_rate)
learn.fit_one_cycle(4)
learn.save('stage-1')
learn.export()
