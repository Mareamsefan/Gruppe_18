import os
from flask_login import LoginManager, login_required, logout_user, current_user
from Gruppe_18.src.main.controller.TourController import TourController
from Gruppe_18.src.main.model.models import Account, Tour
from Gruppe_18.src.main.database.app_config import app
from Gruppe_18.src.main.repository.AccountRepository import AccountRepository
from flask import render_template, redirect, url_for
from Gruppe_18.src.main.database.create_data_db import get_session
from Gruppe_18.src.main.controller.AccountController import AccountController
from Gruppe_18.src.main.repository.TourRepository import TourRepository

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

is_testing = os.environ.get("locust_test", False)

test_database = os.path.abspath('../../test/Test.db')
print(is_testing)

db_path = test_database if is_testing else "YourGuide.db"


def sessions():
    return get_session(db_path)


app.secret_key = 'gruppe_18'


def account_c():
    sessions = get_session(db_path)
    repository = AccountRepository(sessions)
    return AccountController(repository, sessions)


def tour_c():
    sessions = get_session(db_path)
    repository = TourRepository(sessions)
    return TourController(repository, sessions)


@login_manager.user_loader
def load_user(user_id):
    with sessions() as session:
        return session.query(Account).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    account_controller = account_c()
    return account_controller.account_login()


@app.route('/home')
def home():
    tour_controller = tour_c()
    return tour_controller.homepage_based_on_usertype()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account_reg', methods=['GET', 'POST'])
def account_reg():
    account_controller = account_c()
    return account_controller.account_registration()


@app.route('/search', methods=['GET'])
def search():
    tour_controller = tour_c()
    return tour_controller.search_tour()


@app.route('/register_for_tour', methods=['POST'])
def register_for_tour():
    account_controller = account_c()
    return account_controller.tour_registration()


@app.route('/user_tours')
def user_tours():
    tour_controller = tour_c()
    return tour_controller.get_user_tours()


@app.route('/cancel_tour', methods=['POST'])
def cancel_tour():
    account_controller = account_c()
    return account_controller.account_cancel_tour()


@app.route('/new_tour', methods=['POST', 'GET'])
def new_tour():
    tour_controller = tour_c()
    return tour_controller.make_new_tour()


@app.route('/guide_tours')
def guide_tours():
    tour_controller = tour_c()
    return tour_controller.show_guide_tour()


@app.route('/delete_tour', methods=['POST'])
def delete_tour():
    tour_controller = tour_c()
    return tour_controller.deleting_tour()

#
@app.route('/show_all_tours', methods=['GET'])
def show_tours():
    tour_controller = tour_c()
    return tour_controller.show_all_tours()

#
@app.route('/hide_tours', methods=['GET'])
def hide_tours():
    tour_controller = tour_c()
    return tour_controller.hide_all_tours()


@app.route('/show_all_users', methods=['GET'])
def show_all_users():
    account_controller = account_c()
    return account_controller.admin_get_all_users()



@app.route('/hide_all_users', methods=['GET'])
def hide_all_users():
    account_controller = account_c()
    return account_controller.admin_hide_all_user()


@app.route('/delete_account', methods=['POST'])
def delete_account():
    account_controller = account_c()
    return account_controller.deleting_account()

#
@app.route('/show_dashboard', methods=['GET'])
def show_dashboard():
    tour_controller = tour_c()
    return tour_controller.show_dashboard()


@app.route('/hide_dashboard', methods=['GET'])
def hide_dashboard():
    tour_controller = tour_c()
    return tour_controller.hide_dashboard()


@app.route('/profile')
@login_required
def profile():
    account_controller = account_c()
    return account_controller.show_profile()


@app.route('/delete_user', methods=['POST'])
def delete_user():
    account_controller = account_c()
    return account_controller.delete_my_account()


@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    account_controller = account_c()
    return account_controller.update_user_information()


@app.route('/upgrade_usertype', methods=['POST'])
def upgrade_usertype():
    account_controller = account_c()
    return account_controller.update_usertype()


@app.route('/home/filter', methods=['GET','POST'])
def filter_tour():
    tour_controller = tour_c()
    return tour_controller.filter_app()


if __name__ == '__main__':
    app.run(debug=True)
