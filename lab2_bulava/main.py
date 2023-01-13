from controller import Controller

def main():
    dict_table = {
        'Online_store': ['online_store_id', 'name', 'link'],
        'Department_online_store': ['department_online_store_id', 'name', 'online_store_id'],
        'Product': ['product_id', 'name', 'department_online_store_id', 'price'],
        'Order': ['order_id', 'data', 'online_store_id', 'customers_id'],
        'Order_Product': ['order_id', 'product_id'],
        'Customers': ['customers_id', 'name']
    }
    dbname = 'Online_store'
    user = 'postgres'
    password = '1234'
    host = 'localhost'
    port = '5432'
    control = Controller(dict_table, dbname, user, password, host, port)
    control.menu()

if __name__ == '__main__':
    main()
