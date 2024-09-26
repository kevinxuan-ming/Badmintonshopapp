import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

#Class representing a badminton racket with attributes like name, price, description, and image.
class Racket:
    def __init__(self, name, price, description, image_path):
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path

#Shop class to handle available rackets and shopping cart functionality.
class Shop:
    def __init__(self):
        self.rackets = [
            Racket("Yonex Astrox 99", 250, "High-performance racket for advanced players.", "Images/astrox99.PNG"),
            Racket("Li-Ning Axforce 80", 200, "Great for intermediate players.", "Images/axf80.PNG"),
            Racket("Victor Thruster K 9900", 220, "Powerful racket for attacking play.", "Images/VicThruster.PNG"),
            Racket("Yonex Duora Z-Strike", 230, "Versatile racket for all-round play.", "Images/zstrike.PNG"),
            Racket("Yonex Astrox 88D Pro", 210, "Aerodynamic design for faster swings.", "Images/88Dpro.PNG"),
            Racket("Victor Jetspeed S 12", 190, "Lightweight and fast.", "Images/jetspeeds12.PNG"),
            Racket("Yonex Nanoflare 800", 240, "Great control and speed.", "Images/NF800.PNG"),
            Racket("Li-Ning Halbertec 8000", 215, "Optimized for speed and power.", "Images/HB8000.PNG"),
            Racket("Yonex 100zz Navy Blue", 225, "Fast and powerful.", "Images/100zzNB.PNG"),
            Racket("Yonex Voltric Z-Force II", 260, "Top choice for professionals.", "Images/VZFORCE2.PNG")
        ]
        self.cart = []

    #Adds a selected racket and quantity to the cart.
    def add_to_cart(self, racket_index, quantity):
        racket = self.rackets[racket_index]
        self.cart.append((racket, quantity))
        messagebox.showinfo("Added to Cart", f"Added {quantity} x {racket.name} to your cart.")

    #Removes a selected item from the cart.
    def remove_from_cart(self, cart_index):
        if 0 <= cart_index < len(self.cart):
            removed_item = self.cart.pop(cart_index)
            messagebox.showinfo("Removed from Cart", f"Removed {removed_item[0].name} from your cart.")
        else:
            messagebox.showerror("Error", "Invalid cart selection")

    #Generates a receipt for all items in the cart.
    def get_receipt(self):
        receipt = "Receipt:\n"
        total = 0
        for racket, quantity in self.cart:
            cost = racket.price * quantity
            total += cost
            receipt += f"{racket.name} - ${racket.price} x {quantity} = ${cost}\n"
        receipt += f"Total: ${total}"
        return receipt

    #Returns a list of items currently in the cart.
    def get_cart_items(self):
        cart_details = ""
        for i, (racket, quantity) in enumerate(self.cart):
            cart_details += f"{i + 1}. {racket.name} - ${racket.price} x {quantity}\n"
        return cart_details

