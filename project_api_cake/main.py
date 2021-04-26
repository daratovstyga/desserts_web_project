import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.exceptions import abort

from api import get_user_by_email, new_user, get_stocks, get_products, get_user, get_product, new_order, \
    get_user_orders, delete_order, get_order, order_edit, order_rate
from data import db_session
from data.users import User
from forms.login_form import LoginForm
from forms.register import RegisterForm
from data.orders import Order
from forms.new_order import NewOrderForm
from forms.edit_order import EditOrderForm
from forms.rate_form import RateForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        user = get_user_by_email(form.email.data)
        if user:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            birth_date=form.birth_date.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        new_user(user)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/')
@app.route('/main_window')
def main_window():
    return render_template('main_window.html')


@app.route('/catalog')
def catalog():
    products = get_products()
    return render_template('catalog.html', products=products)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/account/<user_id>')
def account(user_id):
    user = get_user(user_id)
    orders = get_user_orders(user_id)
    return render_template('account.html', user=user, orders=orders)


@app.route('/stocks')
def stocks():
    stocks = get_stocks()
    return render_template('stocks.html', stocks=stocks)


@app.route('/one_item/<product_id>')
def one_item(product_id):
    product = get_product(product_id)
    return render_template('one_item.html', item=product)


@app.route('/one_item/add_order/<product_id>/<user_id>', methods=['GET', 'POST'])
def add_order(product_id, user_id):
    form = NewOrderForm()
    if form.validate_on_submit():
        order = Order(
            delivery_date=form.delivery_date.data,
            product=product_id,
            client=user_id)
        new_order(order)
        return redirect(f'/account/{user_id}')
    return render_template('order.html', title='Сделать заказ', form=form)


@app.route('/account/<user_id>/order_delete/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_delete(order_id, user_id):
    user = get_user(user_id)
    if user:
        delete_order(order_id)
        return redirect(f'/account/{user_id}')
    else:
        abort(404)


@app.route('/account/<user_id>/edit_order/<order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(user_id, order_id):
    form = EditOrderForm()
    if request.method == "GET":
        order = get_order(order_id)
        if order:
            form.delivery_date.data = order.delivery_date
        else:
            abort(404)
    if form.validate_on_submit():
        order = get_order(order_id)
        if order:
            order_edit(order_id, form.delivery_date.data, form.taken.data)
            return redirect(f'/account/{user_id}')
        else:
            abort(404)
    return render_template('edit_order.html', title='Редактирование заказа', form=form)


@app.route('/account/<user_id>/rate_order/<order_id>', methods=['GET', 'POST'])
def rate(user_id, order_id):
    form = RateForm()
    if form.validate_on_submit():
        order = get_order(order_id)
        if order:
            order_rate(order_id, form.rating.data)
            return redirect(f'/account/{user_id}')
        else:
            abort(404)
    return render_template('rate_order.html', title='Оцените заказ', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run()
