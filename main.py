""" this is a point of sale system software for a hardware store."""

class Itemlist:
   
    def __init__(self):
        # {"item_name":{"quantity":"",}}. thr format of input
        self.item_list = {}

    def add_item(self, item_name, quantity, price ):
        #this is to add items to the item list, by adding a name, quantity, price
        #the name includes the unique details that will help identify the different products
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        if self.item_name not in self.item_list.keys():
            self.item_list[self.item_name]={"quantity":self.quantity,"self.price":self.price}
        else:
            return "item already exists"

    def remove_item(self, item_name):
        self.item_name = item_name
        #delete an item by giving it's name
        if self.item_list[self.item_name] in self.item_list.keys:
            del self.item_list[self.item_name]
    
    def sell_item(self, item_name, quantity):
        self.item_name = item_name
        self.quantity = quantity
        #selling an item decrements the quantity
        if self.item_list[self.item_name]["quantity"] > 0:
            self.item_list[self.item_name]["quantity"] -= self.quantity
        else:
            return "no stock"

def main():
    pass

if __name__ == "__main__":
    main()