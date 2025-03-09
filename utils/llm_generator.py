import os
import json
import requests
import urllib3
from typing import Dict, Any, Tuple, List, Optional
import streamlit as st
from framework.tool_utils import get_available_tools

# LLM Servis sağlayıcıları
LLM_PROVIDERS = {
    "openai": "OpenAI API",
    "openrouter": "OpenRouter API",
}


def get_available_llm_providers():
    """Mevcut LLM sağlayıcılarını döndürür"""
    return LLM_PROVIDERS


def generate_crew_with_llm(
    user_prompt: str,
    provider: str,
    model: Optional[str] = None,
    existing_config: Optional[Dict[str, Any]] = None,
    update_scope: str = "all",
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Kullanıcı isteği doğrultusunda LLM kullanarak bir CrewAI yapılandırması oluşturur

    Args:
        user_prompt: Kullanıcının doğal dil istekleri
        provider: Kullanılacak LLM sağlayıcısı
        model: Kullanılacak model adı (opsiyonel)
        existing_config: Mevcut yapılandırma (opsiyonel)
        update_scope: Güncelleme kapsamı - "all", "agents", "tasks"

    Returns:
        Oluşturulan config ve uyarılar
    """
    warnings = []

    # Kullanılabilir araçlar hakkında bilgi al
    available_tools = get_available_tools()
    tool_descriptions = "\n".join(
        [f"- {name}: {info['description']}" for name, info in available_tools.items()]
    )

    # Sistem mesajı
    system_msg = (
        """Sen bir ekip ve görev tasarım uzmanısın. Kullanıcının belirttiği senaryoya uygun bir CrewAI yapılandırması oluşturacaksın.
    
    # ... mevcut sistem mesajı ...
    """
        + tool_descriptions
    )

    # Mevcut yapılandırma ve güncelleme kapsamı bilgilerini ekle
    if existing_config:
        system_msg += "\n\nMevcut yapılandırma:\n"
        if existing_config.get("agents"):
            system_msg += "Agents:\n"
            for agent in existing_config["agents"]:
                system_msg += f"- {agent['role']}: {agent['goal']}\n"

        if existing_config.get("tasks"):
            system_msg += "\nTasks:\n"
            for task in existing_config["tasks"]:
                system_msg += f"- {task['name']}: {task['description']}\n"

        if update_scope == "agents":
            system_msg += "\nSadece ajanları güncelle, görevlere dokunma."
        elif update_scope == "tasks":
            system_msg += "\nSadece görevleri güncelle, ajanlara dokunma."
        else:
            system_msg += "\nHem ajanları hem de görevleri güncelle."

    try:
        # Sağlayıcıya göre API çağrısı yap
        if provider == "openai":
            config, api_warnings = call_openai_api(system_msg, user_prompt, model)
            warnings.extend(api_warnings)
        elif provider == "openrouter":
            try:
                config, api_warnings = call_openrouter_api(
                    system_msg, user_prompt, model
                )
                warnings.extend(api_warnings)
            except Exception as openrouter_error:
                warnings.append(
                    f"OpenRouter API hatası: {str(openrouter_error)}. OpenAI API'ye geçiliyor."
                )
                # OpenRouter başarısız olursa OpenAI'ya geri dön
                if os.environ.get("OPENAI_API_KEY"):
                    fallback_model = "gpt-3.5-turbo"  # Fallback model
                    config, api_warnings = call_openai_api(
                        system_msg, user_prompt, fallback_model
                    )
                    warnings.extend(api_warnings)
                    warnings.append(
                        f"OpenAI API ({fallback_model}) ile yedek çözüm kullanıldı."
                    )
                else:
                    return {"agents": [], "tasks": []}, [
                        "OpenRouter API başarısız ve OPENAI_API_KEY bulunamadı."
                    ]
        else:
            return {"agents": [], "tasks": []}, [
                f"Desteklenmeyen LLM sağlayıcısı: {provider}"
            ]

        # Mevcut yapılandırmayla birleştir veya güncelle
        if existing_config and update_scope != "all":
            if update_scope == "agents":
                # Sadece ajanları güncelle
                config["tasks"] = existing_config.get("tasks", [])
            elif update_scope == "tasks":
                # Sadece görevleri güncelle
                config["agents"] = existing_config.get("agents", [])

        return config, warnings

    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        st.error(f"LLM çağrısı sırasında hata: {str(e)}")
        print(error_details)
        return {"agents": [], "tasks": []}, [f"LLM çağrısı sırasında hata: {str(e)}"]


def call_openai_api(
    system_msg: str, user_prompt: str, model: Optional[str] = None
) -> Tuple[Dict[str, Any], List[str]]:
    """OpenAI API'yi çağırır"""
    import openai

    warnings = []

    # API anahtarını kontrol et
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"agents": [], "tasks": []}, [
            "OpenAI API anahtarı bulunamadı. Lütfen .env dosyasına OPENAI_API_KEY ekleyin."
        ]

    # Varsayılan model
    if not model:
        model = "gpt-4"

    try:
        # API çağrısı
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )

        # Yanıtı JSON'a dönüştür
        result_text = response.choices[0].message.content
        config = json.loads(result_text)

        return validate_crew_config(config)

    except json.JSONDecodeError:
        return {"agents": [], "tasks": []}, [
            "LLM yanıtı geçerli bir JSON formatında değil."
        ]
    except Exception as e:
        return {"agents": [], "tasks": []}, [f"OpenAI API hatası: {str(e)}"]


