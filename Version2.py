import tkinter as tk
from tkinter import messagebox

class Racket:
    def __init__(self, name, price):
        self.name = name
        self.price = price

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

    def add_to_cart(self, racket_index, quantity):
        racket = self.rackets[racket_index]
        self.cart.append((racket, quantity))
        messagebox.showinfo("Added to Cart", f"Added {quantity} x {racket.name} to your cart.")

    def get_receipt(self):
        receipt = "Receipt:\n"
        total = 0
        for racket, quantity in self.cart:
            cost = racket.price * quantity
            total += cost
            receipt += f"{racket.name} - ${racket.price} x {quantity} = ${cost}\n"
        receipt += f"Total: ${total}"
        return receipt

class Application(tk.Tk):
    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self.title("Badminton Shop")
        
        self.customer_name = tk.StringVar()

        self.start_page = self.create_start_page()
        self.racket_page = self.create_racket_page()
        self.receipt_page = self.create_receipt_page()

        self.show_frame(self.start_page)

    def show_frame(self, frame):
        frame.tkraise()

    def create_start_page(self):
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Enter your name:").pack(pady=10)
        name_entry = tk.Entry(frame, textvariable=self.customer_name)
        name_entry.pack(pady=10)

        tk.Button(frame, text="Start Shopping", command=self.start_shopping).pack(pady=10)
        return frame

    def start_shopping(self):
        if self.customer_name.get():
            self.show_frame(self.racket_page)
        else:
            messagebox.showerror("Error", "Please enter your name")

    def create_racket_page(self):
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, textvariable=self.customer_name).pack(pady=10)

        self.racket_listbox = tk.Listbox(frame, height=10)
        for racket in self.shop.rackets:
            self.racket_listbox.insert(tk.END, f"{racket.name} - ${racket.price}")
        self.racket_listbox.pack(pady=10)

        tk.Label(frame, text="Quantity:").pack()
        self.quantity_entry = tk.Entry(frame)
        self.quantity_entry.pack(pady=10)

        tk.Button(frame, text="Add to Cart", command=self.add_to_cart).pack(pady=10)
        tk.Button(frame, text="Show Receipt", command=self.show_receipt).pack(pady=10)
        return frame

    def add_to_cart(self):
        try:
            racket_index = self.racket_listbox.curselection()[0]
            quantity = int(self.quantity_entry.get())
            self.shop.add_to_cart(racket_index, quantity)
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Invalid selection or quantity")

    def create_receipt_page(self):
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Receipt").pack(pady=10)
        self.receipt_text = tk.Text(frame, height=10, width=50)
        self.receipt_text.pack(pady=10)

        tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.racket_page)).pack(pady=10)
        return frame

    def show_receipt(self):
        self.receipt_text.delete(1.0, tk.END)
        receipt = self.shop.get_receipt()
        self.receipt_text.insert(tk.END, receipt)
        self.show_frame(self.receipt_page)

def main():
    shop = Shop()
    app = Application(shop)
    app.mainloop()

if __name__ == "__main__":
    main()