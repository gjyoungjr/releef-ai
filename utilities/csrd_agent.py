import re
from typing import List, Union
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain import LLMChain

from .csrd_graph import generate_csrd_graph
from .prompts import CSRD_AGENT_PROMPT_TEMPLATE as PROMPT_TEMPLATE

load_dotenv()

# CSRD_GRAPH = generate_csrd_graph()

# text = []
# metadata = []

# for node_id, node_data in CSRD_GRAPH.nodes(data=True):
#     text.append(node_data['title'])
#     metadata.append({'id': node_id, 'label': node_data['label']})
    
# embeddings = OpenAIEmbeddings()
# CSRD_VECTOR_STORE = FAISS.from_texts(text, embeddings, metadatas=metadata)

# def search_csrd(query: str) -> str:
#     csrd_graph = generate_csrd_graph()
    
#     csrd_results = CSRD_VECTOR_STORE.similarity_search_with_score(query)
#     print(csrd_results)
    
#     response = []
    
#     for doc, score in csrd_results:
#         doc_id = doc.metadata['id']
#         doc_label = doc.metadata['label']
#         doc_content = doc.page_content
#         doc_references = ','.join(list(csrd_graph.neighbors(doc_id)))
        
#         response.append(
#             f'''######
#             [Article ID]: {doc_id}
#             [Article Name]: {doc_label}
#             [Article Content]: {doc_content}
#             [References]: {doc_references}
#             '''
#         )
        
#     return "\n\n".join(response) 

   
# def search_reference(article_reference: str) -> str: 
#     csrd_graph = generate_csrd_graph()

#     result = csrd_graph.nodes[article_reference]
#     doc_references = ','.join(list(csrd_graph.neighbors(article_reference)))
#     doc_content = result['title']
#     doc_label = result['label']
  
#     return f'''###
#     [Articel ID]: {article_reference}
#     [Article Name]: {doc_label}
#     [Article Content]: {doc_content}
#     [References]: {doc_references}
# '''

class CSRDSearch:
    def __init__(self):
        self.csrd_graph = generate_csrd_graph()
        self.text = []
        self.metadata = []
        
        for node_id, node_data in self.csrd_graph.nodes(data=True):
            self.text.append(node_data['title'])
            self.metadata.append({'id': node_id, 'label': node_data['label']})
            
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_texts(self.text, self.embeddings, metadatas=self.metadata)

    def search_csrd(self, query: str) -> str:
        csrd_results = self.vector_store.similarity_search_with_score(query)
        print(csrd_results)

        response = []
        for doc, score in csrd_results:
            doc_id = doc.metadata['id']
            doc_label = doc.metadata['label']
            doc_content = doc.page_content
            doc_references = ','.join(list(self.csrd_graph.neighbors(doc_id)))

            response.append(
                f"""######
                [Article ID]: {doc_id}
                [Article Name]: {doc_label}
                [Article Content]: {doc_content}
                [References]: {doc_references}
                """
            )

        return "\n\n".join(response)

    def search_reference(self, article_reference: str) -> str:
        result = self.csrd_graph.nodes[article_reference]
        doc_references = ','.join(list(self.csrd_graph.neighbors(article_reference)))
        doc_content = result['title']
        doc_label = result['label']

        return f"""###
        [Article ID]: {article_reference}
        [Article Name]: {doc_label}
        [Article Content]: {doc_content}
        [References]: {doc_references}
        """

class CSRDToolSetup:
    def __init__(self, csrd_search):
        self.csrd_search = csrd_search

    def create_tools(self):
        return [
            Tool(
                name='search_csrd',
                func=self.csrd_search.search_csrd,
                description='Useful for when you need to answer questions about the CSRD directive'
            ),
            Tool(
                name='expand_search_reference',
                func=self.csrd_search.search_reference,
                description='Useful for when you need to expand your reference to get more information'
            )
        ]

class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)
    

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
    

csrd_search = CSRDSearch()
tool_setup = CSRDToolSetup(csrd_search)
tools = tool_setup.create_tools()
prompt = CustomPromptTemplate(
    template=PROMPT_TEMPLATE,
    tools=tools,
    input_variables=['input', 'intermediate_steps']
)
output_parser = CustomOutputParser()
llm = OpenAI(temperature=0)
llm_chain = LLMChain(llm=llm, prompt=prompt)
     


tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

def query_csrd_agent(query: str) -> str:
    response = agent_executor.invoke({"input": query})
    return response['output']