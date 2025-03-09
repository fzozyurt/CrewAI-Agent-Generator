import streamlit as st
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

from framework.crewai_generator import create_crewai_code, render_crewai_overview
from framework.tool_utils import (
    get_available_tools,
    get_tool_description,
    get_tool_env_requirements,
)
from generators.prompt_builder import prompt_builder

st.set_page_config(page_title="CrewAI Generator", page_icon="🤖", layout="wide")


def main():
    st.title("🤖 CrewAI Generator")

    # Initialize session state for configuration
    if "config" not in st.session_state:
        st.session_state.config = {"agents": [], "tasks": []}

    # Initialize navigation state
    if "navigation" not in st.session_state:
        st.session_state.navigation = None

    # Sidebar info
    with st.sidebar:
        st.write("### CrewAI Generator")
        st.write(
            "Bu uygulama, CrewAI framework'ü için ekip ve görev yapılandırması oluşturmanıza yardımcı olur."
        )

        # API Key girişi
        with st.expander("API Ayarları", expanded=False):
            openai_key = st.text_input("OpenAI API Key", type="password")
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key

            openrouter_key = st.text_input("OpenRouter API Key", type="password")
            if openrouter_key:
                os.environ["OPENROUTER_API_KEY"] = openrouter_key

    # Navigation
    tabs = ["Prompt Builder", "Agent Builder", "Task Builder", "Preview & Code"]

    # Use the stored navigation if set
    if st.session_state.navigation:
        selected_tab = st.session_state.navigation
        # Reset navigation state
        st.session_state.navigation = None
    else:
        selected_tab = st.sidebar.radio("Navigation", tabs)

    if selected_tab == "Prompt Builder":
        prompt_builder()
    elif selected_tab == "Agent Builder":
        agent_builder()
    elif selected_tab == "Task Builder":
        task_builder()
    elif selected_tab == "Preview & Code":
        preview_and_code()


def agent_builder():
    st.header("Agent Builder")

    # Form for creating a new agent
    with st.form("agent_form"):
        st.subheader("Create a New Agent")
        name = st.text_input("Agent Identifier (no spaces)")
        role = st.text_input("Role")
        goal = st.text_area("Goal")
        backstory = st.text_area("Backstory")

        col1, col2 = st.columns(2)
        with col1:
            verbose = st.checkbox("Verbose", value=True)
        with col2:
            allow_delegation = st.checkbox("Allow Delegation", value=False)

        # Tool selection
        st.subheader("Select Tools")
        available_tools = get_available_tools()
        selected_tools = []

        # Display tools in columns
        cols = st.columns(2)
        for i, (tool_name, tool_info) in enumerate(available_tools.items()):
            col_index = i % 2
            with cols[col_index]:
                if st.checkbox(f"{tool_name}", help=tool_info["description"]):
                    selected_tools.append(tool_name)
                    # If tool requires environment variables, show a note
                    if tool_info.get("requires_env", False):
                        st.info(
                            f"Note: {tool_name} requires the environment variable: {tool_info.get('env_var')}"
                        )

        submitted = st.form_submit_button("Add Agent")
        if submitted:
            if not name or not role or not goal:
                st.error("Agent identifier, role, and goal are required!")
            else:
                agent = {
                    "name": name,
                    "role": role,
                    "goal": goal,
                    "backstory": backstory,
                    "verbose": verbose,
                    "allow_delegation": allow_delegation,
                    "tools": selected_tools,
                }

                st.session_state.config["agents"].append(agent)
                st.success(f"Agent '{name}' added successfully!")

                # Show environment variable requirements if any
                env_requirements = get_tool_env_requirements(selected_tools)
                if env_requirements:
                    st.warning("⚠️ Some selected tools require environment variables:")
                    for req in env_requirements:
                        st.code(f"{req['env_var']}=your_value_here")

    # Display existing agents
    if st.session_state.config["agents"]:
        st.header("Existing Agents")
        for i, agent in enumerate(st.session_state.config["agents"]):
            with st.expander(f"🤖 {agent['role']}", expanded=False):
                st.write(f"**Goal:** {agent['goal']}")
                st.write(f"**Backstory:** {agent['backstory']}")

                if "tools" in agent and agent["tools"]:
                    st.write(f"**Tools:** {', '.join(agent['tools'])}")
                else:
                    st.write("**Tools:** None")

                if st.button(f"Delete Agent", key=f"delete_agent_{i}"):
                    st.session_state.config["agents"].pop(i)
                    # Also remove tasks associated with this agent
                    st.session_state.config["tasks"] = [
                        task
                        for task in st.session_state.config["tasks"]
                        if task["agent"] != agent["name"]
                    ]
                    st.rerun()


def task_builder():
    st.header("Task Builder")

    # Check if agents exist
    if not st.session_state.config["agents"]:
        st.warning("Please create at least one agent before creating tasks.")
        return

    # Form for creating a new task
    with st.form("task_form"):
        st.subheader("Create a New Task")
        name = st.text_input("Task Identifier (no spaces)")
        description = st.text_area("Description")
        expected_output = st.text_area("Expected Output")

        # Agent selection
        agent_options = [agent["name"] for agent in st.session_state.config["agents"]]
        agent = st.selectbox("Assign to Agent", agent_options)

        submitted = st.form_submit_button("Add Task")
        if submitted:
            if not name or not description:
                st.error("Task identifier and description are required!")
            else:
                task = {
                    "name": name,
                    "description": description,
                    "expected_output": expected_output,
                    "agent": agent,
                }

                st.session_state.config["tasks"].append(task)
                st.success(f"Task '{name}' added successfully!")

    # Display existing tasks
    if st.session_state.config["tasks"]:
        st.header("Existing Tasks")
        for i, task in enumerate(st.session_state.config["tasks"]):
            with st.expander(f"📋 {task['name']}", expanded=False):
                st.write(f"**Description:** {task['description']}")
                st.write(f"**Expected Output:** {task['expected_output']}")
                st.write(f"**Assigned to:** {task['agent']}")

                if st.button(f"Delete Task", key=f"delete_task_{i}"):
                    st.session_state.config["tasks"].pop(i)
                    st.rerun()


def preview_and_code():
    st.header("Preview & Generated Code")

    # Check if configuration is complete
    if not st.session_state.config["agents"]:
        st.warning("Please create at least one agent.")
        return

    if not st.session_state.config["tasks"]:
        st.warning("Please create at least one task.")
        return

    # Check for environment variable requirements
    all_tools = []
    for agent in st.session_state.config["agents"]:
        if "tools" in agent and agent["tools"]:
            all_tools.extend(agent["tools"])

    env_requirements = get_tool_env_requirements(all_tools)
    if env_requirements:
        st.warning("⚠️ Your configuration requires the following environment variables:")
        env_code = "# Add these to your .env file:\n"
        for req in env_requirements:
            env_code += f"{req['env_var']}=your_value_here\n"
        st.code(env_code)

    # Show configuration overview
    render_crewai_overview(st.session_state.config)

    # Generate and display code
    st.header("Generated CrewAI Code")
    generated_code = create_crewai_code(st.session_state.config)
    st.code(generated_code, language="python")

    # Download button for the generated code
    st.download_button(
        label="Download Python Code",
        data=generated_code,
        file_name="crew_ai_script.py",
        mime="text/plain",
    )

    # Also provide .env template if needed
    if env_requirements:
        env_template = "# Environment variables for CrewAI\n"
        for req in env_requirements:
            env_template += f"{req['env_var']}=your_value_here\n"

        st.download_button(
            label="Download .env Template",
            data=env_template,
            file_name=".env.template",
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
