
def load_products():
    """
    Load product data from 'products.txt'.
    If the file doesn't exist, create it with default products and then load them.
    Returns:
        A list of dictionaries, each representing a product.
    """
    products = []  # List to store loaded product data
    
    try:
        # Try to open and read the file
        with open("products.txt", "r", encoding='utf-8') as file:
            for line in file:

                # Split line into components and remove extra spaces
                parts = [part.strip() for part in line.strip().split(",")]
                
                # Ensure correct number of parts in line
                if len(parts) == 5:

                    # Convert appropriate fields to int/float and store as a dictionary
                    products.append({
                        "name": parts[0],
                        "brand": parts[1],
                        "quantity": int(parts[2]),
                        "cost_price": float(parts[3]),
                        "country": parts[4]
                    })
    except FileNotFoundError:
        
        # If file doesn't exist, create it with some default product entries
        with open("products.txt", "w", encoding='utf-8') as file:
            default_products = [
                "Vitamin C Serum, Garnier, 200, 1000, France",
                "Skin Cleanser, Cetaphil, 100, 280, Switzerland",
                "Sunscreen, Aqualogica, 200, 700, India",
                "Toner, Plum, 60, 500, India",
                "Conditioner, L'Oréal, 110, 400, France",
                "Night Cream, Olay, 70, 1000, USA",
                "Face Serum, Minimalist, 130, 800, India"
            ]
            file.write("\n".join(default_products))  # Write defaults to file
        
        return load_products()  # Recursively load again after creating the file

    return products  # Return loaded product list
