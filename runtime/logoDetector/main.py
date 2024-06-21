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
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

from ..logoDetector.mrcnn import utils
from ..logoDetector.mrcnn import visualize
from ..logoDetector.mrcnn.visualize import display_images
from ..logoDetector.mrcnn.visualize import display_instances
from ..logoDetector.mrcnn import model as modellib
from ..logoDetector.mrcnn.model import log
from ..logoDetector.mrcnn.config import Config
from ..logoDetector.mrcnn import model as modellib, utils

def loadLogoDetector():  
    LOGO_DETECT_ROOT_DIR = os.getcwd()
    LOGO_DETECT_ROOT_DIR = os.path.join(LOGO_DETECT_ROOT_DIR, 'runtime/logoDetector/')
    LOGO_DETECT_ROOT_DIR = os.path.normpath(LOGO_DETECT_ROOT_DIR)
    print("Working Dir: ", LOGO_DETECT_ROOT_DIR)

    LOGO_DETECT_DATASET_DIR = os.path.join(LOGO_DETECT_ROOT_DIR, 'Datasets/')
    LOGO_DETECT_DATASET_DIR = os.path.normpath(LOGO_DETECT_DATASET_DIR)
    print("Dataset Dir: ", LOGO_DETECT_DATASET_DIR)

    LOGO_DETECT_LOGS_DIR = os.path.join(LOGO_DETECT_ROOT_DIR, "trainingLogs")
    MODEL_PATH = os.path.join(LOGO_DETECT_ROOT_DIR, 'model.h5')

    LOGO_DETECT_GENERATED_PATH = os.path.join(LOGO_DETECT_ROOT_DIR, 'static/generated/order/')
    # COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "LogoDetectorModel/preTrainedModel/mask_rcnn_coco.h5")
    DEFAULT_LOGS_DIR = os.path.join(LOGO_DETECT_ROOT_DIR, "LogoDetectorModel/trainingLogs/sewez20240618T0707/trainingLogs")


    class TrainingConfig(Config):
        NAME = "sewez"
        IMAGES_PER_GPU = 1
        NUM_CLASSES = 1 + 3
        STEPS_PER_EPOCH = 5
        DETECTION_MIN_CONFIDENCE = 0.9
        LEARNING_RATE = 0.001
    class InferenceConfig(TrainingConfig):
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        DETECTION_MIN_CONFIDENCE = 0.7
        DETECTION_NMS_THRESHOLD = 0.3
    inference_config = InferenceConfig()
    model = modellib.MaskRCNN(mode="inference", 
                            config=inference_config,
                            model_dir=LOGO_DETECT_LOGS_DIR)
    print("Loading weights from: ", MODEL_PATH)
    model.load_weights(MODEL_PATH, by_name=True)
    model.load_weights(MODEL_PATH, by_name=True,exclude=[
                        "mrcnn_class_logits", "mrcnn_bbox_fc",
                        "mrcnn_bbox", "mrcnn_mask"])
    # model.keras_model._make_predict_function()
    class TrainingDataset(utils.Dataset):

        def load_training_dataset(self, LOGO_DETECT_DATASET_DIR, subset):
            self.add_class("sewez", 1, "sewez_tshirt")
            self.add_class("sewez", 2, "sewez_tshirt_logo")
            self.add_class("sewez", 3, "sewez_tshirt_brand")
            assert subset in ["train", "val"]
            LOGO_DETECT_DATASET_DIR = os.path.join(LOGO_DETECT_DATASET_DIR, subset)
            annotations = json.load(open(os.path.join(LOGO_DETECT_DATASET_DIR, "annotation.json")))
            annotations = list(annotations.values())
            annotations = [a for a in annotations if a['regions']]
            for a in annotations:
                if type(a['regions']) is dict:
                    polygons = [r['shape_attributes'] for r in a['regions'].values()]
                else:
                    polygons = [r['shape_attributes'] for r in a['regions']]
                objects = [s['region_attributes']['names'] for s in a['regions']]
                name_dict = {"sewez_tshirt": 1, "sewez_tshirt_logo": 2, "sewez_tshirt_brand": 3}
                num_ids = [name_dict[a] for a in objects]
                image_path = os.path.join(LOGO_DETECT_DATASET_DIR, a['filename'])
                image = skimage.io.imread(image_path)
                height, width = image.shape[:2]

                self.add_image(
                    "sewez",
                    image_id=a['filename'],
                    path=image_path,
                    width=width, height=height,
                    polygons=polygons,
                    num_ids=num_ids)

        def load_mask(self, image_id):
            image_info = self.image_info[image_id]
            if image_info["source"] != "sewez":
                return super(self.__class__, self).load_mask(image_id)
            info = self.image_info[image_id]
            if info["source"] != "sewez":
                return super(self.__class__, self).load_mask(image_id)
            num_ids = info['num_ids']
            mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                            dtype=np.uint8)
            for i, p in enumerate(info["polygons"]):
                rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
                mask[rr, cc, i] = 1
            num_ids = np.array(num_ids, dtype=np.int32)
            return mask, num_ids

        def image_reference(self, image_id):
            """Return the path of the image."""
            info = self.image_info[image_id]
            if info["source"] == "object":
                return info["path"]
            else:
                super(self.__class__, self).image_reference(image_id)
    # Training dataset.
    dataset_train = TrainingDataset()
    dataset_train.load_training_dataset(LOGO_DETECT_DATASET_DIR, "train")
    dataset_train.prepare()
    # Validation dataset
    dataset_val = TrainingDataset()
    dataset_val.load_training_dataset(LOGO_DETECT_DATASET_DIR, "val")
    dataset_val.prepare()
    return model, dataset_val

