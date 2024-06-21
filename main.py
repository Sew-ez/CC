import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
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
from runtime.logoDetector.mrcnn import utils
from runtime.logoDetector.mrcnn import visualize
from runtime.logoDetector.mrcnn.visualize import display_images
from runtime.logoDetector.mrcnn.visualize import display_instances
from runtime.logoDetector.mrcnn import model as modellib
from runtime.logoDetector.mrcnn.model import log
from runtime.logoDetector.mrcnn.config import Config
from runtime.logoDetector.mrcnn import model as modellib, utils
from typing import Union, Annotated
from fastapi import FastAPI, Response, Request, status, UploadFile, File, Header, Form
from fastapi.staticfiles import StaticFiles
from function.home import getHome
from function.order import getCart, getOrderForm, pushCart, pushOrder, getFabricTypeAll, getColorAll, addOrder, getLogoTypeAll
from function.auth import authLogin, authLogout, authRegister, authCheck, randomGenerator
from function.classes import RegistrationForm, OrderForm, LoginForm, LogoutForm, CartForm
# from runtime.logoDetector.main import loadLogoDetector, calculateLogo,inferCalculateLogo
from dotenv import load_dotenv
load_dotenv()

#################################################################
#                         LOAD MODEL                            #
#################################################################
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

async def inferCalculateLogo(imagePath, savePath, model, dataset_val):
    # savePath = os.path.join(os.getcwd(), "static/generated/order", saveName)
    # logoPath = os.path.join(os.getcwd(), "static/uploads/order", logoName)
    # imagePath = "/www/wwwroot/sewez/runtime/logoDetector/Datasets/test/3.jpg"
    savePath1 = "/www/wwwroot/sewez/runtime/logoDetector/3.jpg"
    img = skimage.io.imread(imagePath)
    img_arr = np.array(img)
    results = model.detect([img_arr], verbose=1)
    r = results[0]
    visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], 
                                dataset_val.class_names, r['scores'], figsize=(5,5), save_path=savePath1)
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
        print(ratioToCM)
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
    
    print(grouped_result)
    print("Terdeteksi", len(detected_tshirts), " Tshirt dan ", len(detected_logos), " Logo")
    detectionData = {
        "numberOfTshirt": len(detected_tshirts),
        "numberOfLogos": len(detected_logos),
        "data": grouped_result
    }   
    return await detectionData

def calculateLogo(imagePath, savePath, model, dataset_val):
    # data = inferCalculateLogo(logoName=logoName, saveName=saveName, model=model, dataset_val=dataset_val)
    data = inferCalculateLogo(imagePath=imagePath, savePath=savePath, model=model, dataset_val=dataset_val)
    print(data)
    # logoData = data["data"]
    # logoReformat = []
    # for item in logoData:
    #     for logo in item['logos']:
    #         logoReformat.append({
    #             "x": logo['dimensionCM']['x'],
    #             "y": logo['dimensionCM']['y']
    #         })
    return {
        "error": False,
        "message": "Successfully calculated logo",
        "data": {
            # "logo": logoReformat,
            "image": savePath
        }
    }
#
model, dataset_val = loadLogoDetector()
#################################################################
#                         START API                             #
#################################################################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#################################################################
#                              AUTH                             #
#################################################################
@app.post("/auth/login", status_code=200)
def login(response: Response, loginForm: LoginForm):
    return authLogin(loginForm=loginForm)

@app.get("/auth/logout", status_code=200)
def logout(request: Request, response: Response):
    return authLogout(request=request, response=response)

@app.post("/auth/register", status_code=200)
def register(response: Response, registrationform: RegistrationForm):
    return authRegister(response=response, registrationForm=registrationform)

@app.get("/auth/check", status_code=200)
def checkSession(request: Request, response: Response):
    sessionToken = str(request.headers.get("Authorization"))
    return authCheck(sessionToken)

#################################################################
#                           HOME PAGE                           #
#################################################################
@app.get("/home", status_code=200)
def home(request: Request, response: Response):
    return getHome(request=request, response=response)

#################################################################
#                            ORDERING                           #
#################################################################

@app.get("/order/jenis-bahan", status_code=200)
def fabricType(request: Request, response: Response):
    return getFabricTypeAll(request=request, response=response)

@app.get("/order/jenis-bahan-logo", status_code=200)
def logoType(request: Request, response: Response):
    return getLogoTypeAll(request=request, response=response)

@app.get("/order/warna", status_code=200)
def fabricColor(request: Request, response: Response):
    return getColorAll(request=request, response=response)

@app.post("/order/submit", status_code=200)
async def submitOrder(request: Request, response: Response, jenisproduk: Annotated[int, Form()], jenisbahan: Annotated[int, Form()], warna: Annotated[int, Form()], jenislogo: Annotated[int, Form()], xxl:Annotated[int, Form()], xl: Annotated[int, Form()], l: Annotated[int, Form()], m: Annotated[int, Form()], s: Annotated[int, Form()], image: UploadFile = File(...)):
    apiData = addOrder(request=request, response=response, jenisproduk=jenisproduk, jenisbahan=jenisbahan, warna=warna, jenislogo=jenislogo, xxl=xxl, xl=xl, l=l, m=m, s=s, image=image, model=model, dataset_val=dataset_val)
    return apiData