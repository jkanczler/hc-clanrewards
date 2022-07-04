import sys
from data.clanmates import clan_mates
from data.items import items

items_sold = {}
ITEM_PRICE = 50000

def sort_clan_mates():
    clan_mates.sort(key=lambda cm: cm['glory'], reverse=True)

def get_next_clan_mate():
    sort_clan_mates()

    for clan_mate in clan_mates:
        if len(clan_mate['received']) < 5:
            return clan_mate

    return None

def get_item_to_receive(demands):
    for demand in demands:
        if demand['quantity'] > 0:
            for item in items:
                if demand['name'] == item:
                    if items[demand['name']] > 0:
                        return item

    return None

def receive_item(clan_mate, item_to_receive):
    if item_to_receive is not None:
        if items_sold.get(item_to_receive):
            items_sold[item_to_receive]['quantity'] += 1
        else:
            items_sold[item_to_receive] = { 'quantity': 1, 'max': items[item_to_receive] }

        items[item_to_receive] -= 1

    received_display = ''

    if item_to_receive is not None:
        received_display = f"{item_to_receive} ({items_sold[item_to_receive]['quantity']}/{items_sold[item_to_receive]['max']})"
    else:
        received_display = item_to_receive

    clan_mate['received'].append(item_to_receive)
    clan_mate['received_display'].append(received_display)
    clan_mate['glory'] -= ITEM_PRICE

    for demand in clan_mate['demands']:
        if demand['name'] == item_to_receive:
            demand['quantity'] -= 1

    print(f"{clan_mate['name']} is receiving '{received_display}'.")
    print(f"{clan_mate['glory'] + ITEM_PRICE} - {ITEM_PRICE} = {clan_mate['glory']}")

def validate_items():
    for clan_mate in clan_mates:
        for demand in clan_mate['demands']:
            if not items.get(demand['name']):
                print(f"The demand '{demand}' is not in the item list.")

def main() -> int:
    validate_items()

    next_clan_mate = get_next_clan_mate()
    while next_clan_mate is not None:
        item_to_receive = get_item_to_receive(next_clan_mate['demands'])
        receive_item(next_clan_mate, item_to_receive)

        next_clan_mate = get_next_clan_mate()

    for clan_mate in clan_mates:
        print(clan_mate['name'])

        demands = 'demands: '
        for demand in clan_mate['demands']:
            demands += demand['name']
            demands += "; "

        print(demands)

        received = 'received: '
        for received_item in clan_mate['received_display']:
            if received_item is not None:
                received += received_item
            else:
                received += 'None'

            received += "; "

        print(received)

    for item in items:
        for clan_mate in clan_mates:
            for received_item in clan_mate['received_display']:
                if received_item is not None:
                    if received_item.startswith(item.strip()):
                        print(f"{received_item} bought by {clan_mate['name']}")
                else:
                    print(f"None bought by {clan_mate['name']}")

if __name__ == '__main__':
    sys.exit(main())
