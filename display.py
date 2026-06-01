import datetime  # Import the datetime module for getting current date and time

# Function to display a list of products in a formatted table
def display_products(products):
    """Show products in a table."""

    # Print the table header with column titles
    print(f"\n{'Product':<20} {'Brand':<15} {'Stock':<10} {'Price (₹)':<15} {'Country':<10}")
    print("-" * 70)  # Print a separator line

    # Iterate through each product and print its details in a formatted row
    for p in products:
        print(f"{p['name']:<20} {p['brand']:<15} {p['quantity']:<10} ₹{p['cost_price'] * 2:<14.2f} {p['country']:<10}")

# Function to generate a sales invoice with "Buy 3 Get 1 Free" offer and VAT
def generate_sale_invoice(customer, cart):
    """Generate a sales invoice with 'Buy 3 Get 1 Free' applied and 13% VAT."""

    # Create a timestamp string for file naming
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Generate a unique filename using customer name and timestamp
    filename = f"invoice_{customer}_{timestamp}.txt"

    total = 0  # Variable to hold the total cost before VAT

    # Open the invoice file in write mode with UTF-8 encoding
    with open(filename, "w", encoding='utf-8') as f:

        # Write invoice header
        f.write("================================================\n") 
        f.write("============ WeCare Sales Invoice ============\n")
        f.write("================================================\n")
        f.write(f"Date: {datetime.datetime.now()}\n")  # Current date and time
        f.write(f"Customer Name: {customer}\n")        # Customer name
        f.write("-" * 50 + "\n")
        f.write(f"{'Product':<20} {'Qty':<10} {'Free':<10} {'Subtotal':<10}\n")

        # Process each item in the cart
        for item in cart:
            subtotal = item["quantity"] * (item["product"]["cost_price"] * 2)
            total += subtotal
            f.write(f"{item['product']['name']:<20} {item['quantity']:<10} {item['free']:<10} ₹{subtotal:<10.2f}\n")

        vat = total * 0.13
        grand_total = total + vat

        f.write("-" * 50 + "\n")
        f.write(f"Subtotal: ₹{total:.2f}\n")
        f.write(f"VAT (13%): ₹{vat:.2f}\n")
        f.write(f"TOTAL: ₹{grand_total:.2f}\n")
        f.write(f"Free Items: {sum(item['free'] for item in cart)}\n")

# Function to generate a restocking invoice for suppliers
def generate_restock_invoice(supplier, items):
    """Generate restock invoice with 13% VAT."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"restock_{supplier}_{timestamp}.txt"
    subtotal = 0

    with open(filename, "w", encoding='utf-8') as f:
        f.write("================================================\n")
        f.write(f"============ WeCare Restock Invoice ============\n")
        f.write("================================================\n")
        f.write(f"Supplier: {supplier}\n")
        f.write(f"Date: {datetime.datetime.now()}\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Product':<20} {'Qty':<10} {'Price':<10} {'Subtotal':<10}\n")
        f.write("-" * 50 + "\n")

        for item in items:
            line_total = item['quantity'] * item['cost']
            subtotal += line_total
            f.write(f"{item['product']['name']:<20} {item['quantity']:<10} ₹{item['cost']:<9.2f} ₹{line_total:<10.2f}\n")

        vat = subtotal * 0.13
        grand_total = subtotal + vat

        f.write("-" * 50 + "\n")
        f.write(f"Subtotal: ₹{subtotal:.2f}\n")
        f.write(f"VAT (13%): ₹{vat:.2f}\n")
        f.write(f"TOTAL: ₹{grand_total:.2f}\n")