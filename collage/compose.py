# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os, errno
import shutil
import importlib
import random
import asyncio
from itertools import zip_longest

import collage_maker


# %%
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


# %%
ROOT_DIR = "../media/myapp/static/myapp"
OUTPUT_DIR = "collages"
BATCH_SIZE = 8
EXCLUDE_NAMES = ('vendor', 'DP', 'admin', 'collages')
SHUFFLE_IMAGES = True


# %%
OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR)
os.makedirs(OUTPUT_PATH, exist_ok=True)


# %%
async def process_batch_images(images, output_path, name):
    images = filter(lambda file: file is not None, images)
    args = {
        'images': images,
        'width':850 ,
        'init_height':720,
        'output' : os.path.join(output_path, name+'.jpg')
    }
    collage_maker.prepare(**args)


# %%
async def process_dir(current_dir):
    print('=== Entering', current_dir, '===')
    name = os.path.basename(current_dir)
    output_path = os.path.join(OUTPUT_PATH, name)
    # Create output dir if not created
    os.makedirs(output_path, exist_ok=True)
    images = [os.path.join(current_dir, f) for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    # shuffle images if needed
    if SHUFFLE_IMAGES:
        random.shuffle(images)
    await asyncio.gather(*(process_batch_images(batch, output_path, str(i)) for i, batch in enumerate(grouper(images, BATCH_SIZE))))


# %%
async def main():
    dirs = (os.path.join(ROOT_DIR, f) for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f)) and f not in EXCLUDE_NAMES)
    await asyncio.gather(*(process_dir(current_dir) for current_dir in dirs))


# %%
importlib.reload(collage_maker)

asyncio.run(main())

