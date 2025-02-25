from langgraph.graph import StateGraph, START, END 
from app.agent.state import State   
from app.agent.agent import assistant
# from app.agent.tools import tools

class Graph:

    def __init__(self):

        self.builder = StateGraph(State)
        self.builder.add_node('assistant', assistant)

        self.builder.set_entry_point('assistant')  
        self.builder.add_edge('assistant', END) 

        self.graph = self.builder.compile()