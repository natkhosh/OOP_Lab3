from structure_driver import *
from builder import *
from LinkedList import *

driver_name = input("Введите название драйвера > ")
driver_builder = SDFabric.get_sd_driver(driver_name)

driver = driver_builder.build()


l1 = LinkedList()

l1.insert(12, 0)
l1.insert(30, 0)
print(l1, len(l1))
l1.append(1)
print(l1, len(l1))
l1.append(3)
print(l1, len(l1))
l1.append(5)
print(l1, len(l1))
l1.append(1)
print(l1, len(l1))
l1.insert(22, 6)
print(l1, len(l1))
l1.insert(7, 0)
print(l1, len(l1))


l1.set_structure_driver(driver)
l1.save()