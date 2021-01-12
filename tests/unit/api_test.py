from starlette.testclient import TestClient
import os
import sys
sys.path.append(os.getcwd())
from mosaic.server import app
from base64 import b64encode

client = TestClient(app)

def test_ping():
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_create_mosaic_returns_ok():
    body = {
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

    response = client.post(
        "/api/v1/mosaic",
        json=body
    )

    assert response.status_code == 200
    assert response.json()['result'] is not None
    assert len(response.json()['result']['data']) == 2

    # TODO Do a through test by storing the generating file ocally and comparing md5 chceksums

