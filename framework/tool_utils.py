class ToolExecutionContext:
    """Context for tool execution."""

    def __init__(self):
        self.state = {}

    def get_state(self, key, default=None):
        return self.state.get(key, default)

    def set_state(self, key, value):
        self.state[key] = value


def parse_tool_response(response):
    """Parse a tool response string."""
    if not response:
        return None
    return response


def format_tool_input(input_data):
    """Format data as input for a tool."""
    if isinstance(input_data, dict):
        return input_data
    elif isinstance(input_data, str):
        return {"input": input_data}
    else:
        return {"data": input_data}


def get_tool_by_name(name, tool_registry=None):
    """Get a tool by its name from the registry."""
    if not tool_registry:
        return None
    return tool_registry.get(name)


def get_available_tools():
    """
    Get a dictionary of available CrewAI tools with their configurations
    """
    return {
        "SerperDevTool": {
            "description": "Serper.dev API for web search",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Serper.dev API key",
                    "required": True,
                },
                "search_type": {
                    "type": "str",
                    "description": "Type of search (search/images/news)",
                    "default": "search",
                    "required": False,
                },
                "include_answer": {
                    "type": "bool",
                    "description": "Whether to include an answer",
                    "default": False,
                    "required": False,
                },
                "include_images": {
                    "type": "bool",
                    "description": "Whether to include images",
                    "default": False,
                    "required": False,
                },
                "num_results": {
                    "type": "int",
                    "description": "Number of search results",
                    "default": 10,
                    "required": False,
                },
            },
        },
        "SearXSearchTool": {
            "description": "SearX meta search engine tool",
            "parameters": {
                "searx_host": {
                    "type": "str",
                    "description": "SearX host address",
                    "required": True,
                },
                "engines": {
                    "type": "list",
                    "description": "Search engines to use",
                    "required": False,
                },
                "num_results": {
                    "type": "int",
                    "description": "Number of search results",
                    "default": 10,
                    "required": False,
                },
                "language": {
                    "type": "str",
                    "description": "Language for search results",
                    "default": "en",
                    "required": False,
                },
            },
        },
        "GoogleSearchTool": {
            "description": "Google Search API tool",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Google Search API key",
                    "required": True,
                },
                "cse_id": {
                    "type": "str",
                    "description": "Custom Search Engine ID",
                    "required": True,
                },
                "num_results": {
                    "type": "int",
                    "description": "Number of search results",
                    "default": 10,
                    "required": False,
                },
            },
        },
        "BrowserTool": {
            "description": "Browser tool for web browsing and scraping",
            "parameters": {
                "headless": {
                    "type": "bool",
                    "description": "Run browser in headless mode",
                    "default": True,
                    "required": False,
                },
                "browser_type": {
                    "type": "str",
                    "description": "Browser type to use",
                    "default": "chromium",
                    "required": False,
                },
                "proxy": {
                    "type": "str",
                    "description": "Proxy server to use",
                    "required": False,
                },
            },
        },
        "FileReadTool": {
            "description": "Tool to read file contents",
            "parameters": {
                "file_path": {
                    "type": "str",
                    "description": "Path to file to read",
                    "required": True,
                },
                "encoding": {
                    "type": "str",
                    "description": "File encoding",
                    "default": "utf-8",
                    "required": False,
                },
            },
        },
        "FileWriteTool": {
            "description": "Tool to write content to files",
            "parameters": {
                "directory_path": {
                    "type": "str",
                    "description": "Directory to write files to",
                    "required": True,
                },
                "overwrite": {
                    "type": "bool",
                    "description": "Whether to overwrite existing files",
                    "default": False,
                    "required": False,
                },
            },
        },
        "PythonREPLTool": {
            "description": "Python REPL for executing code",
            "parameters": {
                "timeout": {
                    "type": "int",
                    "description": "Timeout in seconds for code execution",
                    "default": 10,
                    "required": False,
                },
            },
        },
        "TavilySearchTool": {
            "description": "Tavily AI search API",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Tavily API key",
                    "required": True,
                },
                "search_depth": {
                    "type": "str",
                    "description": "Search depth (basic/advanced)",
                    "default": "basic",
                    "required": False,
                },
                "max_results": {
                    "type": "int",
                    "description": "Maximum number of results",
                    "default": 5,
                    "required": False,
                },
                "include_answer": {
                    "type": "bool",
                    "description": "Whether to include an answer",
                    "default": True,
                    "required": False,
                },
                "include_images": {
                    "type": "bool",
                    "description": "Whether to include images",
                    "default": False,
                    "required": False,
                },
                "include_raw_content": {
                    "type": "bool",
                    "description": "Whether to include raw content",
                    "default": False,
                    "required": False,
                },
            },
        },
        "BrowserbaseLoadTool": {
            "description": "A tool for interacting with and extracting data from web browsers",
            "parameters": {
                "url": {
                    "type": "str",
                    "description": "URL to load in the browser",
                    "required": True,
                },
                "browserbase_key": {
                    "type": "str",
                    "description": "Your Browserbase API key",
                    "required": True,
                },
            },
        },
        "CodeDocsSearchTool": {
            "description": "A RAG tool optimized for searching through code documentation and related technical documents",
            "parameters": {
                "docs_path": {
                    "type": "str",
                    "description": "Path to code documentation",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top documents to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "CodeInterpreterTool": {
            "description": "A tool for interpreting python code",
            "parameters": {
                "allow_filesystem_access": {
                    "type": "bool",
                    "description": "Whether to allow filesystem access",
                    "default": True,
                    "required": False,
                },
                "allow_network_access": {
                    "type": "bool",
                    "description": "Whether to allow network access",
                    "default": False,
                    "required": False,
                },
            },
        },
        "ComposioTool": {
            "description": "Enables use of Composio tools",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Composio API key",
                    "required": True,
                },
                "tool_name": {
                    "type": "str",
                    "description": "Name of the Composio tool to use",
                    "required": True,
                },
            },
        },
        "CSVSearchTool": {
            "description": "A RAG tool designed for searching within CSV files, tailored to handle structured data",
            "parameters": {
                "csv_file": {
                    "type": "str",
                    "description": "Path to CSV file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top records to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "DALL-E Tool": {
            "description": "A tool for generating images using the DALL-E API",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your OpenAI API key",
                    "required": True,
                },
                "model": {
                    "type": "str",
                    "description": "DALL-E model to use",
                    "default": "dall-e-3",
                    "required": False,
                },
                "size": {
                    "type": "str",
                    "description": "Image size (1024x1024, 1792x1024, etc.)",
                    "default": "1024x1024",
                    "required": False,
                },
                "quality": {
                    "type": "str",
                    "description": "Image quality (standard/hd)",
                    "default": "standard",
                    "required": False,
                },
            },
        },
        "DirectorySearchTool": {
            "description": "A RAG tool for searching within directories, useful for navigating through file systems",
            "parameters": {
                "directory_path": {
                    "type": "str",
                    "description": "Directory path to search",
                    "required": True,
                },
                "recursive": {
                    "type": "bool",
                    "description": "Whether to search recursively",
                    "default": True,
                    "required": False,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top results to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "DOCXSearchTool": {
            "description": "A RAG tool aimed at searching within DOCX documents, ideal for processing Word files",
            "parameters": {
                "docx_file": {
                    "type": "str",
                    "description": "Path to DOCX file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top sections to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "DirectoryReadTool": {
            "description": "Facilitates reading and processing of directory structures and their contents",
            "parameters": {
                "directory_path": {
                    "type": "str",
                    "description": "Directory path to read",
                    "required": True,
                },
                "recursive": {
                    "type": "bool",
                    "description": "Whether to read recursively",
                    "default": False,
                    "required": False,
                },
                "file_pattern": {
                    "type": "str",
                    "description": "File pattern to match (glob)",
                    "required": False,
                },
            },
        },
        "EXASearchTool": {
            "description": "A tool designed for performing exhaustive searches across various data sources",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your EXA API key",
                    "required": True,
                },
                "num_results": {
                    "type": "int",
                    "description": "Number of search results",
                    "default": 10,
                    "required": False,
                },
                "use_highlights": {
                    "type": "bool",
                    "description": "Whether to include highlights",
                    "default": False,
                    "required": False,
                },
            },
        },
        "FirecrawlSearchTool": {
            "description": "A tool to search webpages using Firecrawl and return the results",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Firecrawl API key",
                    "required": True,
                },
                "max_results": {
                    "type": "int",
                    "description": "Maximum number of search results",
                    "default": 10,
                    "required": False,
                },
            },
        },
        "FirecrawlCrawlWebsiteTool": {
            "description": "A tool for crawling webpages using Firecrawl",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Firecrawl API key",
                    "required": True,
                },
                "url": {
                    "type": "str",
                    "description": "Website URL to crawl",
                    "required": True,
                },
                "max_pages_to_crawl": {
                    "type": "int",
                    "description": "Maximum number of pages to crawl",
                    "default": 100,
                    "required": False,
                },
                "max_depth": {
                    "type": "int",
                    "description": "Maximum depth for crawling",
                    "default": 10,
                    "required": False,
                },
                "enable_javascript": {
                    "type": "bool",
                    "description": "Whether to enable JavaScript",
                    "default": True,
                    "required": False,
                },
            },
        },
        "FirecrawlScrapeWebsiteTool": {
            "description": "A tool for scraping webpages URL using Firecrawl and returning its contents",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your Firecrawl API key",
                    "required": True,
                },
                "url": {
                    "type": "str",
                    "description": "Website URL to scrape",
                    "required": True,
                },
                "enable_javascript": {
                    "type": "bool",
                    "description": "Whether to enable JavaScript",
                    "default": True,
                    "required": False,
                },
            },
        },
        "GithubSearchTool": {
            "description": "A RAG tool for searching within GitHub repositories, useful for code and documentation search",
            "parameters": {
                "token": {
                    "type": "str",
                    "description": "GitHub personal access token",
                    "required": True,
                },
                "repo": {
                    "type": "str",
                    "description": "GitHub repository in format 'owner/repo'",
                    "required": True,
                },
                "branch": {
                    "type": "str",
                    "description": "Repository branch to search",
                    "default": "main",
                    "required": False,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top results to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "TXTSearchTool": {
            "description": "A RAG tool focused on searching within text (.txt) files, suitable for unstructured data",
            "parameters": {
                "txt_file": {
                    "type": "str",
                    "description": "Path to text file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top chunks to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "JSONSearchTool": {
            "description": "A RAG tool designed for searching within JSON files, catering to structured data handling",
            "parameters": {
                "json_file": {
                    "type": "str",
                    "description": "Path to JSON file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top results to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "LlamaIndexTool": {
            "description": "Enables the use of LlamaIndex tools",
            "parameters": {
                "index_path": {
                    "type": "str",
                    "description": "Path to LlamaIndex index",
                    "required": True,
                },
                "query_engine_kwargs": {
                    "type": "dict",
                    "description": "Additional arguments for the query engine",
                    "required": False,
                },
            },
        },
        "MDXSearchTool": {
            "description": "A RAG tool tailored for searching within Markdown (MDX) files, useful for documentation",
            "parameters": {
                "mdx_file": {
                    "type": "str",
                    "description": "Path to MDX file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top sections to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "PDFSearchTool": {
            "description": "A RAG tool aimed at searching within PDF documents, ideal for processing scanned documents",
            "parameters": {
                "pdf_file": {
                    "type": "str",
                    "description": "Path to PDF file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top sections to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "PGSearchTool": {
            "description": "A RAG tool optimized for searching within PostgreSQL databases, suitable for database queries",
            "parameters": {
                "connection_string": {
                    "type": "str",
                    "description": "PostgreSQL connection string",
                    "required": True,
                },
                "table_name": {
                    "type": "str",
                    "description": "Database table name",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top results to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "Vision Tool": {
            "description": "A tool for generating images using the DALL-E API",
            "parameters": {
                "api_key": {
                    "type": "str",
                    "description": "Your OpenAI API key",
                    "required": True,
                },
                "model": {
                    "type": "str",
                    "description": "Vision model to use",
                    "default": "gpt-4-vision-preview",
                    "required": False,
                },
            },
        },
        "RagTool": {
            "description": "A general-purpose RAG tool capable of handling various data sources and types",
            "parameters": {
                "data_source": {
                    "type": "str",
                    "description": "Source of data for RAG",
                    "required": True,
                },
                "embeddings_model": {
                    "type": "str",
                    "description": "Model to use for embeddings",
                    "required": False,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top results to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "ScrapeElementFromWebsiteTool": {
            "description": "Enables scraping specific elements from websites, useful for targeted data extraction",
            "parameters": {
                "url": {
                    "type": "str",
                    "description": "Website URL to scrape elements from",
                    "required": True,
                },
                "selector": {
                    "type": "str",
                    "description": "CSS selector for the element",
                    "required": True,
                },
                "headless": {
                    "type": "bool",
                    "description": "Whether to run browser in headless mode",
                    "default": True,
                    "required": False,
                },
                "wait_for": {
                    "type": "float",
                    "description": "Time to wait for page load in seconds",
                    "default": 0,
                    "required": False,
                },
            },
        },
        "ScrapeWebsiteTool": {
            "description": "Facilitates scraping entire websites, ideal for comprehensive data collection",
            "parameters": {
                "url": {
                    "type": "str",
                    "description": "Website URL to scrape",
                    "required": True,
                },
                "headless": {
                    "type": "bool",
                    "description": "Whether to run browser in headless mode",
                    "default": True,
                    "required": False,
                },
                "wait_for": {
                    "type": "float",
                    "description": "Time to wait for page load in seconds",
                    "default": 0,
                    "required": False,
                },
            },
        },
        "WebsiteSearchTool": {
            "description": "A RAG tool for searching website content, optimized for web data extraction",
            "parameters": {
                "url": {
                    "type": "str",
                    "description": "Website URL to search",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top results to retrieve",
                    "default": 5,
                    "required": False,
                },
                "enable_javascript": {
                    "type": "bool",
                    "description": "Whether to enable JavaScript",
                    "default": True,
                    "required": False,
                },
            },
        },
        "XMLSearchTool": {
            "description": "A RAG tool designed for searching within XML files, suitable for structured data formats",
            "parameters": {
                "xml_file": {
                    "type": "str",
                    "description": "Path to XML file",
                    "required": True,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top elements to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
        "YoutubeChannelSearchTool": {
            "description": "A RAG tool for searching within YouTube channels, useful for video content analysis",
            "parameters": {
                "channel_id": {
                    "type": "str",
                    "description": "YouTube channel ID",
                    "required": True,
                },
                "api_key": {
                    "type": "str",
                    "description": "YouTube API key",
                    "required": True,
                },
                "max_results": {
                    "type": "int",
                    "description": "Maximum number of results",
                    "default": 10,
                    "required": False,
                },
                "caption_language": {
                    "type": "str",
                    "description": "Language for captions",
                    "default": "en",
                    "required": False,
                },
            },
        },
        "YoutubeVideoSearchTool": {
            "description": "A RAG tool aimed at searching within YouTube videos, ideal for video data extraction",
            "parameters": {
                "video_id": {
                    "type": "str",
                    "description": "YouTube video ID",
                    "required": True,
                },
                "api_key": {
                    "type": "str",
                    "description": "YouTube API key",
                    "required": True,
                },
                "caption_language": {
                    "type": "str",
                    "description": "Language for captions",
                    "default": "en",
                    "required": False,
                },
                "top_k": {
                    "type": "int",
                    "description": "Number of top sections to retrieve",
                    "default": 5,
                    "required": False,
                },
            },
        },
    }


def get_tool_description(tool_name):
    """
    Get the description of a specific tool

    Args:
        tool_name: Name of the tool

    Returns:
        String description of the tool or None if tool doesn't exist
    """
    tools = get_available_tools()
    if tool_name in tools:
        return tools[tool_name]["description"]
    return None


def validate_tool_parameters(tool_name, parameters):
    """
    Validate the parameters for a specific tool

    Args:
        tool_name: Name of the tool
        parameters: Dictionary of parameter values

    Returns:
        List of error messages, empty if validation passed
    """
    errors = []
    tools = get_available_tools()

    if tool_name not in tools:
        return ["Invalid tool name"]

    tool_config = tools[tool_name]
    expected_params = tool_config["parameters"]

    # Check for required parameters
    for param_name, param_config in expected_params.items():
        if param_config.get("required", False):
            if param_name not in parameters or not parameters[param_name]:
                errors.append(f"Missing required parameter: {param_name}")

    # Type validation
    for param_name, value in parameters.items():
        if param_name in expected_params:
            param_type = expected_params[param_name]["type"]

            # Skip empty optional parameters
            if not value and not expected_params[param_name].get("required", False):
                continue

            # Type validation
            if param_type == "int" and not isinstance(value, int):
                try:
                    int(value)
                except (ValueError, TypeError):
                    errors.append(f"Parameter {param_name} must be an integer")
            elif param_type == "float" and not isinstance(value, float):
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors.append(f"Parameter {param_name} must be a float")
            elif param_type == "bool" and not isinstance(value, bool):
                errors.append(f"Parameter {param_name} must be a boolean")

    return errors


def format_tool_for_config(tool_name, parameters):
    """
    Format a tool configuration for CrewAI

    Args:
        tool_name: Name of the tool
        parameters: Dictionary of parameter values

    Returns:
        Dictionary with tool configuration
    """
    tools = get_available_tools()
    tool_config = tools.get(tool_name, {})

    # Clean parameters
    clean_params = {}
    for name, value in parameters.items():
        # Skip empty parameters
        if value == "" or value is None:
            continue
        clean_params[name] = value

    # Format based on tool class name
    formatted_config = {"type": tool_name, **clean_params}

    return formatted_config


def get_tool_env_requirements(tool_name=None):
    """
    Get environment requirements for tools

    Args:
        tool_name: Optional name of specific tool to get requirements for,
                  or a list of tool names

    Returns:
        List of dictionaries with 'env_var' and 'description' keys
    """
    # Define environment requirements for each tool
    env_requirements = {
        "SerperDevTool": [
            {
                "env_var": "SERPER_API_KEY",
                "description": "API key for Serper.dev search service",
            }
        ],
        "GoogleSearchTool": [
            {"env_var": "GOOGLE_API_KEY", "description": "API key for Google Search"},
            {
                "env_var": "GOOGLE_CSE_ID",
                "description": "Custom Search Engine ID for Google Search",
            },
        ],
        "TavilySearchTool": [
            {
                "env_var": "TAVILY_API_KEY",
                "description": "API key for Tavily Search API",
            }
        ],
        "BrowserbaseLoadTool": [
            {
                "env_var": "BROWSERBASE_API_KEY",
                "description": "API key for Browserbase",
            }
        ],
        "ComposioTool": [
            {
                "env_var": "COMPOSIO_API_KEY",
                "description": "API key for Composio",
            }
        ],
        "DALL-E Tool": [
            {
                "env_var": "OPENAI_API_KEY",
                "description": "API key for OpenAI DALL-E",
            }
        ],
        "EXASearchTool": [
            {
                "env_var": "EXA_API_KEY",
                "description": "API key for EXA search service",
            }
        ],
        "FirecrawlSearchTool": [
            {
                "env_var": "FIRECRAWL_API_KEY",
                "description": "API key for Firecrawl search service",
            }
        ],
        "FirecrawlCrawlWebsiteTool": [
            {
                "env_var": "FIRECRAWL_API_KEY",
                "description": "API key for Firecrawl crawl service",
            }
        ],
        "FirecrawlScrapeWebsiteTool": [
            {
                "env_var": "FIRECRAWL_API_KEY",
                "description": "API key for Firecrawl scrape service",
            }
        ],
        "GithubSearchTool": [
            {
                "env_var": "GITHUB_TOKEN",
                "description": "Personal access token for GitHub",
            }
        ],
        "Vision Tool": [
            {
                "env_var": "OPENAI_API_KEY",
                "description": "API key for OpenAI Vision API",
            }
        ],
        "YoutubeChannelSearchTool": [
            {
                "env_var": "YOUTUBE_API_KEY",
                "description": "API key for YouTube Data API",
            }
        ],
        "YoutubeVideoSearchTool": [
            {
                "env_var": "YOUTUBE_API_KEY",
                "description": "API key for YouTube Data API",
            }
        ],
        "BrowserTool": [],
        "CodeDocsSearchTool": [],
        "CodeInterpreterTool": [],
        "CSVSearchTool": [],
        "DirectorySearchTool": [],
        "DOCXSearchTool": [],
        "DirectoryReadTool": [],
        "FileReadTool": [],
        "FileWriteTool": [],
        "JSONSearchTool": [],
        "LlamaIndexTool": [],
        "MDXSearchTool": [],
        "PDFSearchTool": [],
        "PGSearchTool": [
            {
                "env_var": "DATABASE_URL",
                "description": "PostgreSQL connection string",
            }
        ],
        "PythonREPLTool": [],
        "RagTool": [],
        "ScrapeElementFromWebsiteTool": [],
        "ScrapeWebsiteTool": [],
        "SearXSearchTool": [],
        "TXTSearchTool": [],
        "WebsiteSearchTool": [],
        "XMLSearchTool": [],
    }

    # Handle different input types
    if tool_name is None:
        # Return all requirements as a flat list
        all_requirements = []
        for tool_reqs in env_requirements.values():
            all_requirements.extend(tool_reqs)
        return all_requirements
    elif isinstance(tool_name, list):
        # Return requirements for a list of tools
        combined_requirements = []
        for tool in tool_name:
            if tool in env_requirements:
                combined_requirements.extend(env_requirements[tool])
        return combined_requirements
    else:
        # Return requirements for a single tool
        return env_requirements.get(tool_name, [])
