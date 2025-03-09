# Integrating LangChain Tools with CrewAI

CrewAI supports integration with LangChain tools, allowing you to use a wide range of additional capabilities in your agent workflows. This guide demonstrates how to integrate LangChain tools into your CrewAI agents.

## Basic Integration Pattern

To integrate a LangChain tool with CrewAI, you need to create a wrapper class that inherits from `BaseTool`. This is critical for proper functioning in the CrewAI framework.

### Required Pattern

```python
from langchain.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import SomeUtility

class MyLangChainTool(BaseTool):
    name: str = "ToolName" 
    description: str = "Description of what this tool does"
    utility_attribute: SomeUtility = Field(default_factory=SomeUtility)
    
    def _run(self, query: str) -> str:
        try:
            return self.utility_attribute.run(query)
        except Exception as e:
            return f"Error: {str(e)}"
```

Key elements of this pattern:
1. Inherit from `BaseTool`
2. Define `name` and `description` attributes
3. Use `Field(default_factory=...)` for instantiating the utility
4. Implement the `_run` method that calls the utility's method

## Example: Google Serper Search Tool

Here's a concrete example using Google Serper API for search capabilities:

```python
from crewai import Agent, Task, Crew
from langchain.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a search tool using GoogleSerperAPIWrapper
class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find current information about markets, companies, and trends."
    search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper)

    def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

# Create an agent with the search tool
researcher = Agent(
    role="Research Analyst",
    goal="Gather current market data and trends",
    backstory="""You are an expert research analyst with years of experience in
    gathering market intelligence. You're known for your ability to find
    relevant and up-to-date market information and present it in a clear,
    actionable format.""",
    tools=[SearchTool()],
    verbose=True
)

# Define a task for the agent
research_task = Task(
    description="Research the current market trends for electric vehicles and provide a summary of key findings",
    agent=researcher
)

# Create a crew with the agent
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=2
)

# Run the crew
result = crew.kickoff()
print(result)
```

## Common LangChain Tool Integration Examples

### Wikipedia Search

```python
from langchain.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import WikipediaAPIWrapper

class WikipediaTool(BaseTool):
    name: str = "Wikipedia"
    description: str = "Useful for retrieving information from Wikipedia about concepts, historical events, people, and places."
    wiki: WikipediaAPIWrapper = Field(default_factory=WikipediaAPIWrapper)

    def _run(self, query: str) -> str:
        try:
            return self.wiki.run(query)
        except Exception as e:
            return f"Error searching Wikipedia: {str(e)}"
```

### Wolfram Alpha Calculations

```python
from langchain.tools import BaseTool
from pydantic import Field
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

class WolframAlphaTool(BaseTool):
    name: str = "WolframAlpha"
    description: str = "Useful for mathematical calculations, unit conversions, and factual questions about physics, chemistry, geography, etc."
    wolfram: WolframAlphaAPIWrapper = Field(default_factory=WolframAlphaAPIWrapper)

    def _run(self, query: str) -> str:
        try:
            return self.wolfram.run(query)
        except Exception as e:
            return f"Error with Wolfram Alpha calculation: {str(e)}"
```

### Weather Information

```python
from langchain.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import OpenWeatherMapAPIWrapper

class WeatherTool(BaseTool):
    name: str = "Weather"
    description: str = "Useful for retrieving current weather information for a specific location."
    weather: OpenWeatherMapAPIWrapper = Field(default_factory=OpenWeatherMapAPIWrapper)

    def _run(self, query: str) -> str:
        try:
            return self.weather.run(query)
        except Exception as e:
            return f"Error retrieving weather information: {str(e)}"
```

## Environment Variables

Many LangChain tools require API keys or other credentials. Always ensure you have the required environment variables set in your `.env` file:

```
SERPER_API_KEY=your_serper_api_key
SERPAPI_API_KEY=your_serpapi_api_key
OPENAI_API_KEY=your_openai_api_key
WOLFRAM_ALPHA_APPID=your_wolfram_alpha_appid
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
BING_SUBSCRIPTION_KEY=your_bing_subscription_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
```

## Helper Functions for Tool Generation

The `tool_utils.py` file includes helpful functions for generating tool classes automatically:

```python
# Get code for a tool class
tool_code = generate_langchain_tool_class("GoogleSerperAPIWrapper")
print(tool_code)

# Get integration example for a tool
example = get_langchain_integration_example("WikipediaAPIWrapper")
print(example)
```

## Available LangChain Tools

The system includes many LangChain tools that you can integrate with CrewAI:

1. **Search Tools**:
   - `GoogleSerperAPIWrapper` - Google search via Serper API
   - `SerpAPI` - Search engine results via SerpAPI
   - `BingSearchAPIWrapper` - Bing search
   - `GoogleSearchAPIWrapper` - Google Custom Search

2. **Knowledge Tools**:
   - `WikipediaAPIWrapper` - Wikipedia article search
   - `ArxivAPIWrapper` - Academic paper search
   - `PubMed` - Medical research paper search

3. **Computational Tools**:
   - `WolframAlphaAPIWrapper` - Math & knowledge engine

4. **Utility Tools**:
   - `OpenWeatherMapAPIWrapper` - Weather information
   - `DALLE3` - Image generation
   - `HumanInputRun` - Ask for human input

For a complete list and implementation examples, check the `tool_utils.py` file in the framework directory.
