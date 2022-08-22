class ClanMate:
    def __init__(self, clan_mate_data, item_price):
        self.name = clan_mate_data['name']
        self.glory = clan_mate_data['glory']
        self.demands = clan_mate_data['demands']
        self.rewards = []
        self._item_price = item_price

        for demand in self.demands:
            demand['original'] = demand['quantity']


    def give_item(self, demanded_item, item_to_give):
        self.rewards.append(item_to_give)
        self.glory -= self._item_price

        for demand in self.demands:
            if demanded_item in demand['items']:
                # Reduce the demanded quantity
                demand['quantity'] -= 1


    def print_demands(self):
        demands = 'Kérés: '
        for demand in self.demands:
            demands += f"{demand['items']} ({demand['original']})"
            demands += "; "

        print(demands)


    def print_rewards(self):
        rewards = 'Jutalom: '
        for reward in self.rewards:
            if reward is not None:
                rewards += reward
            else:
                rewards += 'None'

            rewards += "; "

        print(rewards)
