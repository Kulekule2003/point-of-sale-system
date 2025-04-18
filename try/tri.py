class Itemlist:
    def __init__(self):
        self.item_list = {}

    def add_item(self, item_name, quantity, price):
        if item_name not in self.item_list:
            self.item_list[item_name] = {"quantity": quantity, "price": price}
        else:
            return "item already exists"

    def remove_item(self, item_name):
        if item_name in self.item_list:
            del self.item_list[item_name]

    def sell_item(self, item_name, quantity):
        if item_name in self.item_list and self.item_list[item_name]["quantity"] >= quantity:
            self.item_list[item_name]["quantity"] -= quantity
        else:
            return "not enough stock"
    6ho
if __name__ == "__main__":
    it = Itemlist()
    it.add_item("vita milk","30","4000")
    print(it.print_items())