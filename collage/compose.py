# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os, errno
import shutil
import importlib

import collage_maker


# %%
ROOT_DIR = "../media/myapp/static/myapp"
OUTPUT_DIR = "collages"
BATCH_SIZE = 8
EXCLUDE_NAMES = ('vendor', 'DP', 'admin')


# %%
dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f)) and f not in EXCLUDE_NAMES]
dirs = [os.path.join(ROOT_DIR, name) for name in dirs]
print(dirs)

OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR)
os.makedirs(OUTPUT_PATH, exist_ok=True)


# %%
importlib.reload(collage_maker)

for current_dir in dirs:
    name = os.path.basename(current_dir)
    print('=== Entering', current_dir, '===')
    args = {
        'folder':current_dir,
        'width':850 ,
        'init_height':720,
        'shuffle' : True ,
        'output' : os.path.join(OUTPUT_PATH, name+'.jpg')
    }
    # img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    collage_maker.prepare(**args)

