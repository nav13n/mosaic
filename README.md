# Template Based Image Generation Service

Follow the Makefile.
```
make environment
make install
make test
make run
make package
make publish
```


"""
Assumption 1: # CSV Headers and Placeholders have same name
Assumption 2: An image generation service already exists that can generate an image given a rendered template
"""

"""
Payload Example:
"""
```
{
        "template": {
            "spec": {
                "objects":[{
                    "type":"image",
                    "width":300,
                    "height":300,
                    "x":100,
                    "y":100,
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
            }
        },
        "data": {
            "table":{
                "headers":["id", "price", "title", "description", "url"],
                "values":[[1,50,'product1','desc1','url1'], [2,25,'product2','desc2','url2']]
            }
        },
       "mappings":{
           "url": "url",
           "text": "price"
       }}
}
```
