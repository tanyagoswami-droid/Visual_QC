from fastapi import FastAPI, UploadFile, Form
import requests
import shutil
import os

app = FastAPI()

API_URL = "https://api-gateway.juno.lenskart.com/v2/products/product/internal/all-images/"

HEADERS = {
    "X-Api-Client": "desktop",
    "Accept": "application/json",
    "Cookie": "__cf_bm=ZzO9DVmTLe1OrRIQvIGhognFMdw9hUvlbLzna72dW7s-1768994792-1.0.1.1-HoADQb3KfAZGnzR4s3Th4iXvpKStZpU4ZHB006xvo.XNlw4OTmXpgw_yYTpZ3lJtkddFPHOFaDId8Ey_x2iOAvFrIumlMEc6an2Od9TLOT4"
}

os.makedirs("warehouse_images", exist_ok=True)
os.makedirs("reference_images", exist_ok=True)

@app.post("/upload")
async def upload_image(
    product_id: str = Form(...),
    warehouse_image: UploadFile = Form(...)
):
    # 1. Save warehouse image
    warehouse_path = f"warehouse_images/{product_id}.jpg"
    with open(warehouse_path, "wb") as f:
        shutil.copyfileobj(warehouse_image.file, f)

    # 2. Call product image API
    response = requests.get(API_URL + product_id, headers=HEADERS)
    data = response.json()

    # 3. Extract first reference image URL
    ref_url = data["result"]["imageUrls"][0]

    # 4. Download reference image
    ref_image = requests.get(ref_url).content
    ref_path = f"reference_images/{product_id}.jpg"
    with open(ref_path, "wb") as f:
        f.write(ref_image)

    return {
        "status": "success",
        "product_id": product_id,
        "warehouse_image_saved": warehouse_path,
        "reference_image_saved": ref_path
    }

