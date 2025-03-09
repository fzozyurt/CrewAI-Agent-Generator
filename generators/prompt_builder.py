import streamlit as st
import os
from utils.openrouter import get_openrouter_models
from utils.llm_generator import (
    generate_crew_with_llm,
    get_available_llm_providers,
    get_example_scenario_prompts,
)


def prompt_builder():
    """Prompt tabanlı ekip oluşturucu UI"""

    st.header("🔮 Prompt Tabanlı Ekip Oluşturucu")

    # Sekmeler oluştur: Yapılandırma modu ve LLM modu
    tab1, tab2 = st.tabs(["🤖 LLM ile Oluştur", "✍️ Manuel Giriş"])

    with tab1:
        # LLM ile ekip oluşturma
        llm_based_crew_builder()


def update_configuration(new_config):
    """Mevcut yapılandırmayı günceller veya birleştirir"""

    # Session state'te yapılandırma yoksa oluştur
    if "config" not in st.session_state:
        st.session_state.config = {"agents": [], "tasks": []}

    # Mevcut yapılandırma varsa, güncelleme seçenekleri göster
    if st.session_state.config["agents"] or st.session_state.config["tasks"]:
        st.subheader("Yapılandırmayı Güncelle")
        option = st.radio(
            "Mevcut yapılandırma ile ne yapmak istersiniz?",
            ["Mevcut yapılandırmayı değiştir", "Mevcut yapılandırma ile birleştir"],
        )

        if option == "Mevcut yapılandırmayı değiştir":
            st.session_state.config = new_config
            st.success("Yapılandırma başarıyla güncellendi!")
        else:
            # Yapılandırmaları birleştir
            merge_configurations(st.session_state.config, new_config)
            st.success("Yapılandırmalar başarıyla birleştirildi!")
    else:
        # Mevcut yapılandırma yoksa, direkt kaydet
        st.session_state.config = new_config
        st.success("Yapılandırma başarıyla oluşturuldu!")

    # Yapılandırma önizlemesi
    preview_config(new_config)


def merge_configurations(target_config, source_config):
    """İki yapılandırmayı birleştirir"""

    # Ajanları birleştir
    for agent in source_config["agents"]:
        existing_names = [a["name"] for a in target_config["agents"]]
        if agent["name"] in existing_names:
            idx = existing_names.index(agent["name"])
            target_config["agents"][idx] = agent
        else:
            target_config["agents"].append(agent)

    # Görevleri birleştir
    for task in source_config["tasks"]:
        existing_names = [t["name"] for t in target_config["tasks"]]
        if task["name"] in existing_names:
            idx = existing_names.index(task["name"])
            target_config["tasks"][idx] = task
        else:
            target_config["tasks"].append(task)


def preview_config(config):
    """Yapılandırma önizlemesi görüntüler"""

    st.subheader("Oluşturulan Yapılandırma")

    agent_tab, task_tab = st.tabs(["Agents", "Tasks"])

    with agent_tab:
        for agent in config["agents"]:
            with st.expander(f"🤖 {agent['role']}", expanded=True):
                st.write(f"**Name:** {agent['name']}")
                st.write(f"**Goal:** {agent['goal']}")
                st.write(f"**Backstory:** {agent['backstory']}")
                if agent["tools"]:
                    st.write(f"**Tools:** {', '.join(agent['tools'])}")
                else:
                    st.write("**Tools:** None")

    with task_tab:
        for task in config["tasks"]:
            with st.expander(f"📋 {task['name']}", expanded=True):
                st.write(f"**Description:** {task['description']}")
                st.write(f"**Expected Output:** {task['expected_output']}")
                st.write(f"**Assigned to:** {task['agent']}")

    # Önizleme sayfasına geçiş butonu
    if st.button("Önizleme ve Kod Sayfasına Git"):
        st.session_state.navigation = "Preview & Code"
        st.rerun()


