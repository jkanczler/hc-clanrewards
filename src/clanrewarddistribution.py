import data
from clanmate import ClanMate
from clanrewards import ClanRewards


class ClanRewardsDistributor:
    # Each clan mate can receive this many rewards
    _number_of_rewards = 5


    def __init__(self):
        self._init_item_price()
        self._init_clan_mates()
        self._init_clan_rewards()


    def distribute_clan_rewards(self):
        successful_validation = self._validate_items()

        if not successful_validation:
            return

        self._distribute_clan_rewards()
        self._print_results()


    def _init_item_price(self):
        self._item_price = data.get_item_price()


    def _init_clan_mates(self):
        self._clan_mates = []
        clan_mate_data_list = data.get_clan_mates()

        for clan_mate_data in clan_mate_data_list:
            self._clan_mates.append(ClanMate(clan_mate_data, self._item_price))


    def _init_clan_rewards(self):
        _available_items = data.get_items()
        self.clan_rewards = ClanRewards(_available_items, self._item_price)


    def _distribute_clan_rewards(self):
        print()
        print('Jutalmak kiosztása...')

        # Distribute the rewards until there's an available awardee
        next_clan_mate = self._get_next_clan_mate()
        while next_clan_mate is not None:
            item_received = self.clan_rewards.distribute_item(next_clan_mate)
            print(f"{next_clan_mate.name} megkapja a következő tárgyat: '{item_received}'. Glory levonás: {next_clan_mate.glory + self._item_price} - {self._item_price} = {next_clan_mate.glory}")

            next_clan_mate = self._get_next_clan_mate()

        print()


    # Gets the next clan mate who can receive a reward
    def _get_next_clan_mate(self):
        self._clan_mates.sort(key=lambda cm: cm.glory, reverse=True)

        for clan_mate in self._clan_mates:
            if len(clan_mate.rewards) < self._number_of_rewards:
                return clan_mate

        return None


    def _print_results(self):
        print('--- Jutalmak Ember Szerint ---')

        for clan_mate in self._clan_mates:
            print(f"{clan_mate.name} kérései és jutalma:")

            clan_mate.print_demands()
            clan_mate.print_rewards()

            print()

        print()
        self.clan_rewards.print_distribution_history()


    def _validate_items(self):
        success = True
        for clan_mate in self._clan_mates:
            for demand in clan_mate.demands:
                for item in demand['items']:
                    if not self.clan_rewards.available_items.get(item):
                        print(f"A '{item}' kérés nincs a listában.")
                        success = False

        if not success:
            print('Tárgy Lista Validáció Sikertelen: javítsd ki a tárgy listát...')
        else:
            print('Tárgy Lista Validáció Sikeres')

        return success
