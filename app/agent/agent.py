from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.state import State
from langchain_groq import ChatGroq
from app.core.config import settings
from app.agent.tools import tools
from langgraph.prebuilt import create_react_agent
import json

def assistant(state: State):

    llm = ChatGroq(model=settings.MODEL_NAME, api_key=settings.GROQ_KEY)

    system_message = SystemMessage(content="""You are a helpful assistant.

    Your task is to retrieve the most relevant chunks from the Qdrant vector store using the `search_document` tool and provide a concise, well-structured response to the user.

    **Guidelines:**
    - Use the `search_document` tool with **exact** `doc_titles` provided by the user. Do not modify, paraphrase, or enhance them.
    - Ensure all tool calls include the correct parameters.
    - Once you receive the tool's response, use **only** that information to generate the final answer. **Do not** invoke any other tools.
    - Craft your answer to be brief, informative, and based solely on the tool's output.

    **Response Format:**
    Your final response **must** be a valid JSON object in the following structure and should include nothing else:

    {
        "response": "Your concise, brief and well-structured answer based on the tool's output."
    }
    """)
    
    human_message = HumanMessage(content=f"""Here is the user's query: {state['query']}.\n
    Use the following document titles **exactly as provided** when calling the `search_document` tool:\n
    {json.dumps(state['doc_titles'])}
    """)

    agent = create_react_agent(llm, tools)

    inputs = {"messages": [system_message, human_message]}

    llm_response = agent.invoke(inputs)


    res = json.loads(llm_response['messages'][-1].content)

    if res['response']:
        state['response'] = res['response']
    else:
        state['response'] = "Sorry I could not find any relevant information in the document(s) for your query."


    return state
