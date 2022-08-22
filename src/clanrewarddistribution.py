import data
from clanmate import ClanMate

class ClanRewardsDistributor:
    # Tracking the items distributed to clan mates
    _items_distributed = {}

    # Price of any items, this will be deducated from the glory after each item received
    _item_price = 50000

    # Each clan mate can receive this many rewards
    _number_of_rewards = 5

    _available_items = data.get_items()


    def __init__(self):
        self._init_clan_mates()


    def distribute_clan_rewards(self):
        successful_validation = self._validate_items()

        if successful_validation:
            self._distribute_clan_rewards()


    def _distribute_clan_rewards(self):
        print('--- Jutalmak ---')

        # Distribute the rewards until there's an available awardee
        next_clan_mate = self._get_next_clan_mate()
        while next_clan_mate is not None:
            self._try_distributing_item(next_clan_mate)

            next_clan_mate = self._get_next_clan_mate()

        self._write_result_to_output()


    # Gets the next clan mate who can receive a reward
    def _get_next_clan_mate(self):
        self._clan_mates.sort(key=lambda cm: cm.glory, reverse=True)

        for clan_mate in self._clan_mates:
            if len(clan_mate.received) < self._number_of_rewards:
                return clan_mate

        return None


    # Gets the next reward available based on the demands
    def _get_item_to_distribute(self, demands):
        for demand in demands:
            if demand['quantity'] > 0:
                for demanded_item in demand['items']:
                    for available_item in self._available_items:
                        if demanded_item == available_item and self._available_items[demanded_item] > 0:
                            return available_item

        return None


    # Distributes the next available item to a clan mate
    def _try_distributing_item(self, clan_mate):
        # Gets the next item to distributed
        item_to_distribute = self._get_item_to_distribute(clan_mate.demands)

        received = ''
        if item_to_distribute is not None:
            received = self._distribute_item(clan_mate, item_to_distribute)
        else:
            # if there's none to distribute, just record the fact that none is received as reward
            received = item_to_distribute

        self._sell_item_to_clan_mate(clan_mate, item_to_distribute, received)

    def _distribute_item(self, clan_mate, item_to_distribute):
        # if we can distribute an item, properly register quantities and history:

        # handle the distributed items records:
        if self._items_distributed.get(item_to_distribute):
            # If one piece of this item already distributed, then increase the received quantity
            self._items_distributed[item_to_distribute]['quantity'] += 1
        else:
            # First time distributing this item initialize the quantity and maximum available quantity
            self._items_distributed[item_to_distribute] = { 'quantity': 1, 'max': self._available_items[item_to_distribute], 'history': [] }

        # deduct the count of availability
        self._available_items[item_to_distribute] -= 1

        # record history
        received = f"{item_to_distribute} ({self._items_distributed[item_to_distribute]['quantity']}/{self._items_distributed[item_to_distribute]['max']})"
        self._items_distributed[item_to_distribute]['history'].append(f"{received} kiosztva {clan_mate.name} klántagnak {clan_mate.glory + self._item_price} glorynál.")

        return received


    def _sell_item_to_clan_mate(self, clan_mate, item_to_distribute, received):
        # Update clan mate info
        clan_mate.received.append(received)
        clan_mate.glory -= self._item_price

        for demand in clan_mate.demands:
            if item_to_distribute in demand['items']:
                # Reduce the demanded quantity
                demand['quantity'] -= 1

        print(f"{clan_mate.name} megkapja a következő tárgyat: '{received}'. Glory levonás: {clan_mate.glory + self._item_price} - {self._item_price} = {clan_mate.glory}")


    def _write_result_to_output(self):
        print()
        print('--- Jutalmak Ember Szerint ---')

        for clan_mate in self._clan_mates:
            print()
            print(f"{clan_mate.name} kérései és jutalma:")

            demands = 'Kérés: '
            for demand in clan_mate.demands:
                demands += f"{demand['items']} ({demand['original']})"
                demands += "; "

            print(demands)

            received = 'Jutalom: '
            for received_item in clan_mate.received:
                if received_item is not None:
                    received += received_item
                else:
                    received += 'None'

                received += "; "

            print(received)

        print()
        print('--- Jutalmak Tárgy Szerint ---')
        index = 0
        for item in self._available_items:
            if self._items_distributed.get(item):
                for history in self._items_distributed[item]['history']:
                    index += 1
                    print(f'{index}. {history}')


    def _validate_items(self):
        print('--- Tárgy Lista Validáció ---')

        success = True
        for clan_mate in self._clan_mates:
            for demand in clan_mate.demands:
                for item in demand['items']:
                    if not self._available_items.get(item):
                        print(f"A '{item}' kérés nincs a listában.")
                        success = False

        if not success:
            print('Tárgy Lista Validáció Sikertelen: javítsd ki a tárgy listát...')
            print()
        else:
            print('Tárgy Lista Validáció Sikeres')
            print()

        return success


    def _init_clan_mates(self):
        self._clan_mates = []
        clan_mate_init_objs = data.get_clan_mates()

        for init_obj in clan_mate_init_objs:
            self._clan_mates.append(ClanMate(init_obj))
