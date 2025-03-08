from typing import Dict, Any


def create_langgraph_code(config: Dict[str, Any]) -> str:
    """
    Generates LangGraph Python code from the provided configuration.

    Args:
        config: Dictionary containing agents, nodes and edges configuration

    Returns:
        String containing generated Python code for LangGraph
    """
    code = """from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from typing import Dict, List, Tuple, Any, TypedDict, Annotated
import operator

# Define state
class AgentState(TypedDict):
    messages: List[BaseMessage]
    next: str

"""

    # Generate tool definitions if needed
    if any(agent["tools"] for agent in config["agents"]):
        code += "# Define tools\n"
        tools = set()
        for agent in config["agents"]:
            tools.update(agent["tools"])

        for tool in tools:
            code += f"""class {tool.capitalize()}Tool(BaseTool):
    name = "{tool}"
    description = "Tool for {tool} operations"
    
    def _run(self, query: str) -> str:
        # Implement actual functionality here
        return f"Result from {tool} tool: {{query}}"
    
    async def _arun(self, query: str) -> str:
        # Implement actual functionality here
        return f"Result from {tool} tool: {{query}}"

"""

        code += "tools = [\n"
        for tool in tools:
            code += f"    {tool.capitalize()}Tool(),\n"
        code += "]\n\n"

    # Generate Agent configurations
    for agent in config["agents"]:
        code += f"# Agent: {agent['name']}\n"
        code += f"def {agent['name']}_agent(state: AgentState) -> AgentState:\n"
        code += f"    \"\"\"Agent that handles {agent['role']}.\"\"\"\n"
        code += f"    # Create LLM\n"
        code += f"    llm = ChatOpenAI(model=\"{agent['llm']}\")\n"
        code += f"    # Get the most recent message\n"
        code += f"    messages = state['messages']\n"
        code += f"    response = llm.invoke(messages)\n"
        code += f"    # Add the response to the messages\n"
        code += f"    return {{\n"
        code += f'        "messages": messages + [response],\n'
        code += f'        "next": state.get("next", "")\n'
        code += f"    }}\n\n"

    # Define routing logic function
    code += """# Define routing logic
def router(state: AgentState) -> str:
    \"\"\"Route to the next node.\"\"\"
    return state.get("next", "END")

"""

    # Generate graph configuration
    code += "# Define the graph\n"
    code += "workflow = StateGraph(AgentState)\n\n"

    # Add nodes
    code += "# Add nodes to the graph\n"
    for node in config["nodes"]:
        code += f"workflow.add_node(\"{node['name']}\", {node['agent']}_agent)\n"

    code += "\n# Add conditional edges\n"
    # Add edges
    for edge in config["edges"]:
        if edge["target"] == "END":
            code += f"workflow.add_edge(\"{edge['source']}\", END)\n"
        else:
            code += f"workflow.add_edge(\"{edge['source']}\", \"{edge['target']}\")\n"

    # Set entry point
    if config["nodes"]:
        code += f"\n# Set entry point\nworkflow.set_entry_point(\"{config['nodes'][0]['name']}\")\n"

    # Compile and run
    code += """
# Compile the graph
app = workflow.compile()

# Run the graph
def run_agent(query: str) -> List[BaseMessage]:
    \"\"\"Run the agent on a query.\"\"\"
    result = app.invoke({
        "messages": [HumanMessage(content=query)],
        "next": ""
    })
    return result["messages"]

# Example usage
if __name__ == "__main__":
    result = run_agent("Your query here")
    for message in result:
        print(f"{message.type}: {message.content}")
"""

    return code


def render_langgraph_overview(config: Dict[str, Any]):
    """
    Renders a visual overview of LangGraph configuration in Streamlit UI.

    Args:
        config: Dictionary containing agents, nodes and edges configuration
    """
    import streamlit as st

    # Display Agents
    st.subheader("Agents")
    for agent in config["agents"]:
        with st.expander(f"🤖 {agent['role']}", expanded=True):
            st.write(f"**Goal:** {agent['goal']}")
            st.write(f"**Tools:** {', '.join(agent['tools'])}")
            st.write(f"**LLM:** {agent['llm']}")

    # Display Nodes
    st.subheader("Graph Nodes")
    for node in config["nodes"]:
        with st.expander(f"📍 {node['name']}", expanded=True):
            st.write(f"**Description:** {node['description']}")
            st.write(f"**Agent:** {node['agent']}")

    # Display Edges
    st.subheader("Graph Edges")
    for edge in config["edges"]:
        with st.expander(f"🔗 {edge['source']} → {edge['target']}", expanded=True):
            if "condition" in edge:
                st.write(f"**Condition:** {edge['condition']}")