#Main application class that builds the GUI for the shop using tkinter.
class Application(tk.Tk):
    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self.title("Badminton Shop")
        
        #Variable to store the customer name.
        self.customer_name = tk.StringVar()

        #Create different pages for the app.
        self.start_page = self.create_start_page()
        self.racket_page = self.create_racket_page()
        self.receipt_page = self.create_receipt_page()
        self.cart_page = self.create_cart_page()

        #Show the start page initially.
        self.show_frame(self.start_page)

    #Switches between frames in the GUI.
    def show_frame(self, frame):
        frame.tkraise()

    #Creates the start page for the app.
    def create_start_page(self):
        frame = tk.Frame(self, bg="#E3F2FD")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Enter your name:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        name_entry = tk.Entry(frame, textvariable=self.customer_name)
        name_entry.pack(pady=10)

        tk.Button(frame, text="Start Shopping", command=self.start_shopping, bg="#64B5F6", fg="white").pack(pady=10)

        #Load and display the homepage image.
        home_image = Image.open("images/homepage.PNG")
        home_image = home_image.resize((300, 200), Image.LANCZOS)
        home_image_tk = ImageTk.PhotoImage(home_image)
        home_image_label = tk.Label(frame, image=home_image_tk, bg="#E3F2FD")
        home_image_label.image = home_image_tk 
        home_image_label.pack(pady=10)

        return frame

    #Validates the customer's name and proceeds to the racket page.
    def start_shopping(self):
        if self.customer_name.get():
            self.show_frame(self.racket_page)
        else:
            messagebox.showerror("Error", "Please enter your name")

    #Creates the page to display available rackets for selection.
    def create_racket_page(self):
        frame = tk.Frame(self, bg="#E8F5E9")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, textvariable=self.customer_name, bg="#E8F5E9", font=("Arial", 14)).pack(pady=10)

        self.racket_listbox = tk.Listbox(frame, height=10)
        for racket in self.shop.rackets:
            self.racket_listbox.insert(tk.END, f"{racket.name} - ${racket.price}")
        self.racket_listbox.pack(pady=10)
        self.racket_listbox.bind("<<ListboxSelect>>", self.display_racket_details)

        self.racket_image_label = tk.Label(frame, bg="#E8F5E9")
        self.racket_image_label.pack(pady=10)

        self.racket_description_label = tk.Label(frame, wraplength=250, bg="#E8F5E9", font=("Arial", 12))
        self.racket_description_label.pack(pady=10)

        tk.Label(frame, text="Quantity:", bg="#E8F5E9", font=("Arial", 12)).pack()
        self.quantity_entry = tk.Entry(frame)
        self.quantity_entry.pack(pady=10)

        tk.Button(frame, text="Add to Cart", command=self.add_to_cart, bg="#81C784", fg="white").pack(pady=10)
        tk.Button(frame, text="View Cart", command=self.show_cart, bg="#81C784", fg="white").pack(pady=10)  
        tk.Button(frame, text="Show Receipt", command=self.show_receipt, bg="#81C784", fg="white").pack(pady=10)
        return frame

    #Displays details (image and description) of the selected racket.
    def display_racket_details(self, event):
        selected_index = self.racket_listbox.curselection()
        if selected_index:
            racket = self.shop.rackets[selected_index[0]]
            racket_image = Image.open(racket.image_path)
            racket_image = racket_image.resize((150, 200), Image.LANCZOS)
            racket_image_tk = ImageTk.PhotoImage(racket_image)
            self.racket_image_label.config(image=racket_image_tk)
            self.racket_image_label.image = racket_image_tk 

            self.racket_description_label.config(text=racket.description)

    #Adds the selected racket and quantity to the cart.
    def add_to_cart(self):
        try:
            racket_index = self.racket_listbox.curselection()[0]
            quantity = int(self.quantity_entry.get())
            self.shop.add_to_cart(racket_index, quantity)
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Invalid selection or quantity")

    #Creates the receipt page.
    def create_receipt_page(self):
        frame = tk.Frame(self, bg="#FFF3E0")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Receipt", bg="#FFF3E0", font=("Arial", 16)).pack(pady=10)
        self.receipt_text = tk.Text(frame, height=10, width=50, bg="#FFE0B2")
        self.receipt_text.pack(pady=10)

        tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.racket_page), bg="#FFB74D", fg="white").pack(pady=10)
        return frame

    #Displays the receipt with all items in the cart.
    def show_receipt(self):
        self.receipt_text.delete(1.0, tk.END)
        receipt = self.shop.get_receipt()
        self.receipt_text.insert(tk.END, receipt)
        self.show_frame(self.receipt_page)

    #Creates the cart page where the customer can view or remove items from the cart.
    def create_cart_page(self):
        frame = tk.Frame(self, bg="#F3E5F5")
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Cart Items", bg="#F3E5F5", font=("Arial", 16)).pack(pady=10)
        self.cart_text = tk.Text(frame, height=10, width=50, bg="#E1BEE7")
        self.cart_text.pack(pady=10)

        tk.Label(frame, text="Select Item Number to Remove:", bg="#F3E5F5", font=("Arial", 12)).pack(pady=10)
        self.remove_entry = tk.Entry(frame)
        self.remove_entry.pack(pady=10)

        tk.Button(frame, text="Remove from Cart", command=self.remove_from_cart, bg="#BA68C8", fg="white").pack(pady=10)
        tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.racket_page), bg="#BA68C8", fg="white").pack(pady=10)
        return frame

    #Displays the cart and its items.
    def show_cart(self):
        self.cart_text.delete(1.0, tk.END)
        cart_items = self.shop.get_cart_items()
        self.cart_text.insert(tk.END, cart_items)
        self.show_frame(self.cart_page)

    #Removes the selected item from the cart by index.
    def remove_from_cart(self):
        try:
            cart_index = int(self.remove_entry.get()) - 1
            self.shop.remove_from_cart(cart_index)
            self.show_cart()  # Refresh the cart view after removal
        except ValueError:
            messagebox.showerror("Error", "Invalid selection")

#Main function that starts the application.
def main():
    shop = Shop()
    app = Application(shop)
    app.mainloop()

if __name__ == "__main__":
    main()
