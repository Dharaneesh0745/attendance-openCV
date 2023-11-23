class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item_name, qty):
        item = (item_name, qty)
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item[0] == item_name:
                self.items.remove(item)
                break

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item[1]
        return total

cart = Cart()
cart.add_item("Mango", 100)
cart.add_item("Banana", 20)
cart.add_item("Papaya", 30)

print("Current Items : ")
for item in cart.items:
    print(item[0], '-', item[1])
total_qty = cart.calculate_total()
print("Toatl Quantity : ", total_qty)

cart.remove_item("Banana")

print("Updated Cart : ")
for item in cart.items:
    print(item[0], '-', item[1])

total_qty = cart.calculate_total()
print("Total Quantity : ", total_qty)