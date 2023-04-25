from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
from models.device import Write, Read, Update, ListRead
from fastapi.encoders import jsonable_encoder

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

app = FastAPI()


# Create operation
@app.post("/items/")
async def create_item(item: Write):
    result = collection.insert_one(jsonable_encoder(item))
    return {"id": str(result.inserted_id)}


# Read operation
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    result = collection.find_one({"_id": ObjectId(item_id)})
    return result


# Update operation
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Update):
    result = collection.replace_one({"_id": ObjectId(item_id)}, jsonable_encoder(item))
    return {"modified_count": result.modified_count}


# Delete operation
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    return {"deleted_count": result.deleted_count}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)