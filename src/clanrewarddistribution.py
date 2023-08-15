from datetime import date
import os
import data
from clanmate import ClanMate
from clanrewards import ClanRewards


# Only one public method as this is the entry point to the application.
# pylint: disable=too-few-public-methods
class ClanRewardsDistributor:
    # Each clan mate can receive this many rewards
    _number_of_rewards = 5


    def __init__(self, data_dir, reward_dir):
        self._data_dir = data_dir
        self._reward_dir = reward_dir

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
        clan_mate_data_list = data.get_clan_mates(self._data_dir)

        for clan_mate_data in clan_mate_data_list:
            print(clan_mate_data)
            self._clan_mates.append(ClanMate(clan_mate_data))


    def _init_clan_rewards(self):
        self.clan_rewards = ClanRewards(self._data_dir)


    def _distribute_clan_rewards(self):
        print()
        print('Jutalmak kiosztása...')

        # Distribute the rewards until there's an available awardee
        next_clan_mate = self._get_next_clan_mate()
        while next_clan_mate is not None:
            item_received = self.clan_rewards.distribute_item(next_clan_mate)

            reward_log = f"{next_clan_mate.name} megkapja a következő tárgyat: '{item_received}'."
            glory_log = f"Glory levonás: {next_clan_mate.glory + self._item_price} - {self._item_price} = {next_clan_mate.glory}"
            print(f"{reward_log} {glory_log}")

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
        result = ''
        result += '--- Jutalmak Ember Szerint ---\n'

        for clan_mate in self._clan_mates:
            result += f"{clan_mate.name} kérése és jutalma:\n"

            result += clan_mate.print_demands()
            result += clan_mate.print_rewards()

            result += '\n'

        result += '\n'
        result += self.clan_rewards.print_distribution_history()

        print(result)
        self._save_results_to_file(result)


    def _save_results_to_file(self, result):
        if not os.path.exists(self._reward_dir):
            os.makedirs(self._reward_dir)

        with open(f'{self._reward_dir}/rewards_{date.today()}.txt', 'w', encoding='utf-8') as output:
            output.write(result)


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
