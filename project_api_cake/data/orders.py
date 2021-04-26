import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    delivery_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=None)
    is_taken = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    product = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
    client = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')
    name = orm.relation('Product')
