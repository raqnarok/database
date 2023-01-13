import psycopg2
from abc import abstractmethod
from datetime import datetime


class Model:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.returns = None
        self.cursor = None

    def connect(self):
        return psycopg2.connect(dbname=self.database, user=self.user, password=self.password,
                                host=self.host, port=self.port)

    def execute(self, operation_num, table=None, values=None, name_columns=None):
        with self.connect() as con:
            try:
                self.cursor = con.cursor()
                task = Task(self.cursor, table, values, name_columns)
                self.returns = task.get_task(operation_num)
                con.commit()
            except (Exception, psycopg2.Error) as e:
                print("Check you value", e)
            finally:
                if self.cursor:
                    self.cursor.close()
                    if self.returns:
                        return self.returns


class Task:
    def __init__(self, cursor, table, values, name_columns):
        self.dict_foo = None
        self.cur = cursor
        self.table = table
        self.values = values
        self.name_columns = name_columns

    def get_task(self, task_index):
        self.dict_foo = {
            1: self.select_table,
            2: self.select_all_tables,
            3: self.search,
            4: self.insert_data,
            5: self.update_data,
            6: self.insert_random,
            7: self.delete_data,
        }
        return self.dict_foo[task_index]()

    def print_fetchall(self):
        tuple_data = self.cur.fetchall()
        if tuple_data:
            for columns in tuple_data:
                for column in columns:
                    print(column, end='  ')
                print()
            return tuple_data
        else:
            print('Table is empty')

    def create_random_str(self):
        uppercase_letter = "chr(ascii('A') + (random() * 25)::int)"
        lowercase_letter = "chr(ascii('a') + (random() * 25)::int)"
        self.cur.execute(f"""SELECT ({uppercase_letter}{(" || " + lowercase_letter) * 30})""")

    def create_random_int(self):
        self.cur.execute(f'''SELECT (random() * 100 + 1)::int AS RAND_1_11;''')

    def fetch_random_id(self, table, id_):
        self.cur.execute(f'''SELECT {id_} FROM "{table}" ORDER BY random() LIMIT(1)''')

    @staticmethod
    def str_for_insert(our_data):
        return "'" + str(our_data) + "'"

    def select_table(self):
        self.cur.execute(f'''SELECT * FROM "{self.table}";''')
        print(self.table)
        for column in self.name_columns:
            print(column, end='   ')
        print()
        self.print_fetchall()

    def select_all_tables(self):
        for table_name in range (len(self.values)):
            print('           ', self.values[table_name])
            for column in self.name_columns[table_name]:
                print(column, end='   ')
            print()
            self.cur.execute(f'''SELECT * FROM "{self.values[table_name]}";''')
            self.print_fetchall()

    def search(self):
        self.cur.execute(f'''SELECT {self.values[0]} FROM "{self.table}" 
                    WHERE {self.values[1]}::VARCHAR LIKE '%{self.values[2]}%';''')
        self.print_fetchall()

    def insert_data(self):
        str_keys = ''
        str_value = ''
        for key, value in self.values.items():
            str_keys += key + ' ,'
            str_value += self.str_for_insert(value) + ' ,' if isinstance(value, str) else str(value) + ', '
        str_keys = str_keys[:-2]
        str_value = str_value[:-2]
        self.cur.execute(f"""INSERT INTO "{self.table}" ({str_keys})
                            VALUES ({str_value}); """)
        print('Successfully completed')

    def update_data(self):
        column_id_ = list(self.values.keys())[0]
        id_ = self.values[column_id_]
        del self.values[column_id_]
        str_set = ''
        for key, value in self.values.items():
            if value:
                str_set += key + ' = ' + (self.str_for_insert(value) + ' ,'
                                          if isinstance(value, str) else str(value) + ' ,')
        str_set = str_set[:-2]
        self.cur.execute(f"""UPDATE  "{self.table}"
                                    SET {str_set}
                                    WHERE {column_id_}  = {id_}; """)
        print('Successfully completed')

    def insert_random(self):
        id_ = 1 if self.table != 'Order_Product' else 0
        self.values = {}
        self.cur.execute(f'''SELECT column_name, data_type FROM information_schema.columns 
                    WHERE table_name = '{self.table}';''')
        tuple_data = [self.cur.fetchall()]
        self.cur.execute(f'''SELECT
                tc.table_schema, 
                tc.constraint_name, 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_schema AS foreign_table_schema,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN (select row_number() over (partition by table_schema, table_name, 
                    constraint_name order by row_num) ordinal_position,
                             table_schema, table_name, column_name, constraint_name
                      from   (select row_number() over (order by 1) row_num, table_schema, 
                      table_name, column_name, constraint_name
                              from   information_schema.constraint_column_usage
                             ) t
                     ) AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
                  AND ccu.ordinal_position = kcu.ordinal_position
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = '{self.table}';''')
        tuple_data.append(self.cur.fetchall())
        for list_data in tuple_data[0][id_:]:
            for data_column in tuple_data[1]:
                if list_data[0] == data_column[3]:
                    self.fetch_random_id(data_column[5], list_data[0])
                    break
            else:
                if list_data[1] == 'integer' or list_data[1] == 'numeric':
                    self.create_random_int()
                elif list_data[1] == 'date':
                    value = datetime.now().strftime('%Y-%m-%d')
                    self.values[list_data[0]] = value
                    continue
                else:
                    self.create_random_str()
            self.values[list_data[0]] = self.cur.fetchall()[0][0]
        return self.values

    def delete_data(self):
        self.cur.execute(f'''DELETE FROM "{self.table}" WHERE {self.values[0]} = {self.values[1]};''')
        print('Successfully completed')
