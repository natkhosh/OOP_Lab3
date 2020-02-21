from weakref import ref
from structure_driver import *


class Node:
    def __init__(self, prev_node=None, next_node=None, data=None):

        if prev_node is not None and not isinstance(prev_node, type(self)):
            raise TypeError('prev_node must be Node or None')

        if next_node is not None and not isinstance(next_node, type(self)):
            raise TypeError('next_node must be Node or None')

        self.prev_node = ref(prev_node) if prev_node is not None else None
        self.next_node = next_node
        self.data = data

    def __str__(self):
        return self.data


class LinkedList:
    def __init__(self, head=None, tail=None, size=0, _structure_driver=None):
        self.size = 0
        self.head = None
        self.tail = None

        self.__structure_driver = None

    def __str__(self):
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

    @property
    def str_size(self):
        """
        Метод, позволяющий посмотреть длину списка
        :return: int
        """
        return f" (Элементов: {self.size})"

    def append(self, data):
        if self.head is None:
            new_node = Node(None, None, data)
            new_node.next_node = new_node.prev_node = new_node
            self.head = new_node

        else:
            self.tail = self.head.prev_node
            new_node = Node(None, None, data)
            new_node.data = data
            new_node.next_node = self.head
            self.head.prev_node = new_node
            new_node.prev_node = self.tail
            self.tail.next_node = new_node
        self.size += 1

    def insert(self, node, index=0):
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
            self.tail = self.head.prev_node
            new_node = Node(None, None, node)
            new_node.data = node  # Inserting the data
            new_node.next_node = self.head
            new_node.prev_node = self.tail
            self.tail.next_node = self.head.prev_node = new_node
            self.head = new_node
            self.size += 1
        elif index > self.size-1:
            self.append(node)
        else:
            current_node = self.head
            next = current_node.next_node
            i = 0
            while i < self.size-1:
                if i+1 == index:
                    current_node.next_node = None
                    next.prev_node = None
                    new_node = Node(current_node, next, node)
                    current_node.next_node = new_node
                    next.prev_node = ref(new_node)

                current_node = current_node.next_node
                next = current_node.next_node
                i += 1
            self.size += 1

    def clear(self):
        '''
        Очистка списка
        '''
        self.__init__()

    def find(self, node):
        if not isinstance(node, (int, str)):
            raise TypeError

        current_node = self.head
        list_i = []
        i = 0
        while i < self.size+1:
            if current_node.data == node:
                list_i.append(i)
            i += 1
            current_node = current_node.next_node

        if len(list_i) == 0:
            return "Такого элемента в списке нет!"
        elif len(list_i) == 1:
            return list_i[0]
        else:
            return list_i

    def remove(self, node):
        if self.head is None:
            print("Список пустой")
            return
        if self.head.next_node is None:
            if self.head.data == node:
                self.head = None
            else:
                print("Элемент не найден")
            return

        if self.head.data == node:
            current_node = self.head
            self.head = current_node.next_node
            current_node.next_node = None
            current_node.prev_node = None
            self.head.prev_node = ref(self.tail)
            self.tail.next_node = self.head
            self.size -= 1
            return

        current_node = self.head

        if current_node.next_node is not None:
            current_node = current_node.next_node
            current_prev = self.head
            current_next = current_node.next_node
            current_prev.next_node = current_node
            current_node.prev_node = ref(current_prev)
            i = 1
            while i != self.size+1:
                if current_node.data == node:
                    current_prev.next_node = current_next
                    current_next.prev_node = ref(current_prev)
                    current_node.prev_node = None
                    current_node.next_node = None
                    current_node = current_next
                else:
                    if (i == self.size and current_node.data != node):
                        print("Элемент не найден")
                        current_node = current_node.next_node
                        current_prev = current_prev.next_node
                        current_next = current_next.next_node
                        self.size += 1
                        break
                    else:
                        current_node = current_node.next_node
                        current_prev = current_prev.next_node
                        current_next = current_next.next_node
                i += 1
        else:
            print("Элемент не найден")
            self.size += 1
        self.size -= 1

    def delete(self, index):
        if not isinstance(index, int):
            raise TypeError
        ...


    def __to_dict(self):
        d = {}
        i = 0
        current_node = self.head
        while i < self.size:
            d[i] = current_node.data
            i += 1
            current_node = current_node.next_node
        return d

    def __from_dict(self, d={0: 3, 1: 5, 2: 6, 3: 22, 4: 1}):
        for index, value in d.items():
            self.insert(value, index)
        print(self.__to_dict())

    def load(self):
        self.__from_dict(self.__structure_driver.read())

    def save(self):
        self.__structure_driver.write(self.__to_dict())

    def set_structure_driver(self, driver):
        self.__structure_driver = driver


if __name__ == "__main__":
    l1 = LinkedList()
    l1.insert(66, 0)
    print(l1, l1.str_size)
    l1.append(1)
    print(l1, l1.str_size)
    l1.append(3)
    print(l1, l1.str_size)
    l1.append(5)
    print(l1, l1.str_size)
    l1.append(6)
    print(l1, l1.str_size)
    l1.insert(22, 0)
    print(l1, l1.str_size)
    # print('---')
    # print(l1._LinkedList__to_dict())
    # print('---')
    # l1.clear()
    # d = {0: 3, 1: 5, 2: 6, 3: 22, 4: 1}
    # print(l1._LinkedList__from_dict())

    # print(l1)
    # l1.from_dict()

    l1.set_structure_driver(JSONFileDriver('test_00.json'))
    l1.save()

