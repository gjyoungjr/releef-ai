from pinecone import Pinecone, ServerlessSpec


# TODO: Add 'typing' to func args 
class PineconeClient:
    def __init__(self, api_key: str):
        self.client = Pinecone(api_key=api_key)

    def list_indexes(self):
        return self.client.list_indexes()

    def create_index(self, name, dimension, metric, spec):
        self.client.create_index(
            name=name, 
            dimension=dimension, 
            metric=metric, 
            spec=ServerlessSpec( # TODO: Change to accept spec as a parameter
            cloud='aws',
            region='us-east-1'
        ))

    def get_index(self, name):
        return self.client.Index(name)
