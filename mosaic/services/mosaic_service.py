import pypeln as pl
from .object_store_io import ObjectStoreIO
from string import Template as StringTemplate
from typing import Union, List, Any
import uuid
from ..models import (
    TemplateObjectTypes,
    TemplateObject,
    TemplateImageObject,
    TemplateTextObject,
    TemplateSpec,
    Template,
    FeedTable,
    FeedData
    )

class MosaicService:
    
    """Dynamically generate an image using template and some replacement data"""    
    def __init__(self, config=None, log=None):
        self.config = config
        self.store_io = ObjectStoreIO(config=config, log=None)
 
    async def get_template(self, id: str) -> TemplateSpec:
         #TODO Retrieve template from is using Template Service
        template_spec = TemplateSpec.parse_obj(
            {
                "objects":[{
                    "type":"image",
                    "width":350,
                    "height":300,
                    "x":300,
                    "y":300,
                    "url":"$url"
                },{
                    "type":"textbox",
                    "width":300,
                    "height":300,
                    "x":100,
                    "y":100,
                    "text":"Now at $$$price"
                }],
                "width":600,
                "height":600
            })
        return template_spec

    async def get_data(self, url: str) -> FeedTable:
        #TODO Retrieve feed data from Feed url
        table = FeedTable.parse_obj({
                "headers":["id", "price", "title", "description", "url"],
                "values":[[1,50,'product1','desc1','url1'], [2,25,'product2','desc2','url2']]
        })
        return table

    async def generate(self, template_spec: TemplateSpec, mappings: dict, table: FeedTable) -> List[Any]:
        #TODO Asynchronously call the image generation

        headers = table.headers
        values = table.values
        def on_start():
            return dict(
                headers = headers, 
                template_spec = template_spec,
                mappings = mappings
            )
        stage = pl.task.map(self.generate_images, values, workers=3, maxsize=4, on_start = on_start) #TODO Pass from config
        results = await stage
        return results

    async def generate_images(self, value: List[Union[str, int, float]], headers:List[str], template_spec: TemplateSpec, mappings: dict) -> str:
        #TODO Replace the place holder with values in rendered template
        
        data_dict =  {headers[i]: value[i] for i in range(len(headers))} 
        template_spec_dict = template_spec.dict()

        for obj in template_spec_dict['objects']:
            for key in obj.keys():
                if key in mappings.keys():
                    substitution= {mappings[key]:str(data_dict[mappings[key]])}
                    template = StringTemplate(obj[key])
                    obj[key] = template.substitute(**substitution)

        image_bytes = await self.get_image_for_template(template_spec_dict)

        image_name = '{}.png'.format(str(uuid.uuid4()))
        image_url = await self.store_io.put(image_name, image_bytes)

        return image_url

    async def get_image_for_template(self, rendered_template: dict) -> bytes :
        #TODO Call the existing image generation API to get the image from template
        #TODO Use retry with backoff as the downstream API has 5% failure rate
        print(rendered_template)
        image_bytes = bytes('image', 'utf-8')
        return image_bytes

 
