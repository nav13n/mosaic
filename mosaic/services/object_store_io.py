class ObjectStoreIO:
    
    """Save Image Data"""

    def __init__(self, config=None, log=None):
        self.url = None

 
    async def put(self,  file_name: str, data: bytes) -> str:
        #TODO Save image to a blob store
        url = 'public_url_prefix/{}'.format(file_name)
        return url


    