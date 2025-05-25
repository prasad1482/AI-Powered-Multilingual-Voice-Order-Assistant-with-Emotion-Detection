import spacy
from fuzzywuzzy import process
from typing import List, Dict

def process_order(text: str, language: str = "en") -> Dict:
    nlp = spacy.load("en_core_web_sm" if language == "en" else "es_core_news_sm")
    doc = nlp(text.lower())
    
    orders = []
    current_order = {"quantity": 1, "item": None, "customization": None, "intent": "add", "price": 0.0}
    menu_items = {
        "cheeseburgers": 5.99, "hamburgers": 4.99, "hamburguesas": 4.99,
        "fries": 2.99, "pizza": 8.99
    }
    quantities = {"one": 1, "two": 2, "three": 3, "uno": 1, "dos": 2, "tres": 3}
    customizations = ["no", "without", "sin"]
    intents = {
        "add": ["add", "order", "want", "agregar", "pedir"],
        "remove": ["remove", "delete", "no want", "quitar", "eliminar"],
        "confirm": ["confirm", "yes", "correct", "confirmar", "sí", "correcto"]
    }
    conjunctions = ["and", "y"]
    
    # Spelling correction
    tokens = [token.text for token in doc]
    for i, token in enumerate(tokens):
        if token not in quantities and token not in customizations and token not in conjunctions:
            match, score = process.extractOne(token, list(menu_items.keys()) + list(intents.keys()) + list(quantities.keys()))
            if score > 80:  # Threshold for correction
                tokens[i] = match
    corrected_text = " ".join(tokens)
    doc = nlp(corrected_text)
    
    for token in doc:
        for intent, keywords in intents.items():
            if token.text in keywords:
                if current_order["item"]:
                    orders.append(current_order)
                current_order = {"quantity": 1, "item": None, "customization": None, "intent": intent, "price": 0.0}
                break
        if token.text in quantities:
            current_order["quantity"] = quantities[token.text]
        elif token.text in menu_items:
            current_order["item"] = token.text
            current_order["price"] = menu_items[token.text] * current_order["quantity"]
        elif token.text in customizations and token.i + 1 < len(doc):
            current_order["customization"] = doc[token.i + 1].text
        elif token.text in conjunctions and current_order["item"]:
            orders.append(current_order)
            current_order = {"quantity": 1, "item": None, "customization": None, "intent": "add", "price": 0.0}
    
    if current_order["item"] or current_order["intent"] in ["remove", "confirm"]:
        orders.append(current_order)
    
    if not orders:
        orders.append({"quantity": 1, "item": "unknown item", "customization": "no customization", "intent": "add", "price": 0.0})
    
    validated_orders = []
    for order in orders:
        if order["item"] not in menu_items and order["intent"] not in ["remove", "confirm"]:
            order["item"] = "invalid item"
            order["customization"] = "please clarify"
            order["price"] = 0.0
        validated_orders.append(order)
    
    response = []
    for order in validated_orders:
        if language == "es":
            if order["intent"] == "add":
                response.append(f"{order['quantity']} {order['item']} sin {order['customization'] or 'nada'} (${order['price']:.2f})")
            elif order["intent"] == "remove":
                response.append(f"Quitando {order['item'] or 'artículo'}")
            elif order["intent"] == "confirm":
                response.append("Orden confirmada")
        else:
            if order["intent"] == "add":
                response.append(f"{order['quantity']} {order['item']}, {order['customization'] or 'no customization'} (${order['price']:.2f})")
            elif order["intent"] == "remove":
                response.append(f"Removing {order['item'] or 'item'}")
            elif order["intent"] == "confirm":
                response.append("Order confirmed")
    
    return {
        "order_text": " y ".join(response) if language == "es" else " and ".join(response),
        "orders": validated_orders,
        "confirmation_prompt": f"¿Es correcto: {' y '.join(response)}?" if language == "es" else f"Is this correct: {' and '.join(response)}?"
    }

if __name__ == "__main__":
    english_order = "add too chesseburger no ketcup and remove friez"
    spanish_order = "agregar dos hamburguesa sin sals y quitar piza"
    print("English:", process_order(english_order, "en"))
    print("Spanish:", process_order(spanish_order, "es"))