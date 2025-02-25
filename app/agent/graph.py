from langgraph.graph import StateGraph, START, END
from app.agent.state import State
from app.agent.agent import assistant
from app.core.logger import logger
from typing import Optional

class Graph:
    """Graph class to manage the StateGraph for the assistant."""

    def __init__(self):
        try:
            logger.info("Initializing StateGraph...")
            self.builder = StateGraph(State)
            self._setup_graph()
            self.graph = self.builder.compile()
            logger.info("StateGraph compiled successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize graph: {str(e)}")
            raise RuntimeError("Graph initialization failed.")

    def _setup_graph(self):
        """Sets up nodes and edges for the graph."""
        self.builder.add_node('assistant', assistant)
        self.builder.set_entry_point('assistant')
        self.builder.add_edge('assistant', END)