from flask import render_template, request, redirect, session
from base import app
from base.com.dao.user_dao import UserDAO
from base.com.vo.user_vo import UserVO
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user_vo = UserVO()
        user_dao = UserDAO()

        user_vo.name = name
        user_vo.email = email
        user_vo.password = generate_password_hash(password)

        user_dao.insert_user(user_vo)
        return redirect('/login')

    return render_template('admin/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_dao = UserDAO()
        user = user_dao.get_by_email(email)

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect('/userDetails')

        return render_template("admin/login.html")

    return render_template('admin/login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('admin/dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/view_users')
def view_users():
    user_dao = UserDAO()
    user_list = user_dao.view_all_users()
    return render_template('admin/viewUsers.html', user_list=user_list)


@app.route('/delete_user')
def delete_user():
    user_id = request.args.get('user_id')
    user_vo = UserVO()
    user_vo.id = user_id
    user_dao = UserDAO()
    user_dao.delete_user(user_vo)
    return redirect('/view_users')