from environs import Env
import json
from typing import Dict, List
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))

env = Env()
env.read_env()

def read_json_file(file:str) -> Dict:
    with open(file) as f:
        data = json.load(f)
    return data

def read_version(file:str) -> str:
    service_version = "NA"
    if os.path.exists(file):
        with open(file) as version_file:
            service_version = version_file.readline().strip()
    return service_version
    
OPENAPI_PREFIX = env.str("OPENAPI_PREFIX")

ALLOWED_HOSTS: List[str] = [] #TODO: fixme

# app port
HTTP_PORT = env.int("HTTP_PORT")
MAX_WORKER = env.int("MAX_WORKER")

VERSION_FILE = env.str("VERSION_FILE")
API_V1_STR = env.str("API_V1_STR")

SERVICE_VERSION = read_version(VERSION_FILE)
SERVICE_NAME = env.str("SERVICE_NAME", "test-service")


