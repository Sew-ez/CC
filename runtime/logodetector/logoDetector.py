import warnings
warnings.filterwarnings('ignore')
import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import cv2
import random
import math
import re
import time
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

from ..LogoDetectorModel.mrcnn import utils
from ..LogoDetectorModel.mrcnn import visualize
from ..LogoDetectorModel.mrcnn.visualize import display_images
from ..LogoDetectorModel.mrcnn.visualize import display_instances
from ..LogoDetectorModel.mrcnn import model as modellib
from ..LogoDetectorModel.mrcnn.model import log
from ..LogoDetectorModel.mrcnn.config import Config
from ..LogoDetectorModel.mrcnn import model as modellib, utils

# Root directory of the project
#ROOT_DIR = "D:\MRCNN_tensorflow2.7_env\Mask-RCNN"
ROOT_DIR = os.getcwd()
ROOT_DIR = os.path.normpath(ROOT_DIR)
print("Working Dir: ", ROOT_DIR)
DATASET_DIR = os.path.join(ROOT_DIR, 'Datasets/logoDetector/')
DATASET_DIR = os.path.normpath(DATASET_DIR)
print("Dataset Dir: ", DATASET_DIR)

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library


# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "LogoDetectorModel/preTrainedModel/mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "LogoDetectorModel/trainingLogs/sewez20240618T0707/trainingLogs")
