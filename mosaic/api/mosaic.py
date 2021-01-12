from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict
import uuid
import json
import logging

from ..models import (
    TemplateObjectTypes,
    TemplateObject,
    TemplateImageObject,
    TemplateTextObject,
    TemplateSpec,
    Template,
    FeedTable,
    FeedData,
    CreateMosaicRequest,
    CreateMosaicResult,
    CreateMosaicResponse 
    )

from ..services.mosaic_service import MosaicService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/mosaic", response_model=CreateMosaicResponse)
async def create_mosaic(
    request: CreateMosaicRequest
    ):
    
    template = request.template
    data = request.data
    mappings = request.mappings
   
    # Validations
    if template.template_id is not None and template.spec is not None:
        raise HTTPException(status_code=400, detail="Invalid Request! Only one of the id or spec fields shall be present!")

    if template.template_id is None and template.spec is None:
        raise HTTPException(status_code=400, detail="Invalid Request! Atleast one of the id or spec fields shall be present!")

    if data.table is not None and data.url is not None:
        raise HTTPException(status_code=400, detail="Invalid Request! Only one of the table or url fields shall be present!")

    if data.table is None and data.url is None:
        raise HTTPException(status_code=400, detail="Invalid Request! Atleast one of the table or url fields shall be present!")


    # Initialise mosaic service
    mosaic_service = MosaicService(log=logger)

    template_spec = template.spec
    if template_spec is None:
        # TODO Retrieve template spec from template service for the template id 
        pass
    
    table = data.table
    if table is None:
        # TODO Retrieve template spec from template service for the template id 
        pass

    
    result = await mosaic_service.generate(template_spec, mappings, table)
    response = CreateMosaicResponse(result=CreateMosaicResult(data=result))

    return response

