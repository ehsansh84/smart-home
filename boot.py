from fastapi import FastAPI
import os
import uvicorn
from enum import Enum
from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from publics import db
from models.device import Write, Read, ListRead, Update
from models.general import OutputCreate, OutputOnlyNote
from bson import ObjectId
from publics import serialize_list, serialize_dict, exception_line
from datetime import datetime



# def db():
#     from pymongo import MongoClient
#     con = MongoClient(MONGO_URL, connectTimeoutMS=1000)
#     return con['smart']


app = FastAPI()

router = APIRouter(
    prefix="/device",
    tags=['Device']
)

col = db()['device']

module_text = 'device'


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_device(item: Write):
    _id = col.insert_one(jsonable_encoder(item)).inserted_id
    return {
        'detail': f'{module_text} successfully created.',
        'data': {
            'id': str(_id)
        }
    }


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=OutputOnlyNote)
async def update_device(_id, item: Update):
    update_doc = {k: v for k, v in item if v is not None}
    result = col.update_one({"_id": ObjectId(_id)}, {"$set": update_doc})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Cluster {item.name} not found!',
        )
    return {"detail": f"{module_text} successfully updated."}


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=OutputOnlyNote)
async def delete_device(_id):
    result = col.delete_one({"_id": ObjectId(_id)})
    if result['n'] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{module_text} with id {_id} not found!',
        )
    return {'detail': f'{module_text} successfully deleted.'}


@router.get("/", response_description="List all clusters", response_model=ListRead)
async def list():
    data = col.find()
    return serialize_list(data)


@router.get("/{id}", response_description="Show a cluster", response_model=Read)
async def get_one(_id):
    data = col.find_one({'_id': ObjectId(_id)})
    return serialize_dict(data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)