from datetime import datetime
from pydantic import ValidationError


class View:
    def __init__(self):
        self.tables = {
            1: 'Online_store',
            2: 'Department_online_store',
            3: 'Product',
            4: 'Order',
            5: 'Order_Product',
            6: 'Customers',
            7: 'Return in operations_menu',
        }
        self.sql_operations = {
            1: 'Show table',
            2: 'Show all tables',
            3: 'Search',
            4: 'Add data',
            5: 'Update data',
            6: 'Add random packed data',
            7: 'Delete data',
            8: 'Exit the program',
        }

    def menu_parser(self, menu, end):
        while True:
            for number, value in menu.items():
                print(number, value)
            value = input("Enter choice № ")
            try:
                value = int(value)
            except Exception:
                self.menu_parser(menu, end)
            else:
                if 1 <= value <= end:
                    return value
                else:
                    print(f"Enter the number from 1 to {end}")
                    self.menu_parser(menu, end)

    def operations_menu(self):
        value = self.menu_parser(self.sql_operations, 8)
        return value

    def tables_menu(self):
        value = self.menu_parser(self.tables, 7)
        if value == 7:
            return 7
        return self.tables[value]

    def search(self, columns):
        values = ['']
        for count in range(len(columns)):
            values[0] += columns[count] + ', '
            print(count + 1, columns[count])
        values.append(int(input('Enter number')))
        if 0 < values[1] <= len(columns):
            values[0] = values[0][:-2]
            values[1] = columns[values[1] - 1]
            values.append(input('write what you want search'))
            return values
        print('write correct')
        return self.search(columns)

    @staticmethod
    def create_data(columns, id_):
        values = {}
        for column in columns[id_:]:
            if column == 'data':
                value = datetime.now().strftime('%Y-%m-%d')
                values[column] = value
                continue
            print('Write value in column', column)
            value = input()
            values[column] = value
        return values

    def add_random(self):
        value = input('How many data you wanna random add')
        try:
            value = int(value)
        except Exception:
            self.add_random()
        else:
            if 1 <= value:
                return value
            else:
                print("Enter the number from 1")
                self.add_random()

    def delete_id(self):
        value = input('What data you wanna delete')
        try:
            value = int(value)
        except Exception:
            self.add_random()
        else:
            if 1 <= value:
                return value
            else:
                print("Enter the number from 1")
                self.add_random()