import json
import os

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from version import get_image, get_version

app = FastAPI()

client = MongoClient(os.environ["MONGO_URI"])
db = client.mydatabase


@app.get("/health")
async def health():
    return {"status": "ok", "version": get_version(), "image": get_image()}


# The driver checks MongoDB in the background (every 10 s by default);
# this reads its latest result.
@app.get("/ready")
async def ready():
    if not client.topology_description.has_writable_server():
        return JSONResponse({"status": "not ready", "mongodb": "unreachable"}, 503)
    return JSONResponse({"status": "ok", "mongodb": "ok"})


@app.post("/store")
async def store(data: dict):
    result = db.mycollection.insert_one(data)
    return {"id": str(result.inserted_id)}


@app.get("/retrieve/{version_dict_id}")
async def retrieve(version_dict_id: str):
    result = db.mycollection.find_one({"_id": ObjectId(version_dict_id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    result["_id"] = str(result["_id"])
    return result
