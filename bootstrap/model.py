import os.path
import json

class Model:

    def __init__(self):
        self.__names__ = []
        self.subscribers = {}

    def subscribe(self, attr: str, receiver): # receiver := lambda (model, attr_name, value)
        attr_subscribers = self.subscribers.get(attr, [])
        attr_subscribers.append(receiver)
        self.subscribers[attr] = attr_subscribers

    def __getitem__(self, attr):
        return getattr(self, attr)

    def register(self, attr: str, value):
        if not hasattr(self, attr):
            self.__names__.append(attr)
        setattr(self, attr, value)

    def update(self, attr: str, value):
        self.register(attr, value)
        for subscriber in self.subscribers.get(attr, []):
            subscriber(self, attr, value)

    def mocktify(self, attr):
        value = self[attr]
        for subscriber in self.subscribers.get(attr, []):
            subscriber(self, attr, value)

    def has(self, attr):
        return hasattr(self, attr)

    def has_value(self, attr):
        return self.has(attr) and self[attr] is not None

    #TODO: 'delete' operation things ...

class JsonConfigModel(Model):

    @classmethod
    def from_file(cls, path: str):
        model = JsonConfigModel(cls.read_json(path))
        return model
    
    @classmethod
    def read_json(self, path: str):
        if os.path.isfile(path):
            with open(path, 'r') as json_file:
                json_content = json.load(json_file)
        else:
            raise RuntimeError(path + '는 읽을 수 없는 파일입니다.')
        return json_content

    def __init__(self, json = None):
        super().__init__()
        if json is not None:
            self.register_from_json(json)

    def register_from_json(self, json):
        for attr, value in json.items():
            self.register(attr, value)

    def jsonify(self):
        return {name:self[name] for name in self.__names__}

    def dumps(self):
        tmp = self.jsonify()
        return json.dumps(tmp)

    def dump(self, json_file_path: str):
        with open(json_file_path, 'w') as json_file:
            return json.dump(self.jsonify(), json_file)
            

    