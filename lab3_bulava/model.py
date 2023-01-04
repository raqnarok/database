import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from abc import abstractmethod

Base = declarative_base()


class OnlineStore(Base):
    __tablename__ = 'Online_store'
    online_store_id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)

    def __init__(self, name, link):
        self.name = name
        self.link = link
        super(OnlineStore, self).__init__()


class DepartmentOnlineStore(Base):
    __tablename__ = 'Department_online_store'
    department_online_store_id = Column(Integer, primary_key=True)
    name = Column(String)
    online_store_id = Column(Integer, ForeignKey('Online_store.online_store_id'))

    online_store = relationship('OnlineStore', foreign_keys=[online_store_id])

    def __init__(self, name, online_store_id):
        self.name = name
        self.online_store_id = online_store_id
        super(DepartmentOnlineStore, self).__init__()


class Product(Base):
    __tablename__ = 'Product'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    department_online_store_id = Column(Integer, ForeignKey('Department_online_store.department_online_store_id'))
    price = Column(Integer)

    department_online_store = relationship('DepartmentOnlineStore', foreign_keys=[department_online_store_id])

    def __init__(self, name, department_id, price):
        self.name = name
        self.department_id = department_id
        self.price = price
        super(Product, self).__init__()


class Order(Base):
    __tablename__ = 'Order'
    order_id = Column(Integer, primary_key=True)
    data = Column(sqlalchemy.Time)
    online_store_id = Column(Integer, ForeignKey('Online_store.online_store_id'))
    customers_id = Column(Integer, ForeignKey('Customers.customers_id'))

    online_store = relationship("OnlineStore", foreign_keys=[online_store_id])
    customers = relationship("Customers", foreign_keys=[customers_id])

    def __init__(self, plant_id, date, customers_id):
        self.plant_id = plant_id
        self.date = date
        self.customers_id = customers_id
        super(Order, self).__init__()


class OrderProduct(Base):
    __tablename__ = 'Order_Product'
    order_id = Column(Integer, ForeignKey('Order.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)

    order = relationship("Order", foreign_keys=[order_id])
    product = relationship("Product", foreign_keys=[product_id])

    def __init__(self, order_id, product_id):
        self.order_id = order_id
        self.product_id = product_id
        super(OrderProduct, self).__init__()


class Customers(Base):
    __tablename__ = 'Customers'
    customers_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
        super(Customers, self).__init__()


class Model:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dict_foo = {
            1: SelectTable,
            2: InsertData,
            3: UpdateData,
            4: DeleteData,
        }
        self.dict_table = {
            1: OnlineStore,
            2: DepartmentOnlineStore,
            3: Product,
            4: Order,
            5: OrderProduct,
            6: Customers,
        }

    def get_engine(self):
        return create_engine(url=f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")

    def connect(self):
        try:
            _engine = self.get_engine()
            Base.metadata.create_all(_engine)
            return sessionmaker(bind=_engine)()
        except Exception as ex:
            print("Connection could not be made due to the following error: \n", ex)

    def execute(self, task, table_name=None, values=None):
        session = self.connect()
        tasks = self.dict_foo[task](session, self.dict_table[table_name], values, task)
        tasks()


class Task:
    def __init__(self, session, table, values, task):
        self.session = session
        self.table = table
        self.values = values
        self.task = task
        self.table_id = {
            1: OnlineStore.online_store_id,
            2: DepartmentOnlineStore.department_online_store_id,
            3: Product.product_id,
            4: Order.order_id,
            5: OrderProduct.order_id,
            6: Customers.customers_id,
        }
        # self.table_row = {
        #     1: [online_store_id, name, link],
        #     2: [department_id, name, online_store_id],
        #     3: [product_id, name, department_id, price],
        #     4: [order_id, price],
        #     6: [customers_id, name],
        # }

    @abstractmethod
    def __call__(self):
        raise NotImplemented


class SelectTable(Task):
    def __call__(self):
        for item in self.session.query(self.table).all():
            for column in item.__table__.columns:
                print(column.name, end='  ')
            print()
            break
        for item in self.session.query(self.table).all():
            for value in tuple(getattr(item, column.name) for column in item.__table__.columns):
                print(value, end='  ')
            print()


class InsertData(Task):
    def __call__(self):
        self.session.add(self.table(*self.values.values()))
        self.session.commit()


class UpdateData(Task):
    def __call__(self):
        column_id_ = list(self.values.keys())[0]
        id_ = self.values[column_id_]
        del self.values[column_id_]
        data = list(self.values.values())
        row = self.session.query(self.table).get(id_)
        columns = [col for col in row.__table__.columns.keys()]
        columns.pop(0)

        for column, d in zip(columns, data):
            if d != '-':
                row.__setattr__(column, d)
        self.session.commit()

class DeleteData(Task):
    def __call__(self):
        row_ = self.session.query(self.table).get(self.values[1])
        if row_:
            self.session.delete(row_)
            self.session.commit()
