from pydantic import (
    BaseModel,
    confloat
)
from typing import Union, List, Any
from enum import Enum 

class TemplateObjectTypes(str, Enum):
    image = 'image'
    text = 'textbox'

class TemplateObject(BaseModel):
    type: TemplateObjectTypes
    width: int
    height: int
    x: int
    y: int

class TemplateImageObject(TemplateObject):
    url: str

class TemplateTextObject(TemplateObject):
    text: str

class TemplateSpec(BaseModel):
    objects: List[Union[TemplateImageObject, TemplateTextObject]]
    width: int
    height: int

class Template(BaseModel):
    template_id: str = None
    spec: TemplateSpec = None

class FeedTable(BaseModel):
    headers: List[str]
    values: List[List[Union[str, int, float]]]

class FeedData(BaseModel):
    table: FeedTable = None
    url: str = None
    
class CreateMosaicRequest(BaseModel):
    template: Template
    data: FeedData = None
    mappings: dict = None

class CreateMosaicResult(BaseModel):
    data: List[str] = None
    url: str = None

class CreateMosaicResponse(BaseModel):
    result: CreateMosaicResult


