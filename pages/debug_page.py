import streamlit as st
import time
import json
import os


def format_time(timestamp):
    """Timestamp'i okunabilir formata dönüştürür"""
    if not timestamp:
        return "Hiç güncellenmemiş"
    return time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(timestamp))


def format_cache_age(timestamp):
    """Önbellek yaşını dakika ve saat olarak gösterir"""
    if not timestamp:
        return "Hiç güncellenmemiş"

    age_seconds = time.time() - timestamp
    if age_seconds < 60:
        return f"{age_seconds:.0f} saniye önce"
    elif age_seconds < 3600:
        return f"{age_seconds/60:.1f} dakika önce"
    else:
        return f"{age_seconds/3600:.1f} saat önce"


def debug_view():
    st.set_page_config(page_title="Debug View", page_icon="🐞")

    st.title("🐞 Debug Görünümü")
    st.write(
        "Bu sayfa, uygulama durumu ve önbellek bilgilerini görüntülemek için kullanılır."
    )

    tabs = st.tabs(["🔄 Session State", "💾 Model Cache", "🛠️ Sistem Bilgisi"])

    with tabs[0]:
        st.subheader("Session State İçeriği")

        # Session state anahtarlarını kategorize et
        config_keys = [k for k in st.session_state.keys() if k == "config"]
        model_keys = [k for k in st.session_state.keys() if "model" in k]
        nav_keys = [k for k in st.session_state.keys() if "navigation" in k]
        other_keys = [
            k
            for k in st.session_state.keys()
            if k not in config_keys + model_keys + nav_keys and k != "model_cache"
        ]

        # Yapılandırma bilgisi
        if config_keys:
            st.write("### Yapılandırma")
            config = st.session_state.get("config", {})

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ajan Sayısı", len(config.get("agents", [])))
            with col2:
                st.metric("Görev Sayısı", len(config.get("tasks", [])))

            if st.checkbox("Yapılandırma Detayları", value=False):
                st.json(config)

        # Model ve provider bilgisi
        if model_keys:
            st.write("### Model Bilgisi")
            for key in model_keys:
                st.write(f"**{key}:** {st.session_state[key]}")

        # Navigasyon bilgisi
        if nav_keys:
            st.write("### Navigasyon Bilgisi")
            for key in nav_keys:
                st.write(f"**{key}:** {st.session_state[key]}")

        # Diğer session state verileri
        if other_keys:
            st.write("### Diğer Session State Verileri")
            for key in other_keys:
                st.write(f"**{key}:**")
                st.write(st.session_state[key])

        # Session state temizleme işlemleri
        st.write("---")
        st.subheader("Session State İşlemleri")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Tüm Session State'i Temizle", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Tüm session state temizlendi!")
                st.rerun()

        with col2:
            if st.button("🧹 Sadece Yapılandırmayı Temizle"):
                if "config" in st.session_state:
                    del st.session_state["config"]
                    st.success("Yapılandırma temizlendi!")
                    st.rerun()

    with tabs[1]:
        st.subheader("Model Cache Bilgisi")

        if "model_cache" in st.session_state:
            cache = st.session_state.model_cache
            timestamp = cache.get("timestamp", 0)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Cache Oluşturulma", format_time(timestamp))
            with col2:
                st.metric("Cache Yaşı", format_cache_age(timestamp))
            with col3:
                if "openrouter" in cache:
                    st.metric("OpenRouter Model Sayısı", len(cache["openrouter"]))

            # OpenRouter modelleri
            if "openrouter" in cache and cache["openrouter"]:
                st.write("### OpenRouter Modelleri")

                # Filtreleme alanı
                filter_text = st.text_input("Model Ara:", "")

                # Modelleri filtrele ve göster
                models = cache["openrouter"]
                if filter_text:
                    models = [m for m in models if filter_text.lower() in m.lower()]

                if models:
                    st.write(f"{len(models)} model bulundu")
                    for i, model in enumerate(models):
                        st.code(model)
                else:
                    st.info("Filtreye uygun model bulunamadı")

            # Cache temizleme
            if st.button("🧹 Model Cache'i Temizle"):
                if "model_cache" in st.session_state:
                    del st.session_state["model_cache"]
                    st.success("Model cache temizlendi!")
                    st.rerun()
        else:
            st.info("Henüz model cache oluşturulmamış.")

            # Proaktif önbellek oluşturma
            if st.button("OpenRouter Modellerini Önbelleğe Al"):
                from utils.openrouter import get_openrouter_models

                with st.spinner("OpenRouter modelleri alınıyor..."):
                    try:
                        st.session_state.model_cache = {}
                        models = get_openrouter_models()
                        model_options = [model["model_id"] for model in models]
                        st.session_state.model_cache["openrouter"] = model_options
                        st.session_state.model_cache["timestamp"] = time.time()
                        st.success(
                            f"{len(model_options)} model başarıyla önbelleğe alındı!"
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Model listesi alınamadı: {str(e)}")

    with tabs[2]:
        st.subheader("Sistem Bilgisi")

        # Çevresel değişkenler (hassas bilgileri maskeleyerek)
        st.write("### Çevresel Değişkenler")
        env_vars = {
            "OPENAI_API_KEY": (
                "***" if os.environ.get("OPENAI_API_KEY") else "Tanımlanmamış"
            ),
            "OPENROUTER_API_KEY": (
                "***" if os.environ.get("OPENROUTER_API_KEY") else "Tanımlanmamış"
            ),
            "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "Tanımlanmamış"),
            "OPENROUTER_MODEL": os.environ.get("OPENROUTER_MODEL", "Tanımlanmamış"),
        }

        st.json(env_vars)

        # Streamlit Bilgileri
        st.write("### Streamlit Bilgileri")
        is_sidebar = st.sidebar.checkbox("Bu kutucuk görünürse sidebar aktif demektir")
        st.write(f"Streamlit Sidebar Aktif: {is_sidebar}")


if __name__ == "__main__":
    debug_view()
