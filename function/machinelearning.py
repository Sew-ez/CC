from runtime.logoDetector.inference import calculateLogo as inferCalculateLogo

def calculateLogo(imagePath, savePath, model, dataset_val):
    data = inferCalculateLogo(imagePath=imagePath, savePath=savePath, model=model, dataset_val=dataset_val)
    # inferCalculateLogo(imagePath=imagePath, savePath=savePath, model=model, dataset_val=dataset_val)
    logoData = data["data"]
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
            "logo": logoData,
            # "image": savePath
        }
    }
