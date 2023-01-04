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
            3: 'Add data',
            4: 'Update data',
            5: 'Delete data',
            6: 'Exit the program',
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
        value = self.menu_parser(self.sql_operations, 6)
        return value

    def tables_menu(self):
        value = self.menu_parser(self.tables, 7)
        return value

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

    def delete_id(self):
        value = input('What data you wanna delete')
        try:
            value = int(value)
        except Exception:
            self.delete_id()
        else:
            if 1 <= value:
                return value
            else:
                print("Enter the number from 1")
                self.delete_id()
