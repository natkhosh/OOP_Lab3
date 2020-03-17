from weakref import ref

from structure_driver import *
# IStructureDriver, JSONFileDriver
from react import *
# Observer, Data


class Node(Data):

    def __init__(self, prev_node=None, next_node=None, data=None):
        """
           Конструктор узла
           :param prev_node: int or str
           :param next_node: type(self)
           :param data: type(self)
           """
        super().__init__(data)

        if prev_node is not None and not isinstance(prev_node, type(self)):
            raise TypeError('prev_node must be Node or None')

        if next_node is not None and not isinstance(next_node, type(self)):
            raise TypeError('next_node must be Node or None')

        self.prev_node = ref(prev_node) if prev_node is not None else None
        self.next_node = next_node
        # self.data = data

    def __str__(self):
        return self.data


class LinkedList(Observer):
    def __init__(self, structure_driver=None):
        """
        Конструктор циклического двунаправленного списка
        :param head: type(self)
        :param tail: type(self)
        :param size: int
        """
        self.size = 0
        self.head = None
        self.tail = None

        self.__structure_driver = structure_driver

    def __str__(self):
        """
        Методы для получения строкового представления двунаправленного списка
        :return: str
        """
        if self.head is not None:
            current_node = self.head
        else:
            current_node = Node()
        s = ''
        i = 0
        while i < self.size:
            s += f'{current_node.data}->'
            current_node = current_node.next_node
            i += 1
        return s

    def __len__(self):
        """
        Метод, позволяющий посмотреть длину списка.
         Используется для вывода на экран
        :return: int
        """
        return self.size

    def append(self, data):
        """
        Добавление нового узла в конец списка
        :param data: узел - int, str
        """
        if not isinstance(data, (int, str)):
            raise TypeError

        if self.head is None:
            self.head = Node(None, None, data)
            self.tail = Node(self.head, self.head, data)
            self.head.next_node = self.tail
            self.tail.prev_node = ref(self.head)
        else:
            new_node = self.tail
            self.tail = Node(new_node, self.head, data)
            new_node.data = data
            new_node.next_node = self.tail
            self.head.prev_node = ref(self.tail)
        self.size += 1
        self.update()

    def insert(self, node, index=0):
        """
        Вставка узла по индексу
        :param node: узел - int, str
        :param index: индекс - int
        :return:
        """
        if not isinstance(index, int):
            raise TypeError
        if not isinstance(node, (int, str)):
            raise TypeError

        if self.head is None:
            new_node = Node(None, None, None)
            new_node.next_node = new_node.prev_node = new_node
            self.head = new_node
            self.tail = self.head.prev_node

        if index == 0:
            # self.tail = self.head.prev_node
            new_node = Node(None, None, node)
            new_node.data = node  # Inserting the data
            new_node.next_node = self.head
            new_node.prev_node = self.tail
            self.tail.next_node = self.head.prev_node = new_node
            self.head = new_node
            self.size += 1
        elif index > self.size - 1:
            self.append(node)
        else:
            current_node = self.head
            next = current_node.next_node
            i = 0
            while i < self.size - 1:
                if i + 1 == index:
                    current_node.next_node = None
                    next.prev_node = None
                    new_node = Node(current_node, next, node)
                    current_node.next_node = new_node
                    next.prev_node = ref(new_node)

                current_node = current_node.next_node
                next = current_node.next_node
                i += 1

            # self.insert(node, index)
            current_node.add_observer(self)
            self.size += 1
        self.update()

    def clear(self):
        '''
        Очистка списка
        '''
        self.size = 0
        self.head = None
        self.tail = None
        self.update()

    def find(self, node):
        """
        Поиск узла по узлу
        :param node: узел - int, str
        :return: список - list, если элемент не найден - None
        """
        if not isinstance(node, (int, str)):
            raise TypeError

        current_node = self.head
        list_i = []
        i = 0
        while i <= self.size - 1:
            if current_node.data == node:
                list_i.append(i)
            i += 1
            current_node = current_node.next_node

        if len(list_i) == 1:
            return list_i[0]
        elif len(list_i) > 1:

            return list_i
        else:
            print("Элемент не найден")
            return None

    def remove(self, node):
        """
        Удаление узла по значению узла
        :param node: узел - int, str
        :return:
        """
        if not isinstance(node, (int, str)):
            raise TypeError

        if self.head is None:
            print("Список пустой")
            return

        i = 0
        while i <= self.size:
            if (i == 0) and (self.head.data == node):
                if self.size > 1:
                    current_node = self.head
                    self.head = current_node.next_node
                    current_node.next_node = None
                    current_node.prev_node = None
                    self.head.prev_node = ref(self.tail)
                    self.tail.next_node = self.head
                    self.size -= 1
                    break
                else:
                    self.clear()
                    break

            elif (i == self.size) and (self.tail.data == node):
                current_node = self.tail
                self.tail = current_node.prev_node
                current_node.prev_node = None
                current_node.next_node = None
                self.tail.next_node = self.head
                self.head.prev_node = ref(self.tail)
                self.size -= 1
                return

            else:
                current_node = self.head.next_node
                pred_node = self.head
                sled_node = current_node.next_node
                i = 1
                while i <= self.size:
                    if current_node.data == node:
                        pred_node.next_node = sled_node
                        sled_node.prev_node = ref(pred_node)
                        current_node.prev_node = None
                        current_node.next_node = None
                        current_node = sled_node
                        self.size -= 1
                    elif i == self.size:
                        print("Нет такого индекса")
                    else:
                        current_node = current_node.next_node
                        pred_node = pred_node.next_node
                        sled_node = sled_node.next_node
                    i += 1
            i += 1
        self.update()

    def delete(self, index):
        """
        Удаление узла по индексу
        :param index: индекс - int
        :return:
        """
        if not isinstance(index, int):
            raise TypeError
        if 0 <= index < self.size:
            i = 0
            current_node = self.head
            while i < self.size:
                if i == index:
                    self.remove(current_node.data)
                    break
                current_node = current_node.next_node
                i += 1
        else:
            print("Нет такого индекса")

    def to_dict(self):
        """
        Преобразование двунаправленного списка в словарь
        :return: словарь - dict
        """
        d = {}
        i = 0
        current_node = self.head
        while i < self.size:
            d[i] = current_node.data
            i += 1
            current_node = current_node.next_node
        return d

    def from_dict(self, d={0: 12, 1: 30, 2: 1, 3: 3}):
        """
        Преобразование из словаря
        :param d: словарь - dict
        :return:
        """
        for index, value in d.items():
            self.insert(value, index)
        print(self.to_dict())

    def load(self):
        if self.__structure_driver is None:
            raise ValueError
        self.from_dict(self.__structure_driver.read())

    def save(self):
        if self.__structure_driver is None:
            raise ValueError
        self.__structure_driver.write(self.to_dict())

    def set_structure_driver(self, driver):
        if not isinstance(driver, IStructureDriver):
            raise TypeError()
        self.__structure_driver = driver

    def update(self):
        print("Данные после изменения > ", flush=True)
        print(self.__str__(), self.__len__())
        self.save()


if __name__ == "__main__":

    l1 = LinkedList(JSONFileDriver("test_11.txt"))

    # print(' *** Insert -->')
    # l1.insert(12, 0)
    # print('*** Insert -->')
    # l1.insert(30, 0)

    print('*** Append -->')
    l1.append(1)
    l1.append(1)
    # print(l1, len(l1))
    print(l1.find(1))

    # l1.append(3)
    # # print(l1, len(l1))
    # l1.append(5)
    # # print(l1, len(l1))
    # l1.append(1)
    # # print(l1, len(l1))
    #
    # print('*** Insert -->')
    # l1.insert(7, 0)
    # # print(l1, len(l1))
    #
    #
    # print('*** Delete -->')
    # l1.delete(3)
    #
    # print('*** Remove -->')
    # l1.remove(7)

    # l1.save()



