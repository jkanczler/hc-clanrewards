class ClanMate:
    # Price of any items, this will be deducated from the glory after each item received
    _item_price = 50000

    def __init__(self, init_obj):
        self.name = init_obj['name']
        self.glory = init_obj['glory']
        self.demands = init_obj['demands']
        self.received = []

        for demand in self.demands:
            demand['original'] = demand['quantity']

    def buy_item(self, item):
        self.received.append(item)
        self.glory -= self._item_price

        for demand in self.demands:
            if item in demand['items']:
                # Reduce the demanded quantity
                demand['quantity'] -= 1

        print(f"{self.name} megkapja a következő tárgyat: '{item}'. Glory levonás: {self.glory + self._item_price} - {self._item_price} = {self.glory}")
