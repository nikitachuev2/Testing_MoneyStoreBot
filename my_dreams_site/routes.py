
from app import app, db, login_manager  # Импортируйте login_manager
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, PurchaseForm, GoalForm
from models import User, Purchase, Goal

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/add_purchase", methods=['GET', 'POST'])
@login_required
def add_purchase():
    form = PurchaseForm()
    if form.validate_on_submit():
        purchase = Purchase(user_id=current_user.id, category=form.category.data, amount=form.amount.data)
        db.session.add(purchase)
        db.session.commit()
        flash('Purchase added!', 'success')
        return redirect(url_for('add_purchase'))
    return render_template('add_purchase.html', form=form)

@app.route("/goals", methods=['GET', 'POST'])
@login_required
def goals():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(user_id=current_user.id, target_amount=form.target_amount.data)
        db.session.add(goal)
        db.session.commit()
        flash('Goal set!', 'success')
        return redirect(url_for('goals'))
    return render_template('goals.html', form=form)
