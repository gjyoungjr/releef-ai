from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import (
    HumanMessage,
)

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked "
            "to extract, return null for the attribute's value.",
        ),
        MessagesPlaceholder("context"),
        ("human", "{text}"),
    ]
)


prompt.invoke(
    {"text": "this is some text", "context": [HumanMessage(content="testing 1 2 3")]}
)