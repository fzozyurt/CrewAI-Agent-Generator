from typing import Dict, Any


def create_crewai_code(config: Dict[str, Any]) -> str:
    """
    Generates CrewAI Python code from the provided configuration.

    Args:
        config: Dictionary containing agents and tasks configuration

    Returns:
        String containing generated Python code for CrewAI
    """
    code = "from crewai import Agent, Task, Crew\n"

    # Add tool imports if needed
    used_tools = set()
    for agent in config["agents"]:
        if "tools" in agent and agent["tools"]:
            for tool in agent["tools"]:
                used_tools.add(tool)

    if used_tools:
        code += "from crewai_tools import (\n"
        code += "    " + ",\n    ".join(sorted(used_tools))
        code += "\n)\n"

        # Add environment variables if needed
        env_vars = set()
        if "SerperDevTool" in used_tools:
            env_vars.add("SERPER_API_KEY")
        if "BrowserTool" in used_tools:
            env_vars.add("BROWSERLESS_API_KEY")
        if "GmailTool" in used_tools:
            env_vars.add("GMAIL_TOKEN_PATH")

        if env_vars:
            code += "\nimport os\nfrom dotenv import load_dotenv\n\n"
            code += "# Load environment variables\n"
            code += "load_dotenv()\n\n"

            # Add check for required env variables
            for var in env_vars:
                code += f"if '{var}' not in os.environ:\n"
                code += f'    raise ValueError("Please set the {var} environment variable")\n'
            code += "\n"

    code += "\n"

    # Generate Agent configurations
    for agent in config["agents"]:
        code += f"# Agent: {agent['name']}\n"

        # Create tools list if tools are defined
        if "tools" in agent and agent["tools"]:
            tool_instances = []
            for tool in agent["tools"]:
                if tool == "SerperDevTool":
                    tool_instances.append(f"{tool}()")
                elif tool == "BrowserTool":
                    tool_instances.append(f"{tool}()")
                elif tool == "DirectoryReadTool":
                    tool_instances.append(f"{tool}(directory_path='.')")
                elif tool == "FileReadTool":
                    tool_instances.append(f"{tool}(file_path='example.txt')")
                elif tool == "WebsiteSearchTool":
                    tool_instances.append(f"{tool}()")
                elif tool == "WikipediaSearchTool":
                    tool_instances.append(f"{tool}()")
                else:
                    tool_instances.append(f"{tool}()")

            tools_str = ", ".join(tool_instances)
            code += f"tools_{agent['name']} = [{tools_str}]\n"

        # Create agent
        code += f"agent_{agent['name']} = Agent(\n"
        code += f"    role='{agent['role']}',\n"
        code += f"    goal='{agent['goal']}',\n"
        code += f"    backstory='{agent['backstory']}',\n"
        code += f"    verbose={agent['verbose']},\n"
        code += f"    allow_delegation={agent['allow_delegation']},\n"

        # Add tools reference if available
        if "tools" in agent and agent["tools"]:
            code += f"    tools=tools_{agent['name']}\n"
        else:
            code += "    tools=[]\n"

        code += ")\n\n"

    # Generate Task configurations
    for task in config["tasks"]:
        code += f"# Task: {task['name']}\n"
        code += f"task_{task['name']} = Task(\n"
        code += f"    description='{task['description']}',\n"
        code += f"    agent=agent_{task['agent']},\n"
        code += f"    expected_output='{task['expected_output']}'\n"
        code += ")\n\n"

    # Generate Crew configuration
    code += "# Crew Configuration\n"
    code += "crew = Crew(\n"
    code += (
        "    agents=["
        + ", ".join(f"agent_{a['name']}" for a in config["agents"])
        + "],\n"
    )
    code += (
        "    tasks=[" + ", ".join(f"task_{t['name']}" for t in config["tasks"]) + "]\n"
    )
    code += ")\n\n"
    code += "# Run the crew\n"
    code += "result = crew.kickoff()"

    return code


def render_crewai_overview(config: Dict[str, Any]):
    """
    Renders a visual overview of CrewAI configuration in Streamlit UI.

    Args:
        config: Dictionary containing agents and tasks configuration
    """
    import streamlit as st

    # Display Agents
    st.subheader("Agents")
    for agent in config["agents"]:
        with st.expander(f"🤖 {agent['role']}", expanded=True):
            st.write(f"**Goal:** {agent['goal']}")
            st.write(f"**Backstory:** {agent['backstory']}")

            if "tools" in agent and agent["tools"]:
                st.write(f"**Tools:** {', '.join(agent['tools'])}")
            else:
                st.write("**Tools:** None")

    # Display Tasks
    st.subheader("Tasks")
    for task in config["tasks"]:
        with st.expander(f"📋 {task['name']}", expanded=True):
            st.write(f"**Description:** {task['description']}")
            st.write(f"**Expected Output:** {task['expected_output']}")
            st.write(f"**Assigned to:** {task['agent']}")
