############ Project Paths ############
# This is a nice way to collaborate while
# letting everyone have their own paths.
# Add your path to the list.
#######################################

import os
from os import path
import sys

# Add your path here, if required.
use_local_folder = False
user_paths = [
    # platform, user, full_path
    ('win32', 'ahmad', "G:\\Shared drives\\usc-projects\\webrtc-mobility\\data"),  # ahmad windows home machine
]

proj_dir = path.abspath(path.join(path.dirname(__file__), os.pardir))
sys.path.append(proj_dir)

data_dir = path.join(proj_dir, 'data')
remote_data_processed_dir = ""
if not use_local_folder:
    for platform, user, full_path in user_paths:
        if platform == sys.platform and user == os.getlogin():
            data_dir = full_path
            remote_data_processed_dir = path.join(path.dirname(full_path), 'data-processed')
            break

data_processed_dir = path.join(proj_dir, 'data-processed')
plot_dir = path.join(proj_dir, 'plots')
utils_dir = path.join(proj_dir, 'utils')
