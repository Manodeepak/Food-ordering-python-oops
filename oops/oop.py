import random
import time

class Swiggy:
    Non_veg_restaurant = {
        'Imperial Restaurant': {'Chicken Biriyani': 150, 'Chicken Kabab': 100, 'Mutton Biriyani': 250, 'Chilli Chicken': 120},
        'Calicut Restaurant': {'Dhonne Biriyani': 170, 'Beef Chukka': 220, 'Beef Biriyani': 160},
        '1947 Restaurant': {'Pepper Chicken': 120, 'Chicken Tandoori': 180, 'Hyderabadi Mutton': 280},
        'Kebabs & Curries': {'Butter Chicken': 210, 'Fish Fry': 160, 'Tandoori Chicken': 220, 'Chicken 65': 140},
        'The Spice Trail': {'Andhra Chicken Curry': 190, 'Prawn Masala': 260, 'Nethili Fry': 150, 'Egg Curry': 90},
        'Meat Lovers Hub': {'Grilled Chicken': 200, 'Mutton Rogan Josh': 270, 'Chicken Lolipop': 110, 'Mutton Keema': 180}
    }

    Veg_restaurant = {
        'Sree Krishna Bhavan': {'Paneer Butter Masala': 120, 'Veg Rice': 170, 'Veg Meals': 80, 'Curd Rice': 50},
        'Saravana Bhavan': {'Mini Tiffin': 70, 'Ghee Roast Dosa': 90, 'Poori Masala': 85, 'Idli Vada': 45},
        'Ananda Bhavan': {'Mushroom Masala': 110, 'Aloo Gobi': 100, 'Paneer Tikka': 150, 'Veg Pulao': 120},
        'Rasoi Veg Delight': {'Dal Makhani': 130, 'Jeera Rice': 80, 'Rajma Chawal': 100, 'Chole Bhature': 95},
        'Green Leaf': {'Veg Biryani': 140, 'Paneer Schezwan': 160, 'Kadai Paneer': 150, 'Mix Veg Curry': 110},
        'The Veg Point': {'Hakka Noodles': 100, 'Manchurian Gravy': 120, 'Gobi 65': 80, 'Fried Rice': 90}
    }

    def __init__(self, name, location, phone):
        self.name = name
        self.location = location
        self.phone = phone
        self.cart = []
        self.order_placed = False

    def sign_up(self):
        self.suname = input("Choose a username: ")
        self.spassword = input("Set a password: ")
        print("✅ Signed up successfully!")

    def log_in(self):
        for _ in range(3):
            uname = input("Enter username: ")
            pwd = input("Enter password: ")
            if uname == self.suname and pwd == self.spassword:
                print("✅ Login successful!")
                if self.otp_verification():
                    self.menu()
                return
            else:
                print("❌ Invalid credentials. Try again.")
        print("Too many failed attempts. Exiting.")

    def otp_verification(self):
        otp = random.randint(1000, 9999)
        print(f"📨 OTP sent: {otp} (valid for 60 seconds)")
        start = time.time()
        entered = int(input("Enter OTP: "))
        if time.time() - start <= 60 and entered == otp:
            print("✅ OTP verified.")
            return True
        else:
            print("❌ OTP invalid or expired.")
            return False

    def menu(self):
        while True:
            print("\n--- SWIGGY MENU ---")
            print("1. View Restaurants")
            print("2. Show Cart")
            print("3. Remove Item from Cart")
            print("4. Place Order")
            print("5. Track Order")
            print("6. Exit")

            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.display_restaurants()
            elif choice == '2':
                self.show_cart()
            elif choice == '3':
                self.remove_from_cart()
            elif choice == '4':
                self.place_order()
            elif choice == '5':
                self.track_order()
            elif choice == '6':
                print("👋 Thank you for using Swiggy!")
                break
            else:
                print("❌ Invalid choice.")

    def display_restaurants(self):
        rtype = input("Enter type (veg / non veg): ").strip().lower()
        if rtype == 'veg':
            self._display_restaurant_menu(self.Veg_restaurant)
        elif rtype == 'non veg':
            self._display_restaurant_menu(self.Non_veg_restaurant)
        else:
            print("❌ Invalid type. Please choose veg or non veg.")

    def _display_restaurant_menu(self, restaurants):
        print("\nAvailable Restaurants:")
        for name in restaurants:
            print(" -", name)
        rname = input("Enter restaurant name: ").strip().lower()
        selected = next((res for res in restaurants if res.lower() == rname), None)
        if not selected:
            print("❌ Restaurant not found.")
            return
        print(f"\n🍽️ Menu at {selected}:")
        for food, price in restaurants[selected].items():
            print(f"{food} - ₹{price}")
        self._add_to_cart(restaurants[selected])

    def _add_to_cart(self, menu):
        while True:
            item = input("Add food to cart (or type 'done'): ").strip().lower()
            if item == 'done':
                break
            matched = next((food for food in menu if food.lower() == item), None)
            if matched:
                self.cart.append((matched, menu[matched]))
                print(f"✅ Added {matched} to cart.")
            else:
                print("❌ Item not found.")

    def show_cart(self):
        if not self.cart:
            print("🛒 Your cart is empty.")
            return
        print("🛒 Your Cart:")
        total = 0
        for item, price in self.cart:
            print(f"{item} - ₹{price}")
            total += price
        print(f"💰 Total Amount: ₹{total}")

    def remove_from_cart(self):
        if not self.cart:
            print("🛒 Your cart is empty.")
            return
        while True:
            self.show_cart()
            to_remove = input("Enter food to remove (or 'done'): ").strip().lower()
            if to_remove == 'done':
                break
            matched = next((item for item in self.cart if item[0].lower() == to_remove), None)
            if matched:
                self.cart.remove(matched)
                print(f"✅ Removed {matched[0]} from cart.")
            else:
                print("❌ Item not found in cart.")

    def place_order(self):
        if not self.cart:
            print("❌ Cart is empty.")
            return
        self.show_cart()
        confirm = input("Place this order? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("❌ Order not placed.")
            return
        self._enter_address()
        self._choose_payment()
        self.order_placed = True
        print("✅ Your order has been placed!")

    def _enter_address(self):
        print("🏠 Enter delivery address:")
        area = input("Area: ")
        city = input("City: ")
        pincode = input("Pincode: ")
        print(f"📍 Address:\n{area}, {city}, {pincode}")

    def _choose_payment(self):
        print("\n💳 Payment Options:")
        print("1. UPI")
        print("2. Card")
        print("3. Cash on Delivery")
        method = input("Choose payment method: ")
        if method == '1':
            self._pay_upi()
        elif method == '2':
            self._pay_card()
        elif method == '3':
            print("🚫 COD not available currently.")
        else:
            print("❌ Invalid payment option.")

    def _pay_upi(self):
        upi = input("Enter UPI ID: ")
        print("🔄 Processing UPI payment...")
        time.sleep(2)
        print(f"✅ Payment successful! UPI ID: {upi}")

    def _pay_card(self):
        ctype = input("Card type (debit/credit): ").strip().lower()
        number = input("Last 4 digits of card: ")
        cvv = input("CVV: ")
        if len(number) == 4 and cvv.isdigit():
            print("🔄 Processing card payment...")
            time.sleep(2)
            print(f"✅ Payment successful via {ctype} card!")
        else:
            print("❌ Invalid card details.")

    def track_order(self):
        if not self.order_placed:
            print("❌ No order placed yet.")
            return
        print("📦 Tracking your order:")
        for status in [
            "Preparing your food...",
            "Packing your order...",
            "Out for delivery...",
            "Delivered! Enjoy your meal 😋"
        ]:
            print(status)
            time.sleep(2)

# Run program
name = input("Enter your name: ")
location = input("Enter your location: ")
phone = input("Enter your phone number: ")

user = Swiggy(name, location, phone)
user.sign_up()
user.log_in()
