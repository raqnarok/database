from model import Model
from view import View


class Controller:
    def __init__(self, dict_table, dbname, user, password, host, port):
        self.view_obj = View()
        self.model_obj = Model(dbname, user, password, host, port)
        self.dict_table = dict_table

    def menu_table(self, operation_num):
        table_name = self.view_obj.tables_menu()
        if table_name != 7:
            if operation_num == 1:
                self.model_obj.execute(operation_num, table_name=table_name)
            elif operation_num == 3:
                id_ = 0 if table_name == 5 else 1
                data = self.view_obj.create_data(self.dict_table[table_name], id_=id_)
                self.model_obj.execute(2, table_name, data)
            elif operation_num == 4:
                data = self.view_obj.create_data(self.dict_table[table_name], id_=0)
                self.model_obj.execute(3, table_name, data)
            else:
                id_ = self.view_obj.delete_id()
                values = [self.dict_table[table_name][0], id_]
                self.model_obj.execute(4, table_name, values)

    def menu(self):
        while True:
            operation_num = self.view_obj.operations_menu()
            if operation_num == 2:
                for table_name in range(1, 7):
                    self.model_obj.execute(task=1, table_name=table_name)
            elif operation_num != 7:
                self.menu_table(operation_num)
            else:
                exit()
