# Paso 2: clase Contact
class Contact:
    def __init__(self, name, number):
        self.name = name      # nombre del contacto (string)
        self.number = number  # telefono (string), ej. "123-456-7890"

    def __str__(self):
        return f"{self.name}: {self.number}"


# Paso 3: clase Node (nodo de la lista enlazada)
class Node:
    def __init__(self, key, value):
        self.key = key      # el nombre del contacto, se usa como llave
        self.value = value  # el objeto Contact
        self.next = None    # siguiente nodo en la cadena


# Paso 4: clase HashTable (encadenamiento separado)
class HashTable:
    def __init__(self, size):
        self.size = size              # tamano fijo del arreglo
        self.data = [None] * size     # cada posicion es None o el primer Node

    def hash_function(self, key):
        # Suma los valores ord() de cada letra y usa modulo para obtener un indice valido
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size

    def insert(self, key, value):
        # 'value' aqui es el numero de telefono; se crea el Contact adentro
        index = self.hash_function(key)
        current = self.data[index]

        # Si la llave ya existe, solo actualizamos el numero
        last = None
        while current is not None:
            if current.key == key:
                current.value.number = value
                return
            last = current
            current = current.next

        # Si no existe, creamos el nodo y lo agregamos al final de la cadena
        new_node = Node(key, Contact(key, value))
        if last is None:
            self.data[index] = new_node
        else:
            last.next = new_node

    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]

        # Recorre la lista enlazada buscando el nombre
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None  # no se encontro

    def print_table(self):
        for i in range(self.size):
            current = self.data[i]
            if current is None:
                print(f"Index {i}: Empty")
            else:
                line = f"Index {i}:"
                while current is not None:
                    line += f" - {current.value}"
                    current = current.next
                print(line)


# Pasos 5 y 6: pruebas
if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()

    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    print()
    table.print_table()

    contact = table.search("John")
    print("\nSearch result:", contact)

    # Caso 1: colisiones ("Amy" y "May" tienen las mismas letras, mismo hash)
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    print()
    table.print_table()

    # Caso 2: llave duplicada, actualiza el numero
    table.insert("Rebecca", "999-444-9999")
    print()
    table.print_table()

    # Caso 3: buscar algo que no existe
    print(table.search("Chris"))  # None


# Paso 7: Memo de diseno
"""
Memo

A hash table is the right structure for fast lookups because it turns a
name into an array index with a hash function, so I can jump straight to
the right spot instead of scanning every contact. On average, inserting
and searching take constant time, O(1), even when the table holds hundreds
of entries. A list would need to check each contact one by one, which gets
slower as the list grows.

I handled collisions with separate chaining. Each slot in the array holds
either None or the first Node of a linked list. When two names hash to the
same index, such as "Amy" and "May", which contain the same letters and
therefore the same ord() sum, the new contact is added to the linked list
at that index. To search, I hash the name, go to that index, and walk the
chain comparing keys until I find a match or reach the end. If the name
already exists, insert() updates the number instead of adding a duplicate.

An engineer might choose a hash table over a list or tree when the main
operations are exact-match lookups, inserts, and updates, and when speed
matters more than order. A list is simple but slow to search, and a
balanced tree gives O(log n) lookups and keeps data sorted, which is useful
for range queries or alphabetical output. If you only need to find a
contact by name quickly, a hash table is usually the better choice. The
tradeoff is that it does not keep items in order, and performance can drop
if too many keys collide in the same slot.
"""