from .crewai_generator import create_crewai_code, render_crewai_overview
from .langgraph_generator import create_langgraph_code, render_langgraph_overview


def create_code_block(config, framework):
    """Factory function to create code for the selected framework"""
    if framework == "crewai":
        return create_crewai_code(config)
    elif framework == "langgraph":
        return create_langgraph_code(config)
    else:
        return "# Invalid framework specified"


def render_framework_overview(config, framework):
    """Factory function to render visual overview for the selected framework"""
    if framework == "crewai":
        return render_crewai_overview(config)
    elif framework == "langgraph":
        return render_langgraph_overview(config)
