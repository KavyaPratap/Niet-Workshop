class Product:
    def __init__(self, product_id, name, price, quantity_available):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        return self._product_id

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_quantity_available(self):
        return self._quantity_available

    def set_quantity_available(self, value):
        if value >= 0:
            self._quantity_available = value
        else:
            print("Error: Quantity available cannot be negative.")

    def decrease_quantity(self, amount):
        if not isinstance(amount, int) or amount <= 0:
            print("Error: Amount to decrease must be a positive integer.")
            return False
        if self._quantity_available >= amount:
            self._quantity_available -= amount
            return True
        else:
            print(f"Not enough stock for {self._name}. Available: {self._quantity_available}")
            return False

    def increase_quantity(self, amount):
        if not isinstance(amount, int) or amount <= 0:
            print("Error: Amount to increase must be a positive integer.")
            return
        self._quantity_available += amount

    def display_details(self):
        return (f"Product ID: {self._product_id}, Name: {self._name}, "
                f"Price: ₹{self._price:.2f}, Available: {self._quantity_available}")

    def to_dict(self):
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_available": self._quantity_available,
            "type": "product"
        }

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, weight):
        super().__init__(product_id, name, price, quantity_available)
        self._weight = weight

    def get_weight(self):
        return self._weight

    def display_details(self):
        return (f"Product ID: {self._product_id}, Name: {self._name}, "
                f"Price: ₹{self._price:.2f}, Available: {self._quantity_available}, "
                f"Weight: {self._weight:.2f} kg")

    def to_dict(self):
        data = super().to_dict()
        data["weight"] = self._weight
        data["type"] = "physical"
        return data

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, download_link):
        super().__init__(product_id, name, price, quantity_available)
        self._download_link = download_link

    def get_download_link(self):
        return self._download_link

    def display_details(self):
        return (f"Product ID: {self._product_id}, Name: {self._name}, "
                f"Price: ₹{self._price:.2f}, Available: {self._quantity_available}, "
                f"Download Link: {self._download_link} (placeholder)")

    def to_dict(self):
        data = super().to_dict()
        data["download_link"] = self._download_link
        data["type"] = "digital"
        return data

class CartItem:
    def __init__(self, product, quantity):
        self._product = product
        self._quantity = quantity

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, value):
        if value >= 0:
            self._quantity = value
        else:
            print("Error: Cart item quantity cannot be negative.")

    def calculate_subtotal(self):
        return self._product.get_price() * self._quantity

    def __str__(self):
        return (f"Item: {self._product.get_name()}, Quantity: {self._quantity}, "
                f"Price: ₹{self._product.get_price():.2f}, Subtotal: ₹{self.calculate_subtotal():.2f}")

    def to_dict(self):
        return {
            "product_id": self._product.get_product_id(),
            "quantity": self._quantity
        }

