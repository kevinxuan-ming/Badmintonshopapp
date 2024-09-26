import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os
    

#Function to load user data from an external JSON file, in this function it will path to the JSON file where users data are stored, check if users exist, and create a new file for user 
#if do not exist.
def load_user_data():
    file_path = "user_data.json"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)#Initialises an empty dictionary for user data.
#This helps open the file in read mode, load and return the user data.
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:#This function over here handles cases where the file is not a valid JSON.
        return {}


#Function to save user data to an external JSON file by opening the file in write mode, and saves user data to the file.
def save_user_data(user_data):
    with open("user_data.json", 'w') as file:
        json.dump(user_data, file)


#This is the class that represents the product in the shop for objects racket and shoes with all their attributes, 
# it gives its name, price, description, path to the product's image, and stock availability.
class Product:
    def __init__(self, name, price, description, image_path, stock):
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path
        self.stock = stock  

#The shop class represents the shop's inventory and cart system, it lists all of the rackets and shoes available with their details and stock and is held in a list.
class Shop:
    def __init__(self):
        self.rackets = [
            Product("Yonex 99", 250, "High-performance racket for advanced players.", "Images/astrox99.PNG",10),
            Product("Li-Ning Axforce 80", 200, "Great for intermediate players.", "Images/axf80.PNG",10),
            Product("Victor 9900", 220, "Powerful racket for attacking play.", "Images/VicThruster.PNG",10),
            Product("Yonex Duora Z-Strike", 230, "Versatile racket for all-round play.", "Images/zstrike.PNG",10),
            Product("Yonex Astrox 88D Pro", 210, "Aerodynamic design for faster swings.", "Images/88Dpro.PNG",10),
            Product("Victor  S 12", 190, "Lightweight and fast.", "Images/jetspeeds12.PNG",10),
            Product("Yonex Nanoflare 800", 240, "Great control and speed.", "Images/NF800.PNG",10),
            Product("Li-Ning HB 800000", 215, "Optimized for speed and power.", "Images/HB8000.PNG",10),
            Product("Yonex 100zz ", 225, "Fast and powerful.", "Images/100zzNB.PNG",10),

        ]
        self.shoes = [
            Product("Yonex EclipsionZ ", 130, "Comfortable and durable shoes.", "Images/shoe1.PNG",10),
            Product("Victor A960 Shoe", 140, "Designed for speed and agility.", "Images/Vica960.PNG",10),           
            Product("Yonex SHB", 125, "Perfect for quick movements.", "Images/shoe6.PNG",10),
            Product("Victor P9200 Shoe", 145, "Premium shoes with great support.", "Images/shoe7.PNG",10),
            Product("Yonex X2 ", 150, "High cushioning for intense play.", "Images/shoe9.PNG",10),
            Product("Victor A830    ", 115, "Affordable and reliable.", "Images/shoe10.PNG",10)
        ]
        self.cart = []

#Function to add product to cart, by first determining if the item is a shoe or racket and then it will select the shoe or racket from the list.
    def add_to_cart(self, product_index, quantity, product_type):
        if product_type == "Rackets":
            product = self.rackets[product_index]
        else:
            product = self.shoes[product_index]
#This place is the method for product stock, it first checks if there is enough stock, and the stock would decrease for items added to users cart by the quantity they have
#added. If user selects quantity greater than available stock, than an error message would show up.
        if product.stock >= quantity:  
            product.stock -= quantity  
            self.cart.append((product, quantity))
            messagebox.showinfo("Added to Cart", f"Added {quantity} x {product.name} to your cart.")
        else:
            messagebox.showerror("Stock Error", f"Only {product.stock} units of {product.name} are available.")

#This function over here will remove products from cart, by first checking if user entered a valid index and then removes it from users cart. This will also add how many
#quantity the user has removed from an item to its stock.
    def remove_from_cart(self, cart_index):
        if 0 <= cart_index < len(self.cart):
            removed_item = self.cart.pop(cart_index)
            removed_item[0].stock += removed_item[1]  # Increase stock back
            messagebox.showinfo("Removed from Cart", f"Removed {removed_item[0].name} from your cart.")
        else:
            messagebox.showerror("Error", "Invalid cart selection")

#Here is the receipt method, it will loop through the cart and calculate the cost of each product, and add them all up for total cost and return the generated receipt.
    def get_receipt(self):
        receipt = "Receipt:\n"
        total = 0
        for product, quantity in self.cart:
            cost = product.price * quantity
            total += cost
            receipt += f"{product.name} - ${product.price} x {quantity} = ${cost}\n"
        receipt += f"Total: ${total}"
        return receipt
#This function helps to retrieve the items in the cart and display them by first initialising the empty string for cart details, loop through cart items and then add each
#item to the display string.
    def get_cart_items(self):
        cart_details = ""
        for i, (product, quantity) in enumerate(self.cart):
            cart_details += f"{i + 1}. {product.name} - ${product.price} x {quantity}\n"
        return cart_details

