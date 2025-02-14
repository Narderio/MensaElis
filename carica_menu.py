import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Funzione per ottenere il menu dal sito web
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

# Esegui la funzione e mostra il risultato
menu_of_the_day = get_menu()

if menu_of_the_day:
    print(f"Menu del giorno ({menu_of_the_day['data']}):")
    for category, dishes in menu_of_the_day["menu"].items():
        print(f"\n{category.capitalize()}:")
        for dish in dishes:
            print(f"{dish['piatto']} - {dish['ingredienti']}")
            if dish['gluten_free']:
                print("  Gluten Free")
            if dish['lactose_free']:
                print("  Lactose Free")
            if dish['frozen']:
                print("  Frozen")
