import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_menu():
    url = "https://aiuto.elis.org/menu/"
    response = requests.get(url)
    
    # Controlla che la richiesta abbia avuto successo
    if response.status_code != 200:
        print("Errore nel caricamento della pagina")
        return None
    
    # Analizza la pagina con BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Trova la sezione con il menu (basata sul titolo, classe o altro)
    menu_title = soup.find("h1", {"id": "TitleMenu"})
    if not menu_title:
        print("Menu non trovato nella pagina.")
        return None

    # Inizializza il dizionario per il menu
    menu = {
        "primo": [],
        "secondo": [],
        "contorno": []
    }

    # Estrai le pietanze e aggiungile nelle rispettive categorie
    dishes = soup.find_all("h5", class_="descrizionePietanza")

    for dish in dishes:
        name = dish.get_text(strip=True)
        ingredients = dish.find_next("span", class_="ingredienti")
        ingredients_text = ingredients.get_text(strip=True) if ingredients else "Ingredienti non disponibili"
        
        # Controlla se la pietanza è gluten free, senza lattosio o surgelata
        gluten_free = bool(dish.find("img", {"src": "/Menu/img/gluten.png"}))
        lactose_free = bool(dish.find("img", {"src": "/Menu/img/lactose.png"}))
        frozen = bool(dish.find("span", style="color:aqua;font-weight:bolder;font-size:large;"))

        # Assegna la pietanza alla giusta categoria (primo, secondo, contorno)
        if "Primi" in dish.find_previous("h3").get_text():
            menu["primo"].append({
                "piatto": name,
                "ingredienti": ingredients_text,
                "gluten_free": gluten_free,
                "lactose_free": lactose_free,
                "frozen": frozen
            })
        elif "Secondi" in dish.find_previous("h3").get_text():
            menu["secondo"].append({
                "piatto": name,
                "ingredienti": ingredients_text,
                "gluten_free": gluten_free,
                "lactose_free": lactose_free,
                "frozen": frozen
            })
        elif "Contorni" in dish.find_previous("h3").get_text():
            menu["contorno"].append({
                "piatto": name,
                "ingredienti": ingredients_text,
                "gluten_free": gluten_free,
                "lactose_free": lactose_free,
                "frozen": frozen
            })

    # Ottieni la data corrente e formattala
    today = datetime.today().strftime("%A, %d %B %Y")

    return {
        "data": today,
        "menu": menu
    }

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
            font-size: 20px;
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
menu = get_menu()

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

                    allergen_html = "<br>".join(allergen_info) if allergen_info else "✅ <i>Nessun allergene segnalato</i>"

                    # Correggi HTML mal formato
                    st.markdown(f"""
                        <div class="menu-card">
                            <p class="menu-title">{dish['piatto']}</p>
                            <p class="ingredienti">({dish['ingredienti']})</p>
                            <p class="allergen-icons">{allergen_html}</p>
                        </div>
                    """, unsafe_allow_html=True)



