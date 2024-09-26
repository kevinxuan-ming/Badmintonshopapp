# This class represents a Badminton Racket with a name and price
class Racket:
    def __init__(self, name, price):
        # Initializing the name and price attributes of the racket
        self.name = name
        self.price = price

# This class represents the badminton shop where rackets are sold
class Shop:
    def __init__(self):
        self.rackets = [
            Racket("Yonex Astrox 99", 250),
            Racket("Li-Ning N9ii", 200),
            Racket("Victor Thruster K 9900", 220),
            Racket("Yonex Duora Z-Strike", 230),
            Racket("Li-Ning Aeronaut 8000", 210),
            Racket("Victor Jetspeed S 12", 190),
            Racket("Yonex Nanoflare 700", 240),
            Racket("Li-Ning Turbo Charging 75", 215),
            Racket("Victor Auraspeed 90S", 225),
            Racket("Yonex Voltric Z-Force II", 260)
        ]
        self.cart = []

    # Method to display all available rackets to the customer
    def display_rackets(self):
        print("Available Badminton Rackets:")
        # Loop through the list of rackets and display each one with its price
        for idx, racket in enumerate(self.rackets):
            # Print the racket's index, name, and price
            print(f"{idx + 1}. {racket.name} - ${racket.price}")

    # Method to add a selected racket to the cart
    # racket_index is the index of the racket selected, quantity is the number of rackets
    def add_to_cart(self, racket_index, quantity):
        racket = self.rackets[racket_index - 1]
        self.cart.append((racket, quantity))
        print(f"Added {quantity} x {racket.name} to your cart.")

    # Method to display the receipt after shopping
    def show_receipt(self):
        print("\nReceipt:")
        # Initialize the total cost to 0
        total = 0
        for racket, quantity in self.cart:
            # Calculate the cost of each item in the cart (price * quantity)
            cost = racket.price * quantity
            # Add the item's cost to the running total
            total += cost
            # Display the racket's name, price, quantity, and total cost for that item
            print(f"{racket.name} - ${racket.price} x {quantity} = ${cost}")
        print(f"Total: ${total}")
        
# This class represents a customer shopping in the badminton shop
class Customer:
    def __init__(self, name):
        self.name = name

    # Method to simulate the shopping process for the customer
    def shop(self, shop):
        print(f"Welcome to the badminton shop, {self.name}!")
        while True:
            shop.display_rackets()
            try:
                # Ask the customer to choose a racket by entering its number
                racket_index = int(input("\nEnter the racket number to add to cart (0 to finish): "))
                # If the customer enters 0, break the loop and finish shopping
                if racket_index == 0:
                    break
                # Ask for the quantity of the selected racket
                quantity = int(input("Enter the quantity: "))
                shop.add_to_cart(racket_index, quantity)
            except (ValueError, IndexError):
                print("Invalid input, please try again.")
        shop.show_receipt()

# Main function that runs the shop program
def main():
    shop = Shop()
    customer_name = input("Enter your name: ")
    customer = Customer(customer_name)
    customer.shop(shop)

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
