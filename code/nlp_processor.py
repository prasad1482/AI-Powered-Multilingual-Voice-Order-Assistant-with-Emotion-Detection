def process_order(text, language="en"):
    # Convert text to lowercase and split into words
    words = text.lower().split()
    order = {"item": None, "quantity": None, "customization": None}
    
    # Define common keywords
    quantities = {"one": 1, "two": 2, "three": 3, "uno": 1, "dos": 2, "tres": 3}
    items = ["cheeseburgers", "hamburguesas", "fries", "pizza"]
    customizations = ["no", "without", "sin"]
    
    # Extract entities
    for word in words:
        if word in quantities:
            order["quantity"] = quantities[word]
        elif word in items:
            order["item"] = word
        elif word in customizations:
            order["customization"] = words[words.index(word) + 1] if words.index(word) + 1 < len(words) else None
    
    # Generate response
    if order["item"] is None:
        order["item"] = "unknown item"
    if order["quantity"] is None:
        order["quantity"] = 1
    if order["customization"] is None:
        order["customization"] = "no customization"
    
    if language == "es":
        return f"Pedido: {order['quantity']} {order['item']} sin {order['customization']}"
    return f"Order: {order['quantity']} {order['item']}, {order['customization']}"

if __name__ == "__main__":
    english_order = "two cheeseburgers no ketchup"
    spanish_order = "dos hamburguesas sin salsa"
    print(process_order(english_order, "en"))
    print(process_order(spanish_order, "es"))