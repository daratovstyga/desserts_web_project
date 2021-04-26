from data import db_session
from data.orders import Order
from data.products import Product
from data.stocks import Stock
from data.users import User


def get_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def get_order(order_id):
    session = db_session.create_session()
    return session.query(Order).get(order_id)


def get_stock(stock_id):
    session = db_session.create_session()
    return session.query(Stock).get(stock_id)


def get_stocks():
    session = db_session.create_session()
    return session.query(Stock).all()


def get_products():
    voc = {}
    session = db_session.create_session()
    types = session.query(Product.type).all()
    types = [types[i][0] for i in range(len(types)) if types[i] not in types[:i]]
    for i in types:
        voc[i] = session.query(Product).filter(Product.type == i)
    return voc


def get_product(product_id):
    session = db_session.create_session()
    return session.query(Product).get(product_id)


def get_user_orders(user_id):
    session = db_session.create_session()
    return session.query(Order).filter(Order.client == user_id)


def new_user(user):
    session = db_session.create_session()
    session.add(user)
    session.commit()


def get_user_by_email(email):
    session = db_session.create_session()
    return session.query(User).filter(User.email == email).first()


def get_products_by_type(type):
    session = db_session.create_session()
    return session.query(Product).filter(Product.type == type)


def delete_order(order_id):
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    session.delete(order)
    session.commit()


def order_edit(order_id, delivery_date, taken):
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    order.delivery_date = delivery_date
    order.is_taken = taken
    session.add(order)
    session.commit()


def new_order(order):
    session = db_session.create_session()
    session.add(order)
    session.commit()


def order_rate(order_id, rating):
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    order.rating = rating
    session.add(order)
    session.commit()
