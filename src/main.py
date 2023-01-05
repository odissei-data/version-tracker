import json
import os

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

client = MongoClient(os.environ["MONGO_URI"])
db = client.mydatabase


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
