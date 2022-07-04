from data.current.clanmates import clan_mates
from data.current.items import items as items_available

# Tracking the items distributed to clan mates
_items_distributed = {}

# Price of any items, this will be deducated from the glory after each item received
_ITEM_PRICE = 50000

# Each clan mate can receive this many rewards
_NUMBER_OF_REWARDS = 5

# Gets the next clan mate who can receive a reward
def _get_next_clan_mate():
    clan_mates.sort(key=lambda cm: cm['glory'], reverse=True)

    for clan_mate in clan_mates:
        if len(clan_mate['received']) < _NUMBER_OF_REWARDS:
            return clan_mate

    return None

# Gets the next reward available based on the demands
def _get_item_to_distribute(demands):
    for demand in demands:
        if demand['quantity'] > 0:
            for item in items_available:
                if demand['name'] == item:
                    if items_available[demand['name']] > 0:
                        return item

    return None

# Distributes the next available item to a clan mate
def _distribute_item(clan_mate):
    # Gets the next item to distributed
    item_to_distribute = _get_item_to_distribute(clan_mate['demands'])

    received = ''
    if item_to_distribute is not None:
        # if we can distribute an item, properly register quantities and history:

        # handle the distributed items records:
        if _items_distributed.get(item_to_distribute):
            # If one piece of this item already distributed, then increase the received quantity
            _items_distributed[item_to_distribute]['quantity'] += 1
        else:
            # First time distributing this item initialize the quantity and maximum available quantity
            _items_distributed[item_to_distribute] = { 'quantity': 1, 'max': items_available[item_to_distribute], 'history': [] }

        # deduct the count of availability
        items_available[item_to_distribute] -= 1

        # record history
        received = f"{item_to_distribute} ({_items_distributed[item_to_distribute]['quantity']}/{_items_distributed[item_to_distribute]['max']})"
        _items_distributed[item_to_distribute]['history'].append(f"{received} distributed to {clan_mate['name']} at glory {clan_mate['glory'] + _ITEM_PRICE}")
    else:
        # if there's none to distribute, just record the fact that none is received as reward
        received = item_to_distribute

    # Update clan mate info
    clan_mate['received'].append(received)
    clan_mate['glory'] -= _ITEM_PRICE

    for demand in clan_mate['demands']:
        if demand['name'] == item_to_distribute:
            # Reduce the demanded quantity
            demand['quantity'] -= 1

    print(f"{clan_mate['name']} is receiving '{received}'.")
    print(f"{clan_mate['glory'] + _ITEM_PRICE} - {_ITEM_PRICE} = {clan_mate['glory']}")

def _write_result_to_output():
    print()
    print('--- Rewards by Clan Mates ---')

    for clan_mate in clan_mates:
        print()
        print(f"{clan_mate['name']} demands and rewards:")

        demands = 'Demands: '
        for demand in clan_mate['demands']:
            demands += demand['name']
            demands += "; "

        print(demands)

        received = 'Rewards: '
        for received_item in clan_mate['received']:
            if received_item is not None:
                received += received_item
            else:
                received += 'None'

            received += "; "

        print(received)

    print()
    print('--- Items Distributed ---')
    index = 0
    for item in items_available:
        if _items_distributed.get(item):
            for history in _items_distributed[item]['history']:
                index += 1
                print(f'{index}. {history}')

def _validate_items():
    success = True
    for clan_mate in clan_mates:
        for demand in clan_mate['demands']:
            if not items_available.get(demand['name']):
                print(f"The demand '{demand}' is not in the item list.")
                success = False

    return success

def distribute_clan_rewards():
    print('--- Item List Validation ---')
    validation_result = _validate_items()

    if not validation_result:
        print('Item List Validation failed: please add the missing items to continue...')
    else:
        print('Item List Validation was successful')
        print()
        print('--- Distributing Rewards ---')

        # Distribute the rewards until there's an available awardee
        next_clan_mate = _get_next_clan_mate()
        while next_clan_mate is not None:
            _distribute_item(next_clan_mate)

            next_clan_mate = _get_next_clan_mate()

        _write_result_to_output()
