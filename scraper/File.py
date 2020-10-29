import json
import os


class File:
    @staticmethod
    def read(location, toJson=False):
        with open(location) as f:
            data = f.read()

        return json.loads(data) if toJson else data

    @staticmethod
    def write(data, location):
        if type(data) != str:
            data = json.dumps(data)

        with open(location, 'w') as f:
            f.write(data)

    @staticmethod
    def mkdir(name):
        os.mkdir(name)
