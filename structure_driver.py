# Шаблон проектирования "Стратегия"

import json
import pickle


class IStructureDriver:
    def read(self):
        pass

    def write(self, d):
        pass


class JSONFileDriver(IStructureDriver):
    def __init__(self, filename):
        self.__filename = filename

    def read(self):
        with open(self.__filename, encoding='UTF-8') as f:
            return json.load(f)

    def write(self, d):
        with open(self.__filename, 'w', encoding='UTF-8') as f:
            json.dump(d, f, ensure_ascii=False)


class JSONStringDriver(IStructureDriver):
    def __init__(self, s='{}'):
        self.__s = s

    def get_string(self):
        return self.__s

    def read(self):
        return json.loads(self.__s)

    def write(self, d):
        self.__s = json.dumps(d, ensure_ascii=False)


class PickleDriver(IStructureDriver):
    def __init__(self, filename):
        self.__filename = filename

    def read(self):
        with open(self.__filename, 'rb') as f:
            return pickle.load(f)

    def write(self, d):
        with open(self.__filename, 'wb') as f:
            pickle.dump(d, f)


class SDWorker:
    def __init__(self, structure_driver: IStructureDriver):
        self.__structure_driver = structure_driver

    def load(self):
        return self.__structure_driver.read()

    def save(self, d):
        self.__structure_driver.write(d)

    def set_structure_driver(self, driver):
        self.__structure_driver = driver


