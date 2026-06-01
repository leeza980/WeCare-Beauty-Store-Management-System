from display import display_products, generate_sale_invoice, generate_restock_invoice
from write import save_products

def get_valid_input(prompt, type_, min_=None, max_=None):
    """
    Prompt the user for input and ensure it is of the correct type.
    Optionally validate against min and max bounds.
    """
    while True:
        try:
            value = type_(input(prompt))  # Convert input to specified type
            if (min_ is not None and value < min_) or (max_ is not None and value > max_):
                raise ValueError
            return value
        except ValueError:
            print(f"Invalid input. Please enter a {type_._name_}", end="")
            if min_ is not None and max_ is not None:
                print(f" between {min_} and {max_}.")
            else:
                print(".")

def get_yes_no(prompt):
    """
    Prompt the user for a yes/no answer and return True (yes) or False (no).
    Accepts variations like y, yes, n, no.
    """
    while True:
        response = input(prompt).strip().lower()
        if response.startswith('y'):
            return True
        elif response.startswith('n'):
            return False
        print("Error: Please enter 'y' or 'n'.")

def is_valid_name(name):
    """
    Check that the input name contains only alphabets and spaces.
    Returns True if valid, False otherwise.
    """
    return name.replace(" ", "").isalpha()

def add_new_product(products, restock_items):
    """
    Add a new product to the inventory during restocking.
    Prompts for name, brand (origin), quantity, cost price, and country.
    Adds the new product to restock_items for invoice generation.
    """
    print("\nAdding a new product:")
    
    # Get and validate product name
    while True:
        name = input("Product name: ").strip()
        if not name:
            print("Product name cannot be empty!")
        elif not is_valid_name(name):
            print("Invalid name! Please enter a valid name (alphabets and spaces only).")
        else:
            break

    # Get and validate brand (origin)
    while True:
        brand = input("Brand (origin): ").strip()
        if not brand:
            print("Brand cannot be empty!")
        elif not is_valid_name(brand):
            print("Invalid brand! Please enter a valid brand (alphabets and spaces only).")
        else:
            break

    # Get quantity
    quantity = get_valid_input("Initial quantity: ", int, 1)

    # Get cost price
    cost_price = get_valid_input("Cost price (₹): ", float, 0)

    # Get and validate country
    while True:
        country = input("Country: ").strip()
        if not country:
            print("Country cannot be empty!")
        elif not is_valid_name(country):
            print("Invalid country! Please enter a valid country (alphabets and spaces only).")
        else:
            break

    # Create new product
    new_product = {
        "name": name,
        "brand": brand,
        "quantity": quantity,
        "cost_price": cost_price,
        "country": country
    }
    products.append(new_product)
    
    # Add to restock_items for invoice
    restock_items.append({
        "product": new_product,
        "quantity": quantity,
        "cost": cost_price
    })
    
    save_products(products)  # Save updated product list to file
    print(f"Product '{name}' added successfully!")

def process_sale(products):
    """
    Handle the sale process for customers.
    Includes product selection, quantity input, and 'Buy 3 Get 1 Free' logic.
    """
    display_products(products)  # Show all products to user

    # Get and validate customer name
    while True:
        customer = input("\nCustomer name: ").strip()
        if not customer:
            print("Customer name cannot be empty!")
        elif not is_valid_name(customer):
            print("Invalid name! Please enter a valid name.")
        else:
            break

    cart = []  # List to hold selected sale items
    while True:
        # Display numbered product list
        print("\nAvailable Products:")
        i = 1
        for p in products:
            print(f"{i}. {p['name']} ({p['brand']}) - Stock: {p['quantity']}")
            i += 1
        print("0. Finish")

        # Product selection input
        choice = get_valid_input(f"Select a product (0-{len(products)}): ", int, 0, len(products))
        if choice == 0:
            break  # Exit selection

        product = products[choice - 1]

        # Check stock availability
        if product["quantity"] == 0:
            print(f"The product '{product['name']}' is out of stock.")
            continue

        # Get desired quantity
        qty = get_valid_input(f"Quantity (max {product['quantity']}): ", int, 1, product['quantity'])

        # Calculate free item count (Buy 3 Get 1 Free)
        free_items = qty // 3
        cart.append({
            "product": product,
            "quantity": qty,
            "free": free_items
        })

        # Ask user if they want to add more items
        if not get_yes_no("Add more items? (y/n): "):
            break

    # Generate invoice and update inventory if items were selected
    if cart:
        generate_sale_invoice(customer, cart)
        update_inventory(products, cart, "sale")

