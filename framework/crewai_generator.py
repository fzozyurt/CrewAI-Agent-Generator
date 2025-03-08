from typing import Dict, Any


def create_crewai_code(config: Dict[str, Any]) -> str:
    """
    Generates CrewAI Python code from the provided configuration.

    Args:
        config: Dictionary containing agents and tasks configuration

    Returns:
        String containing generated Python code for CrewAI
    """
    code = "from crewai import Agent, Task, Crew\n\n"

    # Generate Agent configurations
    for agent in config["agents"]:
        code += f"# Agent: {agent['name']}\n"
        code += f"agent_{agent['name']} = Agent(\n"
        code += f"    role='{agent['role']}',\n"
        code += f"    goal='{agent['goal']}',\n"
        code += f"    backstory='{agent['backstory']}',\n"
        code += f"    verbose={agent['verbose']},\n"
        code += f"    allow_delegation={agent['allow_delegation']},\n"
        code += f"    tools={agent['tools']}\n"
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
            st.write(f"**Tools:** {', '.join(agent['tools'])}")

    # Display Tasks
    st.subheader("Tasks")
    for task in config["tasks"]:
        with st.expander(f"📋 {task['name']}", expanded=True):
            st.write(f"**Description:** {task['description']}")
            st.write(f"**Expected Output:** {task['expected_output']}")
            st.write(f"**Assigned to:** {task['agent']}")
