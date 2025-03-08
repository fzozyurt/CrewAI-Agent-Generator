import os
import json
import traceback
import httpx
from typing import Dict, Any
import streamlit as st
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler
from utils.prompts import get_system_prompt_for_framework, get_default_config
from dotenv import load_dotenv

load_dotenv()

# Initialize Langfuse handler with credentials from environment variables
langfuse_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    httpx_client=httpx.Client(verify=False, timeout=60.0),
)


class AgentGenerator:
    def __init__(self):
        # Initialize with default model
        self.model_id = "deepseek/deepseek-r1:free"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.available_models = []

        # Initialize model on first use instead of constructor
        self.llm = None

    def _initialize_model(self, model_id=None):
        if model_id:
            self.model_id = model_id

        try:
            if not self.api_key:
                if "OPENROUTER_API_KEY" in os.environ:
                    self.api_key = os.environ["OPENROUTER_API_KEY"]

                if not self.api_key:
                    raise ValueError("OpenRouter API Key not found")

            # Configure LangChain ChatOpenAI with OpenRouter
            self.llm = ChatOpenAI(
                model=self.model_id,
                openai_api_key=self.api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                max_tokens=4000,
                temperature=0.1,
                http_client=httpx.Client(verify=False, timeout=240.0),
                callbacks=[langfuse_handler],
            )
        except Exception as e:
            raise Exception(f"Failed to initialize model: {e}")

    def analyze_prompt(
        self, user_prompt: str, framework: str, model_id: str = None
    ) -> Dict[str, Any]:
        self._initialize_model(model_id)

        system_prompt = get_system_prompt_for_framework(framework)

        try:
            # Format messages for LangChain
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # Generate response using OpenRouter via LangChain
            response = self.llm.invoke(
                messages, config={"callbacks": [langfuse_handler]}
            )

            # Extract content from the response
            response_text = response.content

            # Extract JSON from response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                st.warning(
                    "Could not extract valid JSON from model response. Using default configuration."
                )
                return get_default_config(framework)

        except Exception as e:
            st.error(f"Error in analyzing prompt: {e}")
            return get_default_config(framework)


# Örnek kullanım
def generate_agents(prompt, framework, model_id):
    try:
        # AgentGenerator sınıfını başlat
        generator = AgentGenerator()

        # Prompt'u analiz et ve sonucu al
        result = generator.analyze_prompt(
            user_prompt=prompt, framework=framework, model_id=model_id
        )

        return result
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
        st.session_state.error_logs.append(traceback.format_exc())
        return None
