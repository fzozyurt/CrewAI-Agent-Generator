import streamlit as st
import os
import time
import traceback
from dotenv import load_dotenv
from typing import Dict, Any

from generators.agent_generator import AgentGenerator, generate_agents

from framework import create_code_block, render_framework_overview
from utils.prompts import get_framework_description, get_example_prompts
from utils.openrouter import get_openrouter_models

# Load environment variables
load_dotenv()


def main():
    # Set up page configuration only once
    if "page_config_done" not in st.session_state:
        st.set_page_config(
            page_title="Agent Framework Generator", page_icon="🚀", layout="wide"
        )
        st.session_state.page_config_done = True

    # Initialize session state variables if not already set
    if "available_models" not in st.session_state:
        st.session_state.available_models = []
        st.session_state.model_options = []
        st.session_state.selected_model_id = (
            "deepseek/deepseek-r1:free"  # Default model
        )
        st.session_state.api_key_provided = False
        st.session_state.error_logs = []

    st.title("Multi-Framework Agent Generator")
    st.write("Generate agent code for different frameworks based on your requirements!")

    # Display OpenRouter information
    st.sidebar.title("🌐 OpenRouter")
    st.sidebar.info("Powered by OpenRouter AI models")

    # Check for API key first
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input("OpenRouter API Key:", type="password")
        if api_key:
            os.environ["OPENROUTER_API_KEY"] = api_key
            st.session_state.api_key_provided = True
            # Don't rerun page, we'll use the key in subsequent operations
    else:
        st.session_state.api_key_provided = True

    # Only try to fetch models if we have an API key and haven't already fetched them
    if st.session_state.api_key_provided and not st.session_state.available_models:
        try:
            st.sidebar.text("Loading available models...")
            progress_placeholder = st.sidebar.empty()
            is_free_only = st.sidebar.checkbox(
                "Only show free models", value=True, key="isFree"
            )
            try:
                all_models = get_openrouter_models(free_only=is_free_only)
                if all_models:
                    st.session_state.available_models = all_models

                    # Create model options
                    model_options = []
                    for model in all_models:
                        label = f"{model['name']} by {model['author']}"
                        model_options.append((model["model_id"], label))

                    st.session_state.model_options = model_options
                else:
                    st.sidebar.warning("Could not fetch models. Using default model.")
                    st.session_state.available_models = [
                        {
                            "name": "Llama-3 70B",
                            "model_id": "meta-llama/llama-3-3-70b-instruct",
                        }
                    ]
            finally:
                progress_placeholder.empty()
        except Exception as e:
            error_msg = f"Error fetching models: {e}"
            st.session_state.error_logs.append(error_msg)
            st.sidebar.error(error_msg)
            st.session_state.available_models = [
                {"name": "Llama-3 70B", "model_id": "meta-llama/llama-3-3-70b-instruct"}
            ]

    # Model selection
    st.sidebar.subheader("🤖 Choose AI Model")

    # Only show model selection if we have models
    if st.session_state.model_options:
        selected_model_id = st.sidebar.selectbox(
            "Select model:",
            options=[model_id for model_id, _ in st.session_state.model_options],
            format_func=lambda x: next(
                (
                    label
                    for model_id, label in st.session_state.model_options
                    if model_id == x
                ),
                x,
            ),
            index=next(
                (
                    i
                    for i, (model_id, _) in enumerate(st.session_state.model_options)
                    if model_id == "deepseek/deepseek-r1:free"
                ),
                0,
            ),
            key="model_selection",
        )
        st.session_state.selected_model_id = selected_model_id
    else:
        st.sidebar.info("Default model: DeepSeek: R1 (free) by DEEPSEEK")
        st.session_state.selected_model_id = "deepseek/deepseek-r1:free"

    # Framework selection
    st.sidebar.title("🔄 Framework Selection")
    framework = st.sidebar.radio(
        "Choose a framework:",
        ["crewai", "langgraph"],
        format_func=lambda x: {"crewai": "CrewAI", "langgraph": "LangGraph"}[x],
    )

    # Framework description
    st.sidebar.markdown(get_framework_description(framework))

    # Sidebar for examples
    st.sidebar.title("📚 Example Prompts")
    example_prompts = get_example_prompts()
    selected_example = st.sidebar.selectbox(
        "Choose an example:", list(example_prompts.keys()), key="example_selection"
    )

    # Main input area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎯 Define Your Requirements")
        user_prompt = st.text_area(
            "Describe what you need:",
            value=example_prompts[selected_example],
            height=100,
            key="user_prompt",
        )

        generate_button = st.button(
            f"🚀 Generate {framework.upper()} Code", key="generate_button"
        )
        if generate_button:
            if not st.session_state.api_key_provided:
                st.error("Please set your OpenRouter API Key in the sidebar")
            else:
                try:
                    with st.spinner(f"Generating your {framework} code..."):
                        # Get model name for display
                        model_name = "selected model"
                        for model in st.session_state.available_models:
                            if model["model_id"] == st.session_state.selected_model_id:
                                model_name = model["name"]
                                break

                        st.info(f"Using {model_name} to generate your code...")

                        config = generate_agents(
                            user_prompt, framework, st.session_state.selected_model_id
                        )

                        # Store the configuration in session state
                        st.session_state.config = config
                        st.session_state.code = create_code_block(config, framework)
                        st.session_state.framework = framework

                        time.sleep(0.5)  # Small delay for better UX
                        st.success(
                            f"✨ {framework.upper()} code generated successfully!"
                        )
                except Exception as e:
                    error_msg = f"Error generating code: {e}\n{traceback.format_exc()}"
                    st.session_state.error_logs.append(error_msg)
                    st.error(f"Error generating code: {e}")
                    # Display more detailed error in an expander
                    with st.expander("View Error Details"):
                        st.code(traceback.format_exc())

    with col2:
        st.subheader("💡 Framework Tips")
        if framework == "crewai":
            st.info(
                """
            **CrewAI Tips:**
            - Define clear roles for each agent
            - Set specific goals for better performance
            - Consider how agents should collaborate
            - Specify task delegation permissions
            """
            )
        elif framework == "langgraph":
            st.info(
                """
            **LangGraph Tips:**
            - Design your graph flow carefully
            - Define clear node responsibilities
            - Consider conditional routing between nodes
            - Think about how state is passed between nodes
            """
            )

    # Display results only if we have them
    if "config" in st.session_state and "code" in st.session_state:
        st.subheader("🔍 Generated Configuration")

        tab1, tab2, tab3 = st.tabs(["📊 Visual Overview", "💻 Code", "🐞 Debug"])

        # Tabs for different views
        with tab1:
            current_framework = st.session_state.framework
            render_framework_overview(st.session_state.config, current_framework)

        with tab2:
            st.code(st.session_state.code, language="python")

            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("📋 Copy Code", key="copy_button"):
                    st.toast("Code copied to clipboard! 📋")

        with tab3:
            st.subheader("Debug Information")
            st.write(
                "This section shows debugging information that can help troubleshoot issues."
            )

            with st.expander("Session State Variables"):
                st.json(
                    {
                        k: v
                        for k, v in st.session_state.items()
                        if k not in ["config", "code", "error_logs"]
                    }
                )

            with st.expander("Error Logs"):
                if st.session_state.error_logs:
                    for i, error in enumerate(st.session_state.error_logs):
                        st.text(f"Error {i+1}:\n{error}")
                else:
                    st.write("No errors logged.")

            if st.button("Clear Session State", key="clear_session"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Session state cleared! Please refresh the page.")


if __name__ == "__main__":
    main()
