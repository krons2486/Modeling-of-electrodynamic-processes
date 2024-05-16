import json

class ResultWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_to_json(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
