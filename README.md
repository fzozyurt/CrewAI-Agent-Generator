# Crew-Agent-Generator

A Streamlit application that helps you generate agent code for different frameworks (CrewAI and LangGraph) based on natural language requirements.

## 🚀 Overview

This tool allows you to:
- Describe your agent requirements in natural language
- Choose between CrewAI and LangGraph frameworks
- Get automatically generated Python code for your agent system
- Visualize the agents, tasks, and relationships

## 📋 Features

- **Multi-Framework Support**: Generate code for CrewAI or LangGraph
- **OpenRouter Integration**: Access to various LLM models through OpenRouter
- **Interactive UI**: Visualize your agent configurations
- **Example Prompts**: Pre-defined examples to get started quickly
- **Langfuse Integration**: Optional tracing and analytics

## 🔧 Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/fzozyurt/CrewAI-Agent-Generator.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   
   # Optional Langfuse integration
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```

## 🔑 OpenRouter API Key

To use this application, you need an OpenRouter API key. Follow these steps to get one:

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account or log in
3. Go to API Keys section from your dashboard
4. Create a new API key
5. Copy the key and add it to your `.env` file or enter it directly in the app

### Free Models on OpenRouter

OpenRouter provides access to several free models that can be used with this application. These free models have `:free` suffix in their identifiers. Some popular free models include:

- **DeepSeek R1** (`deepseek/deepseek-coder:free`) 
- **Google Gemini Pro 2.0 Experimental** (`google/gemini-2.0-pro-exp-02-05:free`)
- **Google Gemma2 9B** (`google/gemma-2-9b-it:free`)
- **Qwen 2.5 VL** (`qwen/qwen-2.5-vl:free`)
- **Phi-3 Mini 128K** (`microsoft/phi-3-mini-128k-instruct:free`)

The application automatically displays available free models when you check the "Only show free models" option in the sidebar.

While free models have usage limitations, they provide enough tokens for generating agent code in this application.

## 🚀 Running the Application

To run the Streamlit app:

```bash
streamlit run app.py
```

If your environment variables are not set in the `.env` file, you can enter your OpenRouter API key directly in the sidebar of the application.

## 🧠 Using the Application

1. **Select a Framework**: Choose between CrewAI and LangGraph
2. **Choose an AI Model**: Select from available models (free or paid)
3. **Define Requirements**: Describe what you need or select from example prompts
4. **Generate Code**: Click the generate button to create your agent code
5. **Explore Results**: View the visual overview, code, and debug information

## 🔗 Framework Information

### CrewAI
CrewAI is designed for creating role-playing autonomous AI agents that work together to accomplish tasks. Each agent has a specific role, goal, and backstory.

### LangGraph
LangGraph is LangChain's framework for building stateful, multi-actor applications with LLMs. It creates directed graphs where nodes are LLM calls, tools, or other operations.

## ⚠️ Notes

- The application uses HTTPS requests with `verify=False`. This is not recommended for production environments.
- Make sure to keep your API keys secure and do not share them.
- The generated code may require additional modifications based on your specific use case.

## 🛠️ Troubleshooting

- **API Key Issues**: If you're having issues with your OpenRouter API key, verify it on the OpenRouter website.
- **Model Loading Errors**: Some models might not be available or might require additional permissions.
- **Code Generation Failures**: Try rephrasing your requirements or using one of the example prompts.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```</body>