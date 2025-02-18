import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import carica_menu

# Imposta il layout a "wide" per una visualizzazione migliore
st.set_page_config(page_title="Menù del giorno 🍽️", layout="wide")

# Stile personalizzato per il design
st.markdown("""
    <style>
        .menu-card {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        .menu-title {
            font-size: 24px;  /* Aumentato il font size */
            font-weight: bold;
            color: #2c3e50;
        }
        .ingredienti {
            font-size: 16px;
            color: #7f8c8d;
        }
        .allergen-icons {
            font-size: 14px;
            color: #2980b9;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Titolo principale
st.title("🍽️ Menù del giorno")

# Ottieni il menu dal sito
menu = carica_menu.get_menu()
print(menu)

# Controllo se il menu è stato caricato con successo
if not menu:
    st.error("⚠️ Impossibile caricare il menu. Riprova più tardi.")
else:
    # Data del menu
    st.subheader(f"📅 {menu['data']}")

    # Itera sulle categorie (Primi, Secondi, Contorni...)
    for category, dishes in menu["menu"].items():
        st.markdown(f"### 🍽️ {category.capitalize()}")  # Titolo della categoria

        # Dividi i piatti in colonne
        cols = st.columns(2)

        for index, dish in enumerate(dishes):
            with cols[index % 2]:  # Alterna le colonne
                with st.container():
                    # Costruisci HTML senza tag chiusi male
                    allergen_info = []
                    if dish['gluten_free']:
                        allergen_info.append("🚫🌾 <b>Senza Glutine</b>")
                    if dish['lactose_free']:
                        allergen_info.append("🚫🥛 <b>Senza Lattosio</b>")
                    if dish['frozen']:
                        allergen_info.append("❄️ <b>Surgelato</b>")

                    allergen_html = "<br>".join(allergen_info) if allergen_info else ""

                    # Correggi HTML mal formato
                    st.markdown(f"""
                        <div class="menu-card">
                            <p class="menu-title">{dish['piatto']}</p>
                            <p class="ingredienti">{dish['ingredienti']}</p>
                            <p class="allergen-icons">{allergen_html}</p>
                        </div>
                    """, unsafe_allow_html=True)



