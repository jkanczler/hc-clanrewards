class ClanRewards:
    def __init__(self, available_items, item_price):
        self.available_items = available_items
        self.distributed_items = {}
        self._item_price = item_price


    def distribute_item(self, clan_mate):
        item_to_distribute = self._get_item_to_distribute(clan_mate.demands)

        # if we can distribute an item, properly register quantities and history:
        if item_to_distribute is None:
            item_to_give = 'None'
        else:
            # handle the distributed items records:
            if item_to_distribute in self.distributed_items:
                # If one piece of this item already distributed, then increase the received quantity
                self.distributed_items[item_to_distribute]['quantity'] += 1
            else:
                # First time distributing this item initialize the quantity and maximum available quantity
                self.distributed_items[item_to_distribute] = { 'quantity': 1, 'max': self.available_items[item_to_distribute], 'history': [] }

            self.available_items[item_to_distribute] -= 1

            # record history
            if item_to_distribute in self.distributed_items:
                item_to_give = f"{item_to_distribute} ({self.distributed_items[item_to_distribute]['quantity']}/{self.distributed_items[item_to_distribute]['max']})"
            else:
                item_to_give = item_to_distribute

            self.distributed_items[item_to_distribute]['history'].append(f"{item_to_give} kiosztva {clan_mate.name} klántagnak {clan_mate.glory + self._item_price} glorynál.")

        clan_mate.give_item(item_to_give)

        return item_to_give


    def print_distribution_history(self):
        print('--- Jutalmak Tárgy Szerint ---')

        index = 0
        for item in self.available_items:
            if self.distributed_items.get(item):
                for history in self.distributed_items[item]['history']:
                    index += 1
                    print(f'{index}. {history}')

        print()


    def _get_item_to_distribute(self, demands):
        for demand in demands:
            if demand['quantity'] > 0:
                for demanded_item in demand['items']:
                    if demanded_item in self.available_items and self.available_items[demanded_item] > 0:
                        return demanded_item

        return None
