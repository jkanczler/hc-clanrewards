class ClanRewards:
    def __init__(self, available_items, item_price):
        self.available_items = available_items
        self._item_price = item_price
        self._init_distributed_items()


    def distribute_item(self, clan_mate):
        current_demand = self._get_current_demand(clan_mate.demands)
        item_to_distribute = self._get_item_to_distribute(current_demand)

        # if we can distribute an item, properly register quantities and history:
        if not item_to_distribute is None:
            self.distributed_items[current_demand]['quantity'] += 1
            self.available_items[current_demand] -= 1
            self.distributed_items[current_demand]['history'].append(f"{item_to_distribute} kiosztva {clan_mate.name} klántagnak {clan_mate.glory} glorynál.")

        clan_mate.give_item(item_to_distribute)

        return item_to_distribute


    def print_distribution_history(self):
        print('--- Jutalmak Tárgy Szerint ---')

        index = 0
        for item in self.available_items:
            if self.distributed_items.get(item):
                for history in self.distributed_items[item]['history']:
                    index += 1
                    print(f'{index}. {history}')

        print()


    def _init_distributed_items(self):
        self.distributed_items = {}

        for available_item in self.available_items:
            self.distributed_items[available_item] = { 'quantity': 0, 'max': self.available_items[available_item], 'history': [] }


    def _get_current_demand(self, demands):
        for demand in demands:
            if demand['quantity'] > 0:
                for demanded_item in demand['items']:
                    if demanded_item in self.available_items and self.available_items[demanded_item] > 0:
                        return demanded_item


    def _get_item_to_distribute(self, demand):
        if demand in self.available_items and self.available_items[demand] > 0:
            return f"{demand} ({self.distributed_items[demand]['quantity'] + 1}/{self.distributed_items[demand]['max']})"

        return None
