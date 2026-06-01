def save_products(products):
    """
    Save the list of products to the 'products.txt' file.
    Each product is saved as a comma-separated string with the format:
    name, brand, quantity, cost_price, country.
    """
    with open("products.txt", "w", encoding='utf-8') as file:

        # Iterate over the list of products
        for p in products:
            
            # Write each product's data to the file as a formatted string
            file.write(f"{p['name']}, {p['brand']}, {p['quantity']}, {p['cost_price']}, {p['country']}\n")
