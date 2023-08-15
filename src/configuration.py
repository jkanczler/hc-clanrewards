import data


class Configuration:
    def __init__(self, data_dir) -> None:
        self._configuration = data.get_configuration(data_dir)


    def get_item_price(self):
        return self._configuration('item_price')


    def get_number_of_rewards(self):
        return self._configuration('number_of_rewards')
