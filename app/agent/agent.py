from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.state import State
from langchain_groq import ChatGroq
from app.core.config import settings
from app.agent.tools import tools
from app.agent.constants import SYSTEM_PROMPT
from langgraph.prebuilt import create_react_agent
import json
from typing import Dict, Any
from app.core.logger import logger



def assistant(state: State, llm: ChatGroq = None) -> Dict[str, Any]:
    """Handles user queries by invoking the LLM with a ReAct agent and returning structured responses.

    Args:
        state (State): The current state including user query and document titles.
        llm (ChatGroq, optional): Pre-initialized LLM instance. Defaults to None.

    Returns:
        Dict[str, Any]: Updated state with the assistant's response.
    """
    try:
        if llm is None:
            logger.info("Initializing ChatGroq LLM...")
            llm = ChatGroq(model=settings.MODEL_NAME, api_key=settings.GROQ_KEY)

        system_message = SystemMessage(content=SYSTEM_PROMPT)
        human_message = HumanMessage(content=f"""Here is the user's query: {state['query']}.\n
        Use the following document titles **exactly as provided** when calling the `search_document` tool:\n
        {json.dumps(state['doc_titles'])}
        """)

        agent = create_react_agent(llm, tools)
        inputs = {"messages": [system_message, human_message]}

        logger.info("Invoking LLM with user query...")
        llm_response = agent.invoke(inputs)

        raw_response = llm_response['messages'][-1].content

        try:
            res = json.loads(raw_response)
            state['response'] = res.get('response', "Sorry, I couldn't find any relevant information.")
        except json.JSONDecodeError:
            logger.error(f"Malformed JSON from LLM: {raw_response}")
            state['response'] = "Error processing the response from the assistant."

        logger.info(f"Assistant response: {state['response']}")
        return state

    except Exception as e:
        logger.error(f"Error in assistant function: {str(e)}")
        state['response'] = "An internal error occurred while processing your query."
        return state
