from controller import Controller

def main():
    dict_table = {
        1 : ['online_store_id', 'name', 'link'],
        2 : ['department_online_store_id', 'name', 'online_store_id'],
        3 : ['product_id', 'name', 'department_online_store_id', 'price'],
        4 : ['order_id', 'data', 'online_store_id', 'customers_id'],
        5 : ['order_id', 'product_id'],
        6 : ['customers_id', 'name']
    }
    dbname = 'Online_store'
    user = 'postgres'
    password = '1234'
    host = 'localhost'
    port = 5432
    control = Controller(dict_table, dbname, user, password, host, port)
    control.menu()

if __name__ == '__main__':
    main()