def call_openrouter_api(
    system_msg: str, user_prompt: str, model: Optional[str] = None
) -> Tuple[Dict[str, Any], List[str]]:
    """OpenRouter API'yi çağırır"""
    warnings = []

    # API anahtarını kontrol et
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return {"agents": [], "tasks": []}, [
            "OpenRouter API anahtarı bulunamadı. Lütfen .env dosyasına OPENROUTER_API_KEY ekleyin."
        ]

    # Varsayılan model
    if not model:
        model = "openai/gpt-4-turbo"

    try:
        # Session oluştur ve yeniden kullanılabilir hale getir
        session = requests.Session()

        # API çağrısı
        response = session.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            verify=False,  # SSL doğrulamasını devre dışı bırak
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/yourusername/crew-agent-generator",  # OpenRouter API politikası gereği
                "X-Title": "Crew-Agent-Generator",  # OpenRouter API politikası gereği
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 4000,
            },
            timeout=60,  # Timeout değerini artır
        )

        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                if "error" in error_json:
                    error_detail = error_json.get("error", {}).get(
                        "message", error_detail
                    )
            except:
                pass

            return {"agents": [], "tasks": []}, [
                f"OpenRouter API hatası: {response.status_code} - {error_detail}"
            ]

        # Yanıtı JSON'a dönüştür
        result = response.json()
        result_text = result["choices"][0]["message"]["content"]

        # JSON içeriğini temizle - bazen model fazladan karakterler ekleyebilir
        result_text = result_text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        config = json.loads(result_text)
        return validate_crew_config(config)

    except json.JSONDecodeError as e:
        return {"agents": [], "tasks": []}, [
            f"LLM yanıtı geçerli bir JSON formatında değil: {str(e)}"
        ]
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        return {"agents": [], "tasks": []}, [
            f"OpenRouter API hatası: {str(e)}\n{error_details}"
        ]


def validate_crew_config(config: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """CrewAI yapılandırmasını doğrular ve uyarıları döndürür"""
    warnings = []

    # Kullanılabilir araçları al
    available_tools = get_available_tools()

    # Minimum gereksinimleri kontrol et
    if "agents" not in config or len(config["agents"]) == 0:
        warnings.append("Yapılandırmada agent bulunamadı.")
        config["agents"] = []

    if "tasks" not in config or len(config["tasks"]) == 0:
        warnings.append("Yapılandırmada task bulunamadı.")
        config["tasks"] = []

    # Her agent için kontroller
    for agent in config.get("agents", []):
        # Gerekli alanları kontrol et
        if "name" not in agent:
            agent["name"] = "unnamed_agent"
            warnings.append(
                f"İsimsiz agent tespit edildi. Otomatik olarak '{agent['name']}' olarak isimlendirildi."
            )

        # Boşlukları alt çizgi ile değiştir
        if " " in agent["name"]:
            old_name = agent["name"]
            agent["name"] = agent["name"].replace(" ", "_")
            warnings.append(
                f"Agent ismi '{old_name}' boşluk içeriyor. '{agent['name']}' olarak düzeltildi."
            )

        # Araçları doğrula
        if "tools" not in agent or not agent["tools"]:
            agent["tools"] = []
            warnings.append(f"Agent '{agent['name']}' için araç tanımlanmamış.")
        else:
            valid_tools = []
            for tool in agent["tools"]:
                if tool in available_tools:
                    valid_tools.append(tool)
                else:
                    warnings.append(
                        f"Bilinmeyen araç '{tool}' agent '{agent['name']}' için tanımlanmış. Bu araç atlanacak."
                    )
            agent["tools"] = valid_tools

    # Her task için kontroller
    for task in config.get("tasks", []):
        # Gerekli alanları kontrol et
        if "name" not in task:
            task["name"] = "unnamed_task"
            warnings.append(
                f"İsimsiz task tespit edildi. Otomatik olarak '{task['name']}' olarak isimlendirildi."
            )

        # Boşlukları alt çizgi ile değiştir
        if " " in task["name"]:
            old_name = task["name"]
            task["name"] = task["name"].replace(" ", "_")
            warnings.append(
                f"Task ismi '{old_name}' boşluk içeriyor. '{task['name']}' olarak düzeltildi."
            )

        # Agent'ı doğrula
        if "agent" not in task:
            if config.get("agents"):
                task["agent"] = config["agents"][0]["name"]
                warnings.append(
                    f"Task '{task['name']}' için agent belirtilmemiş. İlk agent '{task['agent']}' atandı."
                )
            else:
                warnings.append(
                    f"Task '{task['name']}' için agent belirtilmemiş ve yapılandırmada hiç agent yok."
                )
        else:
            # Agent'ın varlığını kontrol et
            agent_names = [a["name"] for a in config.get("agents", [])]
            if task["agent"] not in agent_names:
                if agent_names:
                    task["agent"] = agent_names[0]
                    warnings.append(
                        f"Task '{task['name']}' için tanımlanan agent bulunamadı. '{task['agent']}' olarak değiştirildi."
                    )
                else:
                    warnings.append(
                        f"Task '{task['name']}' için tanımlanan agent bulunamadı ve yapılandırmada hiç agent yok."
                    )

    return config, warnings


def get_example_scenario_prompts() -> List[str]:
    """Örnek senaryo promptlarını döndürür"""
    return [
        "Bir incident analiz sistemi oluşturmak istiyorum. Bu sistem, güvenlik olaylarını analiz edip raporlayabilmeli.",
        "Bir içerik pazarlama ekibi için bir CrewAI sistemi oluşturmak istiyorum. Blog yazıları için araştırma yapıp yazabilmeli.",
        "Müşteri geri bildirimlerini analiz eden ve ürün geliştirme önerileri sunan bir sistem istiyorum.",
        "Rakip analizi yapan ve pazar fırsatlarını belirleyen bir sistem oluşturmak istiyorum.",
        "Web sitemi SEO açısından analiz edip iyileştirmeler öneren bir sistem istiyorum.",
    ]
