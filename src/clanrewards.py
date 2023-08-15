import data


class ClanRewards:
    def __init__(self, data_dir):
        self.available_items = data.get_items(data_dir)
        self._item_price = data.get_item_price()
        self._init_distributed_items()


    def distribute_item(self, clan_mate):
        current_demand = self._get_current_demand(clan_mate.demands)
        item_to_distribute = self._get_item_to_distribute(current_demand)

        # if we can distribute an item, properly register quantities and history:
        if not item_to_distribute is None:
            self._update_store(clan_mate, current_demand, item_to_distribute)

        clan_mate.give_item(item_to_distribute)

        return item_to_distribute


    def print_distribution_history(self):
        distriubtion_history = '--- Jutalmak Tárgy Szerint ---\n'

        index = 0
        for item in self.available_items:
            if self.distributed_items.get(item):
                for history in self.distributed_items[item]['history']:
                    index += 1
                    distriubtion_history += f'{index}. {history}\n'

        distriubtion_history += '\n'

        return distriubtion_history


    def _update_store(self, clan_mate, current_demand, item_to_distribute):
        self.distributed_items[current_demand]['quantity'] += 1
        self.available_items[current_demand] -= 1
        self.distributed_items[current_demand]['history'].append(f"{item_to_distribute} kiosztva {clan_mate.name} klántagnak {clan_mate.glory} glorynál.")


    def _init_distributed_items(self):
        self.distributed_items = {}

        for item_name, item_count in self.available_items.items():
            self.distributed_items[item_name] = { 'quantity': 0, 'max': item_count, 'history': [] }


    def _get_current_demand(self, demands):
        for demand in demands:
            if demand['quantity'] > 0:
                for demanded_item in demand['items']:
                    if demanded_item in self.available_items and self.available_items[demanded_item] > 0:
                        return demanded_item

        return None


    def _get_item_to_distribute(self, demand):
        if demand in self.available_items and self.available_items[demand] > 0:
            return f"{demand} ({self.distributed_items[demand]['quantity'] + 1}/{self.distributed_items[demand]['max']})"

        return None
