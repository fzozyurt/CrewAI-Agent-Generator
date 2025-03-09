import streamlit as st
from framework.tool_utils import (
    get_available_tools,
    format_tool_for_config,
    validate_tool_parameters,
)


def tool_configurator():
    """
    Streamlit UI for configuring CrewAI tools
    """
    st.title("🛠️ CrewAI Tools Configurator")

    # Get available tools
    available_tools = get_available_tools()

    # Show tool selection section
    st.header("Available Tools")

    col1, col2 = st.columns(2)

    with col1:
        selected_tool = st.selectbox(
            "Select a tool to configure:", options=list(available_tools.keys())
        )

    tool_info = available_tools[selected_tool]

    with col2:
        st.info(tool_info["description"])

    # Configure tool parameters
    st.subheader(f"Configure {selected_tool}")

    # Initialize parameters
    params = {}
    for param_name, param_config in tool_info["parameters"].items():
        param_type = param_config["type"]
        param_desc = param_config.get("description", "")
        param_required = param_config.get("required", False)
        param_default = param_config.get("default", "")

        label = f"{param_name} {'(required)' if param_required else ''}"

        # Add appropriate input field based on parameter type
        if param_type == "str":
            params[param_name] = st.text_input(
                label, value=param_default, help=param_desc
            )
        elif param_type == "int":
            params[param_name] = st.number_input(
                label,
                value=int(param_default) if param_default else 0,
                step=1,
                help=param_desc,
            )
        elif param_type == "float":
            params[param_name] = st.number_input(
                label,
                value=float(param_default) if param_default else 0.0,
                help=param_desc,
            )
        elif param_type == "bool":
            params[param_name] = st.checkbox(
                label,
                value=param_default if isinstance(param_default, bool) else False,
                help=param_desc,
            )

    # Display tool configuration code
    st.subheader("Generated Tool Configuration")

    # Validate parameters
    errors = validate_tool_parameters(selected_tool, params)
    if errors:
        for error in errors:
            st.error(error)
    else:
        tool_config = format_tool_for_config(selected_tool, params)

        # Display how to use this tool in your config
        st.code(
            f"""
# Tool configuration for {selected_tool}
tool_config = {tool_config}

# Add this tool to your agent configuration
agent_config = {{
    "name": "your_agent_name",
    "role": "Your agent role",
    "goal": "Your agent goal",
    "backstory": "Your agent backstory",
    "verbose": True,
    "allow_delegation": False,
    "tools": [tool_config]
}}
        """
        )

        # Add button to copy configuration
        if st.button("Add to Session"):
            if "configured_tools" not in st.session_state:
                st.session_state.configured_tools = []

            st.session_state.configured_tools.append(tool_config)
            st.success(f"Added {selected_tool} to your tools!")

    # Display currently configured tools
    if "configured_tools" in st.session_state and st.session_state.configured_tools:
        st.subheader("Your Configured Tools")
        for i, tool in enumerate(st.session_state.configured_tools):
            with st.expander(f"Tool {i+1}: {tool['type']}", expanded=True):
                st.write(tool)
                if st.button(f"Remove Tool {i+1}", key=f"remove_{i}"):
                    st.session_state.configured_tools.pop(i)
                    st.rerun()


if __name__ == "__main__":
    tool_configurator()
