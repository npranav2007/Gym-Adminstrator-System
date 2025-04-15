import datetime
from utils.db import get_db
from utils.bmi_calculator import calculate_bmi, calculate_calories


class Customer:

    def __init__(self, customer_id=None, name=None, mobile=None, email=None,
                 age=None, weight=None, height=None, goal=None, target_weight=None,
                 customer_data=None):
        if customer_data:
            self.id = customer_data.get('id')
            self.name = customer_data.get('name')
            self.mobile = customer_data.get('mobile')
            self.email = customer_data.get('email')
            self.age = customer_data.get('age')
            self.weight = customer_data.get('weight')
            self.height = customer_data.get('height')
            self.goal = customer_data.get('goal')
            self.target_weight = customer_data.get('target_weight')
            self.bmi = customer_data.get('bmi')
            self.daily_calories = customer_data.get('daily_calories')
            self.created_at = customer_data.get('created_at')
            self.plan_id = customer_data.get('plan_id')
            self.plan_start_date = customer_data.get('plan_start_date')
            self.plan_end_date = customer_data.get('plan_end_date')
        else:
            db = get_db()
            customers = db.get('customers', {})
            self.id = customer_id or f"CUST{len(customers) + 1:04d}"

            self.name = name
            self.mobile = mobile
            self.email = email
            self.age = age
            self.weight = weight
            self.height = height
            self.goal = goal
            self.target_weight = target_weight

            if weight and height:
                self.bmi = calculate_bmi(weight, height)
                if age:
                    self.daily_calories = calculate_calories(weight, height, age, goal)
                else:
                    self.daily_calories = 0
            else:
                self.bmi = 0
                self.daily_calories = 0

            self.created_at = datetime.datetime.now().isoformat()
            self.plan_id = None
            self.plan_start_date = None
            self.plan_end_date = None

    @staticmethod
    def get(customer_id):
        db = get_db()
        customers = db.get('customers', {})

        if customer_id in customers:
            return Customer(customer_data=customers[customer_id])
        return None

    @staticmethod
    def get_all():

        db = get_db()
        customers = db.get('customers', {})

        return [Customer(customer_data=customer_data) for customer_id, customer_data in customers.items()]

    def save(self):
        db = get_db()
        customers = db.get('customers', {})

        customers[self.id] = {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal,
            'target_weight': self.target_weight,
            'bmi': self.bmi,
            'daily_calories': self.daily_calories,
            'created_at': self.created_at,
            'plan_id': self.plan_id,
            'plan_start_date': self.plan_start_date,
            'plan_end_date': self.plan_end_date
        }

        db['customers'] = customers
        db.sync()
        return True

    def add_plan(self, plan):
        self.plan_id = plan.id
        self.plan_start_date = plan.start_date
        self.plan_end_date = plan.end_date
        return self.save()

    def is_plan_active(self):
        if not self.plan_end_date:
            return False

        end_date = datetime.datetime.fromisoformat(self.plan_end_date)
        return end_date > datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal,
            'target_weight': self.target_weight,
            'bmi': self.bmi,
            'daily_calories': self.daily_calories,
            'created_at': self.created_at,
            'plan_id': self.plan_id,
            'plan_start_date': self.plan_start_date,
            'plan_end_date': self.plan_end_date,
            'plan_active': self.is_plan_active()
        }