import requests
from typing import List, Dict, Optional


def get_openrouter_models(free_only: bool = False) -> List[Dict]:
    """
    Fetches model data from OpenRouter API and returns a filtered list of models.

    Args:
        free_only (bool): If True, returns only free models.

    Returns:
        List[Dict]: List of models with name, slug, author, and provider information.
    """
    api_url = "https://openrouter.ai/api/frontend/models"

    try:
        response = requests.get(api_url, verify=False)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json().get("data", [])
        models_list = []

        for model in data:
            # Check if model has required fields
            if all(key in model for key in ["name", "slug", "author"]):
                # Check if we need to filter for free models
                if free_only:
                    # Check for ":free" suffix in the slug
                    if not (
                        isinstance(model["slug"], str) and ":free" in model["slug"]
                    ):
                        continue

                # Extract provider name from endpoint if available
                provider_name = None
                if (
                    "endpoint" in model
                    and model["endpoint"]
                    and "provider_name" in model["endpoint"]
                ):
                    provider_name = model["endpoint"]["provider_name"]
                is_free = isinstance(model["slug"], str) and ":free" in model["slug"]
                # Extract relevant information
                model_info = {
                    "name": model["name"],
                    "model_id": model["slug"],  # Using slug as the model identifier
                    "author": model["author"].upper(),
                    "provider": provider_name,  # Add provider name from endpoint
                    "is_free": is_free,
                }
                models_list.append(model_info)

        return models_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching models: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    all_models = get_openrouter_models()
    print(f"Total models available: {len(all_models)}")

    free_models = get_openrouter_models(free_only=True)
    print(f"Free models available: {len(free_models)}")

    # Print some sample models
    if free_models:
        print("\nSample free models:")
        for model in free_models[:3]:  # Show first 3 free models
            provider_info = f" via {model['provider']}" if model["provider"] else ""
            print(
                f"- {model['name']} by {model['author']}{provider_info} (ID: {model['model_id']})"
            )
