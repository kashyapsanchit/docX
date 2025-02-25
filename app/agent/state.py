from langgraph.graph import MessagesState
from typing import List

class State(MessagesState):
    doc_titles: List[str]
    query: str
    response: str