class ShoppingCart:
    def __init__(self):
        self._items = {}
        self.catalog = {}

        self._initialize_dummy_catalog()

    def _initialize_dummy_catalog(self):
        print("Initializing with dummy products in memory...")
        self.catalog['P1'] = PhysicalProduct('P1', 'Laptop', 65000.00, 10, 2.5)
        self.catalog['P2'] = DigitalProduct('P2', 'E-Book Python Basics', 250.00, 100, 'http://demo1.com/python')
        self.catalog['P3'] = Product('P3', 'Mouse', 150.00, 50)
        self.catalog['P4'] = PhysicalProduct('P4', 'Keyboard', 750.00, 20, 1.0)
        self.catalog['P5'] = DigitalProduct('P5', 'Software License', 199.99, 50, 'http://demo2.com/software')

    def add_item(self, product_id, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            print("Error: Quantity must be a positive integer.")
            return False

        if product_id not in self.catalog:
            print(f"Product with ID '{product_id}' not found in catalog.")
            return False

        product = self.catalog[product_id]

        if product.get_quantity_available() < quantity:
            print(f"Not enough stock for {product.get_name()}. Only {product.get_quantity_available()} available.")
            return False

        if product_id in self._items:
            cart_item = self._items[product_id]
            product.decrease_quantity(quantity)
            cart_item.set_quantity(cart_item.get_quantity() + quantity)
            print(f"Added {quantity} more of {product.get_name()} to cart.")
        else:
            product.decrease_quantity(quantity)
            self._items[product_id] = CartItem(product, quantity)
            print(f"Added {quantity} of {product.get_name()} to cart.")

        return True

    def remove_item(self, product_id):
        if product_id not in self._items:
            print(f"Product with ID '{product_id}' not found in your cart.")
            return False

        cart_item = self._items[product_id]
        product = cart_item.get_product()
        quantity_to_return = cart_item.get_quantity()

        product.increase_quantity(quantity_to_return)
        del self._items[product_id]
        print(f"Removed {product.get_name()} from cart.")

        return True

    def update_quantity(self, product_id, new_quantity):
        if not isinstance(new_quantity, int) or new_quantity < 0:
            print("Error: New quantity must be a non-negative integer.")
            return False

        if product_id not in self._items:
            print(f"Product with ID '{product_id}' not found in your cart.")
            return False

        cart_item = self._items[product_id]
        product = cart_item.get_product()
        old_quantity = cart_item.get_quantity()

        if new_quantity == old_quantity:
            print(f"Quantity for {product.get_name()} is already {new_quantity}.")
            return True

        quantity_difference = new_quantity - old_quantity

        if quantity_difference > 0:
            if product.get_quantity_available() < quantity_difference:
                print(f"Not enough stock for {product.get_name()}. Only {product.get_quantity_available()} more available.")
                return False
            product.decrease_quantity(quantity_difference)
        elif quantity_difference < 0:
            product.increase_quantity(abs(quantity_difference))

        if new_quantity == 0:
            del self._items[product_id]
            print(f"Quantity for {product.get_name()} updated to 0. Item removed from cart.")
        else:
            cart_item.set_quantity(new_quantity)
            print(f"Quantity for {product.get_name()} updated to {new_quantity}.")

        return True

    def get_total(self):
        total = 0.0
        for item in self._items.values():
            total += item.calculate_subtotal()
        return total

    def display_cart(self):
        print("\n--- Your Shopping Cart ---")
        if not self._items:
            print("Your cart is empty.")
            return

        for item in self._items.values():
            print(item)

        print(f"--------------------------")
        print(f"Grand Total: ₹{self.get_total():.2f}")
        print("--------------------------")

    def display_products(self):
        print("\n--- Available Products ---")
        if not self.catalog:
            print("No products available in the catalog.")
            return

        for product in self.catalog.values():
            print(product.display_details())
        print("--------------------------")

cart = ShoppingCart()

while True:
    print("\n--- Shopping Cart Menu ---")
    print("1. View Products")
    print("2. Add Item to Cart")
    print("3. View Cart")
    print("4. Update Quantity in Cart")
    print("5. Remove Item from Cart")
    print("6. Checkout")
    print("7. Exit")
    print("--------------------------")

    choice = input("Enter your choice: ")

    if choice == '1':
        cart.display_products()
    elif choice == '2':
        product_id = input("Enter Product ID to add: ").strip().upper()
        quantity_str = input("Enter quantity: ")
        
        if quantity_str.isdigit():
            quantity = int(quantity_str)
            cart.add_item(product_id, quantity)
        else:
            print("Invalid quantity. Please enter a whole number.")
    elif choice == '3':
        cart.display_cart()
    elif choice == '4':
        product_id = input("Enter Product ID to update: ").strip().upper()
        new_quantity_str = input("Enter new quantity: ")

        if new_quantity_str.isdigit():
            new_quantity = int(new_quantity_str)
            cart.update_quantity(product_id, new_quantity)
        else:
            print("Invalid quantity. Please enter a whole number.")
    elif choice == '5':
        product_id = input("Enter Product ID to remove: ").strip().upper()
        cart.remove_item(product_id)
    elif choice == '6':
        print("\n--- Checkout ---")
        print(f"Your total is: ₹{cart.get_total():.2f}")
        print("Thank you for your purchase, Visit Again!")
    elif choice == '7':
        print("Exiting Shopping Cart. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
