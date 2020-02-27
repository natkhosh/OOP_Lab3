# Наблюдатель

from weakref import ref


class Observer:
    def update(self):
        pass


class WeakSubject:
    def __init__(self):
        self.__o = set()

    def add_observer(self, o: Observer):
        self.__o.add(ref(o))

    def remove_observer(self, o: Observer):
        self.__o.remove(ref(o))

    def notify(self):
        for o in self.__o:
            o.update(ref(o))


class Data(WeakSubject):
    def __init__(self, data):
        super().__init__()  # нужно ли вызывать super?
        self._data = data  # подумать как сделать так, чтобы при первой записи тоже уведомлялся observer

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if self._data != data:
            self._data = data
            self.notify()



