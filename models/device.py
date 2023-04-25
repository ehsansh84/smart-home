from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, root_validator

from tools.log_tools import log
from publics import exception_line, serialize_dict, serialize_list, db
# from settings import db
# from .enums import ClusterConst, NodeConst

module_name = 'zone'


class Write(BaseModel):
    f"""
    Use this model to create a {module_name}
    """
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    name: str = Field(description="", example="")
    token: str = Field(description="", example="")
    action: str = Field(description="", example="")
    value: str = Field(description="", example="")
    model: str = Field(description="", example="")

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


class Read(BaseModel):
    f"""
    Use this model to create a {module_name}
    """
    id: str
    created_at: None | str
    updated_at: None | str
    name: str = Field(description="", example="")
    token: str = Field(description="", example="")
    action: str = Field(description="", example="")
    value: str = Field(description="", example="")
    model: str = Field(description="", example="")


class Update(BaseModel):
    f"""
    Use this model to create a {module_name}
    """
    name: str = Field(description="", example="")
    token: str = Field(description="", example="")
    action: str = Field(description="", example="")
    value: str = Field(description="", example="")
    model: str = Field(description="", example="")


ListRead = List[Read]


def insert(item):
    try:
        col = db()[module_name]
        return col.insert_one(jsonable_encoder(item)).inserted_id
    except Exception as e:
        log.error(f'Error: {exception_line()} {str(e)}')


def update(_id, item):
    try:
        col = db()[module_name]
        update_doc = {k: v for k, v in item if v is not None}
        result = col.update_one({"_id": ObjectId(_id)}, {"$set": update_doc})
        return result.raw_result
    except Exception as e:
        log.error(f'Error: {exception_line()} {str(e)}')


def delete(_id):
    try:
        col = db()[module_name]
        result = col.delete_one({"_id": ObjectId(_id)})

        return result.raw_result
    except Exception as e:
        log.error(f'Error: {exception_line()} {str(e)}')


def get_one(_id):
    try:
        col = db()[module_name]
        result = col.find_one({'_id': ObjectId(_id)})
        return serialize_dict(result)
    except Exception as e:
        log.error(f'Error: {exception_line()} {str(e)}')


def get(query={}):
    try:
        col = db()[module_name]
        return serialize_list(col.find(query))
    except Exception as e:
        log.error(f'Error: {exception_line()} {str(e)}')
