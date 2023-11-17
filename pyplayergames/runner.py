import yaml

class Match:

    def __init__(self, config_filepath: str|None = None):



    def load_config(self, config_filepath: str):
        with open(config_filepath, mode='wb') as file:
            self.config = yaml.load(file, Loader=yaml.SafeLoader)
        pass

    def save_config(self, config_filepath: str):
        pass


class Tournament:
    pass


if __name__ == '__main__':
    pass