#The application class represents the main GUI application.
class Application(tk.Tk):
    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self.title("Badminton Shop")
        #This is where the size of the window is adjusted.
        self.geometry("500x500")
        #This will help load user from JSON file and initialise the current user.
        self.user_data = load_user_data() 
        self.current_user = None

        self.customer_name = tk.StringVar()
        self.selected_product_type = tk.StringVar(value="Rackets")
        #This over here creates different windows(frame) for the application. It will always show the start page and login page by default.
        self.start_page = self.create_start_page()
        self.login_page = self.create_login_page()  
        self.product_page = self.create_product_page()
        self.receipt_page = self.create_receipt_page()
        self.cart_page = self.create_cart_page()
        self.stock_page = self.create_stock_page()  
        self.show_frame(self.start_page)
        
        self.show_frame(self.login_page) 
#This function helps raise the selected frame to the front.
    def show_frame(self, frame):
        frame.tkraise()
#This function is the method in creating the login page with usrname and password input.
    def create_login_page(self):
        frame = tk.Frame(self, bg="#E3F2FD")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Username:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(frame)
        self.username_entry.pack(pady=10)

        tk.Label(frame, text="Password:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(frame, text="Login", command=self.login, bg="#64B5F6", fg="white").pack(pady=10)
        tk.Button(frame, text="Create Account", command=self.create_account, bg="#64B5F6", fg="white").pack(pady=10)

        return frame
#This is the method to handle user login. It first retrives the username and password inputted by user and check if it exists in the stored data JSON file.
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.user_data and self.user_data[username] == password:
            self.current_user = username
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.show_frame(self.start_page)
        else:
            messagebox.showerror("Error", "Invalid username or password")
#This is the method to create an account. It firsts retrieves the users username an dpassword inputted, an if it already exits in the JSON file, an error messagebox will pop up.
#If the user does not exist, it will proceed to creating this new account by storing the new data into the JSON file.
    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists")
        else:
            if username and password:
                self.user_data[username] = password
                save_user_data(self.user_data)
                messagebox.showinfo("Account Created", "Account successfully created!")
            else:
                messagebox.showerror("Error", "Please provide both username and password")
                
    def create_start_page(self):
        frame = tk.Frame(self, bg="#E3F2FD")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Enter your name:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        name_entry = tk.Entry(frame, textvariable=self.customer_name)
        name_entry.pack(pady=10)

        tk.Button(frame, text="Start Shopping", command=self.start_shopping, bg="#64B5F6", fg="white").pack(pady=10)

        home_image = Image.open("images/homepage.PNG")
        home_image = home_image.resize((300, 200), Image.LANCZOS)
        home_image_tk = ImageTk.PhotoImage(home_image)
        home_image_label = tk.Label(frame, image=home_image_tk, bg="#E3F2FD")
        home_image_label.image = home_image_tk
        home_image_label.pack(pady=10)

        return frame
#Function to create the stock page
    def create_stock_page(self):
        frame = tk.Frame(self, bg="#FFFDE7")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.stock_text = tk.Text(frame, state='disabled', width=60, height=20)
        self.stock_text.pack(pady=20)

        back_button = tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.product_page), bg="#FDD835", fg="black")
        back_button.pack(pady=10)

        return frame
#This is the method to update and display the stock levels.
    def update_stock_display(self):
        self.stock_text.configure(state='normal')
        self.stock_text.delete(1.0, tk.END)
#This place ombines the racket items and shoes items as one product list.
        product_list = self.shop.rackets + self.shop.shoes  
        stock_info = "Product Stock:\n\n"

        for product in product_list:
            stock_info += f"{product.name}: {product.stock} in stock\n"

        self.stock_text.insert(tk.END, stock_info)
        self.stock_text.configure(state='disabled')
#This is the method to show the stock page and refresh the displayed stock information, this is done by calling the update_stock_display method to refresh the stock information.
    def show_stock(self):
        self.update_stock_display()
        self.show_frame(self.stock_page)
        
    def start_shopping(self):
        if self.customer_name.get():
            self.show_frame(self.product_page)
        else:
            messagebox.showerror("Error", "Please enter your name")
