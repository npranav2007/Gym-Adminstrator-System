from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.db import init_db, get_db
from utils.bmi_calculator import calculate_bmi, calculate_calories
from utils.sms_sender import send_sms
import os
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize the database
init_db()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        users = db['users']

        if username in users and check_password_hash(users[username]['password'], password):
            session['user_id'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('signup.html')

        db = get_db()
        users = db['users']

        if username in users:
            flash('Username already exists!', 'danger')
            return render_template('signup.html')

        users[username] = {
            'username': username,
            'password': generate_password_hash(password),
            'created_at': datetime.datetime.now().isoformat()
        }
        db['users'] = users
        db.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    customers = db.get('customers', {})
    plans = db.get('plans', {})

    total_customers = len(customers)
    active_plans = sum(1 for customer_id, customer in customers.items()
                       if
                       customer.get('plan_id') and customer.get('plan_end_date') > datetime.datetime.now().isoformat())

    return render_template('dashboard.html',
                           total_customers=total_customers,
                           active_plans=active_plans)


@app.route('/customers')
def customers():
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    customers = db.get('customers', {})
    plans = db.get('plans', {})

    return render_template('customers.html', customers=customers, plans=plans)


@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        goal = request.form['goal']  # weight_loss or weight_gain
        target_weight = float(request.form['target_weight'])

        db = get_db()
        customers = db.get('customers', {})

        # Generate a customer ID
        customer_id = f"CUST{len(customers) + 1:04d}"

        # Calculate BMI
        bmi = calculate_bmi(weight, height)

        # Calculate daily calorie needs
        daily_calories = calculate_calories(weight, height, age, goal)

        customers[customer_id] = {
            'id': customer_id,
            'name': name,
            'mobile': mobile,
            'email': email,
            'age': age,
            'weight': weight,
            'height': height,
            'goal': goal,
            'target_weight': target_weight,
            'bmi': bmi,
            'daily_calories': daily_calories,
            'created_at': datetime.datetime.now().isoformat(),
            'plan_id': None,
            'plan_start_date': None,
            'plan_end_date': None
        }

        db['customers'] = customers
        db.sync()

        flash(f'Customer {name} added successfully!', 'success')
        return redirect(url_for('customers'))

    return render_template('add_customer.html')


@app.route('/customers/<customer_id>')
def customer_detail(customer_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    customers = db.get('customers', {})
    plans = db.get('plans', {})

    if customer_id not in customers:
        flash('Customer not found', 'danger')
        return redirect(url_for('customers'))

    customer = customers[customer_id]
    plan = plans.get(customer.get('plan_id', ''), None)

    return render_template('customer_detail.html', customer=customer, plan=plan)


@app.route('/customers/<customer_id>/add_plan', methods=['GET', 'POST'])
def add_plan(customer_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    customers = db.get('customers', {})
    plans = db.get('plans', {})

    if customer_id not in customers:
        flash('Customer not found', 'danger')
        return redirect(url_for('customers'))

    if request.method == 'POST':
        plan_type = request.form['plan_type']  # monthly, quarterly, yearly
        amount = float(request.form['amount'])

        # Calculate plan duration in days
        duration = {
            'monthly': 30,
            'quarterly': 90,
            'yearly': 365
        }.get(plan_type, 30)

        plan_start_date = datetime.datetime.now()
        plan_end_date = plan_start_date + datetime.timedelta(days=duration)

        # Generate a plan ID
        plan_id = f"PLAN{len(plans) + 1:04d}"

        # Create the plan
        plans[plan_id] = {
            'id': plan_id,
            'customer_id': customer_id,
            'plan_type': plan_type,
            'amount': amount,
            'start_date': plan_start_date.isoformat(),
            'end_date': plan_end_date.isoformat(),
            'created_at': datetime.datetime.now().isoformat()
        }

        # Update the customer with the plan
        customers[customer_id]['plan_id'] = plan_id
        customers[customer_id]['plan_start_date'] = plan_start_date.isoformat()
        customers[customer_id]['plan_end_date'] = plan_end_date.isoformat()

        db['plans'] = plans
        db['customers'] = customers
        db.sync()

        # Send SMS notification
        customer = customers[customer_id]
        sms_text = (
            f"Welcome to Our Gym, {customer['name']}!\n"
            f"Your BMI: {customer['bmi']:.1f}\n"
            f"Daily Calorie Target: {customer['daily_calories']:.0f} kcal\n"
            f"Plan: {plan_type.capitalize()}\n"
            f"Start Date: {plan_start_date.strftime('%d-%m-%Y')}\n"
            f"End Date: {plan_end_date.strftime('%d-%m-%Y')}"
        )

        try:
            send_sms(customer['email'], sms_text)
            flash(f'Plan added and Email notification sent to {customer["name"]}!', 'success')
        except Exception as e:
            flash(f'Plan added but Email failed: {str(e)}', 'warning')

        return redirect(url_for('customer_detail', customer_id=customer_id))

    customer = customers[customer_id]
    return render_template('add_plan.html', customer=customer)


if __name__ == '__main__':
    app.run(debug=True)