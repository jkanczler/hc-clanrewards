import json


def get_clan_mates(data_dir):
    return _open_file(f'{data_dir}/clan_mates.json')['clan_mates']


def get_items(data_dir):
    return _open_file(f'{data_dir}/items.json')


def get_configuration(data_dir):
    return _open_file(f'{data_dir}/config.json')


def _open_file(file_name):
    print(__file__)

    with open(f'./{file_name}', 'r+', encoding='utf-8') as file:
        return json.load(file)