#The function for the main product page.
    def create_product_page(self):
        frame = tk.Frame(self, bg="#E8F5E9")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, textvariable=self.customer_name, bg="#E8F5E9", font=("Arial", 14)).pack(pady=10)

        radio_frame = tk.Frame(frame, bg="#E8F5E9")
        radio_frame.pack(pady=10)

        tk.Radiobutton(radio_frame, text="Rackets", variable=self.selected_product_type, value="Rackets", command=self.update_product_grid, bg="#E8F5E9").pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(radio_frame, text="Shoes", variable=self.selected_product_type, value="Shoes", command=self.update_product_grid, bg="#E8F5E9").pack(side=tk.LEFT, padx=20)

        #This helps centering the products on display.
        center_frame = tk.Frame(frame, bg="#E8F5E9")
        center_frame.pack(expand=True, padx=50, pady=20)

        #This adds canvas for scroll functionality on the product page.
        self.canvas = tk.Canvas(center_frame, bg="#E8F5E9")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

      
        self.scrollbar = tk.Scrollbar(center_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        #Creating a frame inside the canvas to hold the products.
        self.product_frame = tk.Frame(self.canvas, bg="#E8F5E9")
        self.canvas.create_window((0, 0), window=self.product_frame, anchor="nw")

        #This helps bind the canvas to the scroll functionality.
        self.product_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        button_frame = tk.Frame(frame, bg="#E8F5E9")
        button_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(button_frame, text="View Cart", command=self.show_cart, bg="#81C784", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="View Product Stock", command=self.show_stock, bg="#FDD835", fg="black").pack(pady=10)  # Button to show stock
        tk.Button(button_frame, text="Show Receipt", command=self.show_receipt, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=10)

        self.update_product_grid()

        return frame
#This method helps update the dispay grid of all items, shoes and rackets.
    def update_product_grid(self):
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        product_list = self.shop.rackets if self.selected_product_type.get() == "Rackets" else self.shop.shoes
#Adjust this number to change the number of columns.
        max_columns = 3 
        row = 0
        col = 0
#This part iterates over the products in the selected product list, it firsts opens the image file for each item and resizes it, and creates a frame for each product to contain
#its image and description. It also creates a label for product name and description, and a button for add to cart and adds it to the frame.
        for idx, product in enumerate(product_list):
            image = Image.open(product.image_path)
            image = image.resize((100, 200), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)

            frame = tk.Frame(self.product_frame, bd=2, relief="groove", bg="#FFFFFF")
            frame.grid(row=row, column=col, padx=5, pady=5)

            image_label = tk.Label(frame, image=image_tk, bg="#FFFFFF")
            image_label.image = image_tk
            image_label.pack()

            tk.Label(frame, text=product.name, bg="#FFFFFF").pack()
            tk.Label(frame, text=f"${product.price}", bg="#FFFFFF").pack()

            tk.Button(frame, text="Add to Cart", command=lambda idx=idx: self.add_to_cart(idx)).pack()
#This place updates the position of each product frame, which is just +1 of the previous, and if the maximum coloumn is reached it will start a new row.
            col += 1
            if col >= max_columns:
                col = 0
                row += 1
#This is the method to add a product to the cart based on its index. It first asks the usrers desired quantity of the product.
    def add_to_cart(self, product_index):
        quantity = simpledialog.askinteger("Quantity", "Enter the quantity:")
        if quantity is not None and quantity > 0:
            self.shop.add_to_cart(product_index, quantity, self.selected_product_type.get())
        else:
            messagebox.showerror("Error", "Invalid quantity")

    def show_cart(self):
        self.update_cart_display()
        self.show_frame(self.cart_page)
#This is the method to update the cart display if something is added or remoeved. It first retrieves the items in the cart and clears all existing text in the cart display
#and hence inserts the new updated cart items onto the display.
    def update_cart_display(self):
        cart_items = self.shop.get_cart_items()
        self.cart_text.configure(state='normal')
        self.cart_text.delete(1.0, tk.END)
        self.cart_text.insert(tk.END, cart_items)
        self.cart_text.configure(state='disabled')

    def create_cart_page(self):
        frame = tk.Frame(self, bg="#FFEBEE")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.cart_text = tk.Text(frame, state='disabled', width=60, height=20)
        self.cart_text.pack(pady=20)

        remove_button = tk.Button(frame, text="Remove from Cart", command=self.remove_from_cart, bg="#E57373", fg="white")
        remove_button.pack(pady=10)

        back_button = tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.product_page), bg="#EF5350", fg="white")
        back_button.pack(pady=10)

        return frame
#This is the method to remove items from the cart. It will first check if the item is in the cart, and then remove if valid and update the cart display.
    def remove_from_cart(self):
        if self.shop.cart:
            cart_index = simpledialog.askinteger("Remove Item", "Enter the cart item number to remove:")
            if cart_index is not None:
                self.shop.remove_from_cart(cart_index - 1)
                self.update_cart_display()
        else:
            messagebox.showinfo("Cart Empty", "No items to remove from the cart.")

    def create_receipt_page(self):
        frame = tk.Frame(self, bg="#FFFDE7")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.receipt_text = tk.Text(frame, state='disabled', width=60, height=20)
        self.receipt_text.pack(pady=20)

        receipt_button = tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.product_page), bg="#FDD835", fg="black")
        receipt_button.pack(pady=10)

        return frame
 
    def show_receipt(self):
        self.receipt_text.configure(state='normal')
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, self.shop.get_receipt())
        self.receipt_text.configure(state='disabled')
        self.show_frame(self.receipt_page)
shop = Shop()
app = Application(shop)
app.mainloop()
