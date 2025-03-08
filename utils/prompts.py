from typing import Dict, Any


def get_system_prompt_for_framework(framework: str) -> str:
    """Returns the system prompt for the specified framework."""
    if framework == "crewai":
        return """
        You are an expert at creating AI research assistants using CrewAI. Based on the user's request,
        suggest appropriate agents, their roles, tools, and tasks. Format your response as JSON with this structure:
        {
            "agents": [
                {
                    "name": "agent name",
                    "role": "specific role description",
                    "goal": "clear goal",
                    "backstory": "relevant backstory",
                    "tools": ["tool1", "tool2"],
                    "verbose": true,
                    "allow_delegation": true/false
                }
            ],
            "tasks": [
                {
                    "name": "task name",
                    "description": "detailed description",
                    "tools": ["required tools"],
                    "agent": "agent name",
                    "expected_output": "specific expected output"
                }
            ]
        }
        """
    elif framework == "langgraph":
        return """
        You are an expert at creating AI agents using LangChain's LangGraph framework. Based on the user's request,
        suggest appropriate agents, their roles, tools, and nodes for the graph. Format your response as JSON with this structure:
        {
            "agents": [
                {
                    "name": "agent name",
                    "role": "specific role description",
                    "goal": "clear goal",
                    "tools": ["tool1", "tool2"],
                    "llm": "model name (e.g., gpt-4)"
                }
            ],
            "nodes": [
                {
                    "name": "node name",
                    "description": "detailed description",
                    "agent": "agent name"
                }
            ],
            "edges": [
                {
                    "source": "source node name",
                    "target": "target node name",
                    "condition": "condition description (optional)"
                }
            ]
        }
        """
    else:
        return """
        You are an expert at creating AI research assistants. Based on the user's request,
        suggest appropriate agents, their roles, tools, and tasks.
        """


def get_framework_description(framework: str) -> str:
    """Returns the description for the specified framework."""
    framework_descriptions = {
        "crewai": """
        **CrewAI** is a framework for orchestrating role-playing autonomous AI agents. 
        It allows you to create a crew of agents that work together to accomplish tasks, 
        with each agent having a specific role, goal, and backstory.
        """,
        "langgraph": """
        **LangGraph** is LangChain's framework for building stateful, multi-actor applications with LLMs.
        It provides a way to create directed graphs where nodes are LLM calls, tools, or other operations, 
        and edges represent the flow of information between them.
        """,
    }
    return framework_descriptions.get(framework, "")


def get_example_prompts() -> Dict[str, str]:
    """Returns example prompts for different use cases."""
    return {
        "Research Assistant": "I need a research assistant that summarizes papers and answers questions",
        "Content Creation": "I need a team to create viral social media content and manage our brand presence",
        "Data Analysis": "I need a team to analyze customer data and create visualizations",
        "Technical Writing": "I need a team to create technical documentation and API guides",
        "IT Incident Analysis": "I need agents to analyze IT incidents, determine root causes, and recommend preventive measures",
        "Financial Analysis": "I need a team to analyze financial data, identify trends, and make investment recommendations",
        "Tourism Analysis": "I need agents to analyze tourism trends, popular destinations, and create travel packages",
        "Web Customer Analysis": "I need agents to analyze web traffic, identify potential customers, and suggest conversion strategies",
        "Product Development": "I need a team to brainstorm product ideas, analyze market fit, and create development roadmaps",
        "Market Research": "I need agents to conduct competitive analysis and identify market opportunities in the tech sector",
        "Educational Content": "I need a team to develop interactive learning materials for programming courses",
        "Security Audit": "I need agents to perform security assessments, identify vulnerabilities, and suggest mitigations",
    }


def get_default_config(framework: str) -> Dict[str, Any]:
    """Returns default configuration for the specified framework when model generation fails."""
    if framework == "crewai":
        return {
            "agents": [
                {
                    "name": "default_assistant",
                    "role": "General Assistant",
                    "goal": "Help with basic tasks",
                    "backstory": "Versatile assistant with general knowledge",
                    "tools": ["basic_tool"],
                    "verbose": True,
                    "allow_delegation": False,
                }
            ],
            "tasks": [
                {
                    "name": "basic_task",
                    "description": "Handle basic requests",
                    "tools": ["basic_tool"],
                    "agent": "default_assistant",
                    "expected_output": "Task completion",
                }
            ],
        }
    elif framework == "langgraph":
        return {
            "agents": [
                {
                    "name": "default_assistant",
                    "role": "General Assistant",
                    "goal": "Help with basic tasks",
                    "tools": ["basic_tool"],
                    "llm": "gpt-4",
                }
            ],
            "nodes": [
                {
                    "name": "process_input",
                    "description": "Process user input",
                    "agent": "default_assistant",
                }
            ],
            "edges": [
                {
                    "source": "process_input",
                    "target": "END",
                    "condition": "task completed",
                }
            ],
        }
    else:
        return {}
