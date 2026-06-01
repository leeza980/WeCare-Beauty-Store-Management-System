
# Import required modules and functions

import datetime  # For handling date and time 
from read import load_products  # Function to load product data from file
from write import save_products  # Function to save product data to file

from display import display_products, generate_sale_invoice, generate_restock_invoice  
# Functions to display products and generate invoices


from operations import process_sale, process_restock, get_valid_input, get_yes_no  
# Functions to handle sales, restocks, and input validation

# Main function to run the store system
def main():
    """Main function to run the WeCare Beauty Store system"""

    # Load products from file into memory at the start of the program
    products = load_products()
    
    # Infinite loop to keep the system running until user exits
    while True:
        # Display main menu
        print("\n================================================") 
        print("\n============== WeCare Beauty Store ==============")
        print("1. Sell Products")      # Option to sell products to customer
        print("2. Restock Products")   # Option to restock inventory
        print("3. View Products")      # Option to view current stock
        print("4. Exit")               # Exit the system
        print("\n================================================") 
        
        # Get user's choice with input validation (must be an integer between 1 and 4)
        choice = get_valid_input("Enter a choice (1-4): ", int, 1, 4)
        
        # Based on user input, call corresponding functionality
        if choice == 1:
            process_sale(products)  # Handle product sale
        elif choice == 2:
            process_restock(products)  # Handle restocking
        elif choice == 3:
            display_products(products)  # Display current product list
        else:
            save_products(products)  # Save updated products to file before exiting
            print("Thank you for using WeCare System!")  # Farewell message
            break  # Exit the loop and end the program

# Entry point check to run main only when script is executed directly
if __name__ == "__main__":
    main()
