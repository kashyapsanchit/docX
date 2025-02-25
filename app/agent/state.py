from langgraph.graph import MessagesState

class State(MessagesState):
    doc_titles: list = None
    query: str
    response: str