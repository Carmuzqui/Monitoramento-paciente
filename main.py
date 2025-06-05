import streamlit as st
from streamlit_option_menu import option_menu
from menu import home, exploracao, alinhamento, previsao    # <--- importa previsao
from utils.helpers import create_qr_code, add_vertical_space

st.set_page_config(page_title="Monitoramento de Sinais Vitais", layout="wide", page_icon="🫁")

# menu_options = ["Início", "Alinhamento", "Exploração", "Previsão"]  # <-- añade Previsão
menu_options = ["Início", "Exploração", "Estimativa da MAP"]
menu_icons = ["house", "bar-chart", "activity"]
MENU_KEY = "menu_selected_option"

# Gerenciar estado inicial
if MENU_KEY not in st.session_state:
    st.session_state[MENU_KEY] = menu_options[0]
active_page_to_render = st.session_state[MENU_KEY]

# Menu lateral
with st.sidebar:
    st.title("🩺 Monitoramento")
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=menu_options.index(active_page_to_render),
        key=MENU_KEY,
        orientation="vertical",
    )
    active_page_to_render = selected

# Renderizar página correspondente
if active_page_to_render == "Início":
    home.render(create_qr_code, add_vertical_space)
elif active_page_to_render == "Exploração":
    exploracao.render()
# elif active_page_to_render == "Alinhamento":
#     alinhamento.render()
elif active_page_to_render == "Estimativa da MAP":
    previsao.render()
else:
    st.error("Página não reconhecida.")
