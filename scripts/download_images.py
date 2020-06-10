from fastai.vision import download_images, verify_images
from fastai.imports import *

classes = ['grass','dandelion']
path = Path('/usr/local/airflow/data')
folder = 'grass'
file = 'grass.csv'
dest = path/folder
dest.mkdir(parents=True, exist_ok=True)
download_images(path/file, dest, max_pics=200)
folder = 'dandelion'
file = 'dandelion.csv'
dest = path/folder
dest.mkdir(parents=True, exist_ok=True)
download_images(path/file, dest, max_pics=200)

for c in classes:
    print(c)
    verify_images(path/c, delete=True, max_size=500)
