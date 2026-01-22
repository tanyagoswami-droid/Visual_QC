from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="pHYBnZ6WCzob0qIIdLoU"
)

result = client.run_workflow(
    workspace_name="tanya-goswami-7v2yh",
    workflow_id="find-scratches-2",
    images={
        "image": "lupl00207_1.jpg"   # path to your image
    },
    use_cache=True
)

preds = result[0]["predictions"]["predictions"]

found=False
for p in preds:
    print({
        "class": p["class"],
        "confidence": round(p["confidence"], 3),
        "width": round(p["width"], 2)
    })
    found=True
if not found:
    print("No defects found")




