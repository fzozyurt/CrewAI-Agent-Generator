import re
from typing import Dict, Any, List, Tuple
import streamlit as st
from framework.tool_utils import get_available_tools


def generate_config_from_prompt(prompt: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Generates CrewAI configuration from a natural language prompt

    Args:
        prompt: User's natural language prompt describing the desired agents and tasks

    Returns:
        Tuple containing the generated config dictionary and any warnings
    """
    config = {"agents": [], "tasks": []}
    warnings = []

    # Get available tools for validation
    available_tools = get_available_tools()

    # Try to extract agent information
    agent_blocks = re.findall(
        r"Agent[:\s]+([^#]+?)(?=\bAgent[:\s]+|\bTask[:\s]+|$)",
        prompt,
        re.IGNORECASE | re.DOTALL,
    )

    if not agent_blocks:
        warnings.append("No agents could be identified in your prompt.")

    # Process each agent block
    for i, agent_block in enumerate(agent_blocks):
        # Extract agent details
        name_match = re.search(r"name[:\s]+([^\n]+)", agent_block, re.IGNORECASE)
        role_match = re.search(r"role[:\s]+([^\n]+)", agent_block, re.IGNORECASE)
        goal_match = re.search(r"goal[:\s]+([^\n]+)", agent_block, re.IGNORECASE)
        backstory_match = re.search(
            r"backstory[:\s]+([^\n]+)", agent_block, re.IGNORECASE
        )
        tools_match = re.search(r"tool(?:s)?[:\s]+([^\n]+)", agent_block, re.IGNORECASE)

        # Set default values
        name = f"agent_{i+1}"
        if name_match:
            name = name_match.group(1).strip().replace(" ", "_")

        role = "Default Role"
        if role_match:
            role = role_match.group(1).strip()

        goal = "Default Goal"
        if goal_match:
            goal = goal_match.group(1).strip()

        backstory = ""
        if backstory_match:
            backstory = backstory_match.group(1).strip()

        # Process tools
        tools = []
        if tools_match:
            tool_text = tools_match.group(1).strip()
            potential_tools = [t.strip() for t in re.split(r"[,;]", tool_text)]

            # Validate tools
            for tool in potential_tools:
                # Try to match tool names (case insensitive and allow partial matches)
                tool_match = None
                for available_tool in available_tools.keys():
                    if (
                        available_tool.lower() == tool.lower()
                        or available_tool.lower().startswith(tool.lower())
                    ):
                        tool_match = available_tool
                        break

                if tool_match:
                    tools.append(tool_match)
                else:
                    warnings.append(
                        f"Unknown tool '{tool}' for agent '{name}'. Ignoring."
                    )

        # Create agent config
        agent = {
            "name": name,
            "role": role,
            "goal": goal,
            "backstory": backstory,
            "verbose": True,
            "allow_delegation": False,
            "tools": tools,
        }

        config["agents"].append(agent)

    # Try to extract task information
    task_blocks = re.findall(
        r"Task[:\s]+([^#]+?)(?=\bAgent[:\s]+|\bTask[:\s]+|$)",
        prompt,
        re.IGNORECASE | re.DOTALL,
    )

    if not task_blocks and config["agents"]:
        warnings.append(
            "No tasks could be identified. At least one task is recommended."
        )

    # Process each task block
    for i, task_block in enumerate(task_blocks):
        # Extract task details
        name_match = re.search(r"name[:\s]+([^\n]+)", task_block, re.IGNORECASE)
        description_match = re.search(
            r"description[:\s]+([^\n]+)", task_block, re.IGNORECASE
        )
        output_match = re.search(
            r"(expected_)?output[:\s]+([^\n]+)", task_block, re.IGNORECASE
        )
        agent_match = re.search(r"agent[:\s]+([^\n]+)", task_block, re.IGNORECASE)

        # Set default values
        name = f"task_{i+1}"
        if name_match:
            name = name_match.group(1).strip().replace(" ", "_")

        description = "Default task description"
        if description_match:
            description = description_match.group(1).strip()

        expected_output = "Task completion report"
        if output_match:
            expected_output = (
                output_match.group(2).strip()
                if output_match.group(2)
                else output_match.group(1).strip()
            )

        # Assign to agent (default to first agent if not specified)
        assigned_agent = config["agents"][0]["name"] if config["agents"] else None
        if agent_match:
            agent_name = agent_match.group(1).strip()
            # Try to find matching agent
            for agent in config["agents"]:
                if (
                    agent["name"].lower() == agent_name.lower()
                    or agent["role"].lower() == agent_name.lower()
                ):
                    assigned_agent = agent["name"]
                    break

        if not assigned_agent:
            warnings.append(
                f"Could not assign task '{name}' to an agent. No agents available."
            )
            continue

        # Create task config
        task = {
            "name": name,
            "description": description,
            "expected_output": expected_output,
            "agent": assigned_agent,
        }

        config["tasks"].append(task)

    return config, warnings


def analyze_prompt_completeness(prompt: str) -> Dict[str, Any]:
    """
    Analyzes a prompt to determine what information might be missing

    Args:
        prompt: User's natural language prompt

    Returns:
        Dictionary with analysis results
    """
    results = {
        "has_agents": False,
        "has_tasks": False,
        "has_tools": False,
        "missing_fields": [],
    }

    # Check for agent indicators
    results["has_agents"] = bool(re.search(r"\bagent[s]?[\s:]+", prompt, re.IGNORECASE))

    # Check for task indicators
    results["has_tasks"] = bool(re.search(r"\btask[s]?[\s:]+", prompt, re.IGNORECASE))

    # Check for tool indicators
    results["has_tools"] = bool(re.search(r"\btool[s]?[\s:]+", prompt, re.IGNORECASE))

    # Check for agent roles
    if not re.search(r"\brole[\s:]+", prompt, re.IGNORECASE) and results["has_agents"]:
        results["missing_fields"].append("Agent roles")

    # Check for agent goals
    if not re.search(r"\bgoal[\s:]+", prompt, re.IGNORECASE) and results["has_agents"]:
        results["missing_fields"].append("Agent goals")

    # Check for task descriptions
    if (
        not re.search(r"\bdescription[\s:]+", prompt, re.IGNORECASE)
        and results["has_tasks"]
    ):
        results["missing_fields"].append("Task descriptions")

    return results


def get_prompt_suggestions() -> List[str]:
    """Returns a list of example prompts"""
    return [
        """
Create a research crew with:
Agent: name: researcher role: Research Specialist goal: Find comprehensive information on AI safety backstory: Expert in data analysis tools: SerperDevTool, WikipediaSearchTool
Agent: name: writer role: Content Writer goal: Create engaging articles backstory: Former journalist with 10 years experience tools: WebsiteSearchTool
Task: name: gather_data description: Find the latest research on AI safety agent: researcher
Task: name: write_article description: Write a 1000-word article on AI safety expected_output: Complete article with citations agent: writer
        """,
        """
I need a web development team:
Agent: name: frontend role: Frontend Developer goal: Build responsive UI backstory: 5 years of React experience tools: FileReadTool
Agent: name: backend role: Backend Developer goal: Create robust API backstory: Expert in Python and databases tools: PythonReplTool
Task: name: design_ui description: Create wireframes for the application agent: frontend
Task: name: implement_api description: Develop RESTful API endpoints agent: backend
        """,
        """
Create a market research crew:
Agent: role: Market Analyst goal: Analyze competitor products tools: SerperDevTool, WebsiteSearchTool
Agent: role: Customer Research Specialist goal: Gather customer feedback tools: FileReadTool
Task: description: Research top 5 competitors in the market agent: Market Analyst 
Task: description: Compile a report of customer preferences agent: Customer Research Specialist
        """,
    ]


def get_prompt_template() -> str:
    """Returns a template for creating agents and tasks"""
    return """# Define your agents and tasks below

Agent:
name: agent_name
role: Agent Role Title
goal: What the agent aims to accomplish
backstory: Background information about the agent
tools: SerperDevTool, WebsiteSearchTool

Task:
name: task_name
description: Detailed description of what needs to be done
expected_output: What the completed task should deliver
agent: agent_name

# You can add more agents and tasks following the same format
"""