def llm_based_crew_builder():
    """LLM tabanlı ekip oluşturucu"""

    st.subheader("LLM ile Ekip Oluştur")
    st.write(
        "Ne tür bir ekibe ihtiyacınız olduğunu doğal dilde anlatın, yapay zeka uygun bir yapılandırma oluştursun."
    )

    # LLM ayarları
    with st.expander("LLM Ayarları", expanded=False):
        # ENV'den API key kontrolleri ve varsayılan sağlayıcı belirleme
        openai_key = os.environ.get("OPENAI_API_KEY")
        openrouter_key = os.environ.get("OPENROUTER_API_KEY")

        # Öncelik sırası: 1) OpenRouter (eğer API key varsa), 2) OpenAI (eğer API key varsa), 3) Varsayılan "openai"
        default_provider = "openrouter"  # Varsayılan değer

        if openrouter_key:
            default_provider = "openrouter"
        elif openai_key:
            default_provider = "openai"

        providers = get_available_llm_providers()
        provider_options = list(providers.keys())

        col1, col2 = st.columns(2)

        with col1:
            if "selected_provider" not in st.session_state:
                st.session_state.selected_provider = default_provider

            provider = st.selectbox(
                "LLM Sağlayıcısı",
                options=provider_options,
                format_func=lambda x: providers[x],
                index=provider_options.index(st.session_state.selected_provider),
                key="provider_selectbox",
            )
            st.session_state.selected_provider = provider

        with col2:
            # Model seçimi için önbellek kullanımı
            if "model_cache" not in st.session_state:
                st.session_state.model_cache = {}

            if "selected_model" not in st.session_state:
                st.session_state.selected_model = {}

            if provider == "openai":
                model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

                # ENV'de belirtilen model var mı kontrol et
                env_model = os.environ.get("OPENAI_MODEL")
                default_model_idx = 0

                if env_model and env_model in model_options:
                    default_model_idx = model_options.index(env_model)
                elif provider in st.session_state.selected_model:
                    # Daha önce seçilmiş model varsa onu kullan
                    if st.session_state.selected_model[provider] in model_options:
                        default_model_idx = model_options.index(
                            st.session_state.selected_model[provider]
                        )

                model = st.selectbox(
                    "Model", options=model_options, index=default_model_idx
                )
                st.session_state.selected_model[provider] = model

            elif provider == "openrouter":
                # OpenRouter modellerini direkt cache fonksiyonundan al
                with st.spinner("Model listesi alınıyor..."):
                    models = get_openrouter_models()
                    model_options = [model["model_id"] for model in models]

                # ENV'de belirtilen model var mı kontrol et
                env_model = os.environ.get("OPENROUTER_MODEL")
                default_model_idx = 0

                if env_model and env_model in model_options:
                    default_model_idx = model_options.index(env_model)
                elif provider in st.session_state.selected_model:
                    # Daha önce seçilmiş model varsa onu kullan
                    if st.session_state.selected_model[provider] in model_options:
                        default_model_idx = model_options.index(
                            st.session_state.selected_model[provider]
                        )

                model = st.selectbox(
                    "Model", options=model_options, index=default_model_idx
                )
                st.session_state.selected_model[provider] = model

            else:
                # Diğer sağlayıcılar için önceki seçimi hatırla
                default_model = ""
                if provider in st.session_state.selected_model:
                    default_model = st.session_state.selected_model[provider]

                model = st.text_input("Model İsmi", value=default_model)
                st.session_state.selected_model[provider] = model

        # API key durumunu kontrol et
        if provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                st.warning("⚠️ OPENAI_API_KEY bulunamadı. .env dosyasına eklemelisiniz.")
        elif provider == "openrouter":
            api_key = os.environ.get("OPENROUTER_API_KEY")
            if not api_key:
                st.warning(
                    "⚠️ OPENROUTER_API_KEY bulunamadı. .env dosyasına eklemelisiniz."
                )

    # İstek promptu için metin alanı
    if "scenario_prompt" not in st.session_state:
        st.session_state.scenario_prompt = ""

    # Örnek senaryolar
    examples = get_example_scenario_prompts()
    with st.expander("Örnek Senaryolar", expanded=False):
        for i, example in enumerate(examples):
            if st.button(f"Örnek {i+1}", key=f"scenario_{i}"):
                st.session_state.scenario_prompt = example
                st.rerun()

    # Kullanıcı prompt girişi
    scenario_prompt = st.text_area(
        "İhtiyacınızı açıklayın:",
        value=st.session_state.scenario_prompt,
        height=150,
        placeholder="Örneğin: Bir incident analiz sistemi oluşturmak istiyorum. Bu sistem güvenlik olaylarını inceleyip raporlayabilmeli.",
    )

    # Yapılandırma oluştur butonu
    if st.button("🔮 Ekip Oluştur", type="primary", disabled=not scenario_prompt):
        st.session_state.scenario_prompt = scenario_prompt

        # Yapay zeka ile yapılandırma oluştur
        with st.spinner("Yapay zeka ekip yapılandırması oluşturuyor..."):
            config, warnings = generate_crew_with_llm(
                user_prompt=scenario_prompt, provider=provider, model=model
            )

        # Uyarıları göster
        if warnings:
            with st.expander("⚠️ Uyarılar", expanded=True):
                for warning in warnings:
                    st.warning(warning)

        # Yapılandırmayı göster ve session state'e kaydet
        if config["agents"] or config["tasks"]:
            update_configuration(config)
        else:
            st.error(
                "Yapılandırma oluşturulamadı. Lütfen isteğinizi daha açık bir şekilde ifade edin."
            )
