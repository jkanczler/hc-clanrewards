import json


def get_clan_mates(data_path):
    return _open_file(f'{data_path}/clan_mates.json')['clan_mates']


def get_items(data_path):
    return _open_file(f'{data_path}/items.json')


def get_item_price():
    return 50000


def _open_file(file_name):
    print(__file__)

    with open(f'./{file_name}', 'r+', encoding='utf-8') as file:
        return json.load(file)