def intersect(boxA, boxB):
    # Compute intersection rectangle coordinates
    xA = max(boxA[1], boxB[1])
    yA = max(boxA[0], boxB[0])
    xB = min(boxA[3], boxB[3])
    yB = min(boxA[2], boxB[2])
    
    # Compute intersection area
    interWidth = max(0, xB - xA)
    interHeight = max(0, yB - yA)
    interArea = interWidth * interHeight
    
    return interArea > 0

def inferCalculateLogo(imagePath, savePath, model, dataset_val):
    img = skimage.io.imread(imagePath)
    img_arr = np.array(img)
    results = model.detect([img_arr], verbose=1)
    r = results[0]
    visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], 
                                dataset_val.class_names, r['scores'], figsize=(5,5), save_path=savePath)
    detection_result = []
    detected_tshirts = []
    detected_logos = []
    for rows, class_id in enumerate(r['class_ids']):
        detection_id = r['class_ids'][rows]
        detection_score = r['scores'][rows]
        detection_rois = r['rois'][rows].tolist()
        y1, x1, y2, x2 = r['rois'][rows]
        length = y2 - y1
        width = x2 - x1
        dimension = {
            "x": width,
            "y": length,
            "area": length * width,
            "maskArea": np.sum(r['masks'][:,:,rows])
            }
        detection = {
        "id": detection_id,
        "score": detection_score,
        "dimension": dimension,
        "roi": detection_rois,
        }
        detection_result.append(detection)
        if detection_id == 1:
            detected_tshirts.append(detection)
        elif detection_id == 2:
            detected_logos.append(detection)

    grouped_result = []
    for tShirt in detected_tshirts:
        # convert relative unit to cm
        tShirtHeightCM = 71
        ratioToCM = tShirtHeightCM/tShirt["dimension"]["y"]
        tShirtWidthCM = ratioToCM * tShirt["dimension"]["x"]
        tShirtAreaCM = tShirtHeightCM * tShirtWidthCM
        tShirtMaskAreaCM = (ratioToCM**2) * tShirt["dimension"]["maskArea"]
        tShirt['dimensionCM'] = {
            "x": tShirtWidthCM,
            "y": tShirtHeightCM,
            "area": tShirtAreaCM,
            "maskArea": tShirtMaskAreaCM
        }
        # List to keep track of logos intersecting with the tshirt
        associated_logos = []
        for logo in detected_logos:
            if intersect(tShirt["roi"], logo["roi"]):
                # convert relative unit to cm
                logoHieghtCM = ratioToCM * logo["dimension"]["y"]
                logoWidthCM = ratioToCM * logo["dimension"]["x"]
                logoAreaCM = logoHieghtCM * logoWidthCM
                logoMaskAreaCM = (ratioToCM**2) * logo["dimension"]["maskArea"]
                logo["dimensionCM"] = {
                    "x": logoWidthCM,
                    "y": logoHieghtCM,
                    "area": logoAreaCM,
                    "maskArea": logoMaskAreaCM
                }
                associated_logos.append(logo)
        tshirt_with_logos = {
            "tshirt": tShirt,
            "logos": associated_logos
        }
        grouped_result.append(tshirt_with_logos)
    detectionData = {
        "numberOfTshirt": len(detected_tshirts),
        "numberOfLogos": len(detected_logos),
        "data": grouped_result
    }   
    return detectionData

def calculateLogo(imagePath, savePath, model, dataset_val):
    data = inferCalculateLogo(imagePath=imagePath, savePath=savePath, model=model, dataset_val=dataset_val)
    logoData = data["data"]
    logoReformat = []
    for item in logoData:
        for logo in item['logos']:
            logoReformat.append({
                "x": logo['dimensionCM']['x'],
                "y": logo['dimensionCM']['y']
            })
    return {
        "error": False,
        "message": "Successfully calculated logo",
        "data": {
            "logo": logoReformat,
            "image": savePath
        }
    }
####################################################