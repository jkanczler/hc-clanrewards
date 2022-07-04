import sys
import json
from data.clanmates import clan_mates
from data.items import items

def sort_clan_mates():
    clan_mates.sort(key=lambda cm: cm['glory'], reverse=True)

def get_next_buyer():
    sort_clan_mates()

    for clan_mate in clan_mates:
        if len(clan_mate['purchased']) < 5:
            return clan_mate

    return None

def get_item_to_buy(demands):
    for demand in demands:
        if demand['quantity'] > 0:
            for item in items:
                if demand['name'] == item:
                    if items[demand['name']] > 0:
                        return item

    return None

def buy_item(buyer, item_to_buy):
    print(f"{buyer['name']} is buying '{item_to_buy}'.")
    print(f"{buyer['glory']} - 50000 = {buyer['glory'] - 50000}")

    if item_to_buy is not None:
        items[item_to_buy] -= 1

    buyer['purchased'].append(item_to_buy)
    buyer['glory'] -= 50000

    for demand in buyer['demands']:
        if demand['name'] == item_to_buy:
            demand['quantity'] -= 1

def validate_items():
    for clan_mate in clan_mates:
        for demand in clan_mate['demands']:
            if not items.get(demand['name']):
                print(f"The demand '{demand}' is not in the item list.")

def main() -> int:
    validate_items()

    orders = []

    next_buyer = get_next_buyer()
    while next_buyer is not None:
        item_to_buy = get_item_to_buy(next_buyer['demands'])
        buy_item(next_buyer, item_to_buy)

        orders.append(
            {
                'name': next_buyer['name'],
                'purchased': item_to_buy
            })

        print(f"remaining gloriy is {next_buyer['glory']}")

        next_buyer = get_next_buyer()

    for clan_mate in clan_mates:
        print(clan_mate['name'])
        
        demands = 'demands: '
        for demand in clan_mate['demands']:
            demands += demand['name']
            demands += "; "

        print(demands)

        purchased = 'purchased: '
        for purchase in clan_mate['purchased']:
            purchased += purchase
            purchased += "; "

        print(purchased)

    for item in items:
        for clan_mate in clan_mates:
            for purchase in clan_mate['purchased']:
                if purchase == item:
                    print(f"{item} bought by {clan_mate['name']}")

if __name__ == '__main__':
    sys.exit(main())