def process_restock(products):
    """
    Handle the restocking of products from a supplier.
    Allows changing cost price, quantity update, and adding new products.
    """
    display_products(products)  # Show all current products

    # Get and validate supplier name
    while True:
        supplier = input("\nSupplier name: ").strip()
        if not supplier:
            print("Supplier name cannot be empty!")
        elif not is_valid_name(supplier):
            print("Invalid name! Please enter a valid name.")
        else:
            break

    restock_items = []  # List to hold restock items
    while True:
        # Display numbered product list
        print("\nCurrent Products:")
        i = 1
        while i <= len(products):
            product = products[i-1]
            print(str(i) + ". " + product["name"] + " (" + product["brand"] + ")")
            i = i + 1
        
        # Set option numbers
        add_new_option = len(products) + 1
        finish_option = len(products) + 2
        
        print(str(add_new_option) + ". Add a new product")    
        print(str(finish_option) + ". Finish")

        # Product selection input
        try:
            choice = int(input("Select an option (1-" + str(len(products)) + ", " + 
                             str(add_new_option) + " to add new, " + 
                             str(finish_option) + " to finish): "))
            
            if choice == finish_option:
                break
            elif choice == add_new_option:
                add_new_product(products, restock_items)
                continue
            elif choice >= 1 and choice <= len(products):
                product = products[choice - 1]

                # Get restock quantity
                while True:
                    try:
                        qty = int(input("Restock quantity: "))
                        if qty >= 1:
                            break
                        print("Quantity must be at least 1")
                    except ValueError:
                        print("Please enter a valid number")

                # Ask if cost price needs to be updated
                while True:
                    cost_input = input("Current cost: ₹" + str(product["cost_price"]) + 
                                       ". New cost (0 to keep): ")
                    try:
                        new_cost = float(cost_input)
                        if new_cost >= 0:
                            break
                        print("Cost cannot be negative!")
                    except ValueError:
                        print("Please enter a valid number!")

                # Update cost price if a new cost is entered
                if new_cost > 0:
                    product["cost_price"] = new_cost

                # Add item to restock list
                restock_items.append({
                    "product": product,
                    "quantity": qty,
                    "cost": product["cost_price"]
                })

                # Ask if more items need to be restocked
                while True:
                    response = input("Do you want to add more items? (y/n): ").strip().lower()
                    if response.startswith('y'):
                        break
                    elif response.startswith('n'):
                        break
                    print("Error: Please enter 'y' or 'n'.")
                
                if response.startswith('n'):
                    break
            else:
                print("Invalid selection. Please try again.")
                
        except ValueError:
            print("Please enter a valid number")

    # Generate invoice and update inventory if restock was done
    if restock_items:
        generate_restock_invoice(supplier, restock_items)
        update_inventory(products, restock_items, "restock")

def update_inventory(products, items, action):
    """
    Update the quantity of products in inventory based on action.
    'sale' reduces quantity, 'restock' increases quantity.
    """
    for item in items:
        product = item["product"]
        if action == "sale":
            product["quantity"] = max(0, product["quantity"] - (item["quantity"] + item["free"]))
        else:  # restock
            product["quantity"] += item["quantity"]
    save_products(products)  # Save updated product list to file