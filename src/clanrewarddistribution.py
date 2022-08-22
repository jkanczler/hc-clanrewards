import data


class ClanRewardsDistributor:
    # Tracking the items distributed to clan mates
    _items_distributed = {}

    # Price of any items, this will be deducated from the glory after each item received
    _item_price = 50000

    # Each clan mate can receive this many rewards
    _number_of_rewards = 5

    _clan_mates = data.get_clan_mates()
    _available_items = data.get_items()


    def distribute_clan_rewards(self):
        print('--- Tárgy Lista Validáció ---')
        validation_result = self._validate_items()

        self._set_original_quantities()

        if not validation_result:
            print('Tárgy Lista Validáció Sikertelen: javítsd ki a tárgy listát...')
        else:
            print('Tárgy Lista Validáció Sikeres')
            print()
            print('--- Jutalmak ---')

            # Distribute the rewards until there's an available awardee
            next_clan_mate = self._get_next_clan_mate()
            while next_clan_mate is not None:
                self._distribute_item(next_clan_mate)

                next_clan_mate = self._get_next_clan_mate()

            self._write_result_to_output()


    # Gets the next clan mate who can receive a reward
    def _get_next_clan_mate(self):
        self._clan_mates.sort(key=lambda cm: cm['glory'], reverse=True)

        for clan_mate in self._clan_mates:
            if not 'received' in clan_mate:
                clan_mate['received'] = []
                clan_mate['received_display'] = []

            if len(clan_mate['received']) < self._number_of_rewards:
                return clan_mate

        return None


    # Gets the next reward available based on the demands
    def _get_item_to_distribute(self, demands):
        for demand in demands:
            if demand['quantity'] > 0:
                for item in self._available_items:
                    if demand['name'] == item:
                        if self._available_items[demand['name']] > 0:
                            return item

        return None


    # Distributes the next available item to a clan mate
    def _distribute_item(self, clan_mate):
        # Gets the next item to distributed
        item_to_distribute = self._get_item_to_distribute(clan_mate['demands'])

        received = ''
        if item_to_distribute is not None:
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
            self._items_distributed[item_to_distribute]['history'].append(f"{received} kiosztva {clan_mate['name']} klántagnak {clan_mate['glory'] + self._item_price} glorynál.")
        else:
            # if there's none to distribute, just record the fact that none is received as reward
            received = item_to_distribute

        # Update clan mate info
        clan_mate['received'].append(received)
        clan_mate['glory'] -= self._item_price

        for demand in clan_mate['demands']:
            if demand['name'] == item_to_distribute:
                # Reduce the demanded quantity
                demand['quantity'] -= 1

        print(f"{clan_mate['name']} megkapja a következő tárgyat: '{received}'. Glory levonás: {clan_mate['glory'] + self._item_price} - {self._item_price} = {clan_mate['glory']}")


    def _write_result_to_output(self):
        print()
        print('--- Jutalmak Ember Szerint ---')

        for clan_mate in self._clan_mates:
            print()
            print(f"{clan_mate['name']} kérései és jutalma:")

            demands = 'Kérés: '
            for demand in clan_mate['demands']:
                demands += f"{demand['name']} ({demand['original']})"
                demands += "; "

            print(demands)

            received = 'Jutalom: '
            for received_item in clan_mate['received']:
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
        success = True
        for clan_mate in self._clan_mates:
            for demand in clan_mate['demands']:
                if not self._available_items.get(demand['name']):
                    print(f"A '{demand}' kérés nincs a listában.")
                    success = False

        return success


    def _set_original_quantities(self):
        for clan_mate in self._clan_mates:
            for demand in clan_mate['demands']:
                demand['original'] = demand['quantity']
