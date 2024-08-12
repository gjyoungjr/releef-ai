from llama_index.core.node_parser import SentenceSplitter

# TODO: Add 'typing' to func args
def create_embedding(document): 
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(document)
    print(f"Content of node 0: {nodes[1].get_content(metadata_mode='all')}")
    
    return nodes
    
   