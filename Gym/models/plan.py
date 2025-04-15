from utils.db import get_db
from datetime import datetime, timedelta


class Plan:

    def __init__(self, customer_id, plan_type, amount, start_date, plan_data=None):
        if plan_data:
            self.id = plan_data.get('id')
            self.customer_id = plan_data.get('customer_id')
            self.plan_type = plan_data.get('plan_type')
            self.amount = plan_data.get('amount')
            self.start_date = datetime.fromisoformat(plan_data.get('start_date'))
            self.end_date = datetime.fromisoformat(plan_data.get('end_date'))
            self.created_at = plan_data.get('created_at')
            self.updated_at = plan_data.get('updated_at')
        else:
            self.id = None  # Assigned when saving
            self.customer_id = customer_id
            self.plan_type = plan_type
            self.amount = amount
            self.start_date = start_date
            self.end_date = self.calculate_end_date(plan_type, start_date)
            self.created_at = datetime.utcnow().isoformat()
            self.updated_at = None

    @staticmethod
    def get_db():
        """
        Get the database for plans.

        Returns:
            dict: Plans dictionary from the database.
        """
        db = get_db()
        return db.get('plans', {})

    @staticmethod
    def calculate_end_date(plan_type, start_date):
        """
        Calculate the end date based on the plan type.

        Args:
            plan_type (str): Type of plan ('monthly', 'quarterly', 'yearly').
            start_date (datetime): Start date of the plan.

        Returns:
            datetime: Calculated end date.
        """
        durations = {
            'monthly': 30,
            'quarterly': 90,
            'yearly': 365
        }
        if plan_type not in durations:
            raise ValueError("Invalid plan type. Must be 'monthly', 'quarterly', or 'yearly'")

        return start_date + timedelta(days=durations[plan_type])

    @staticmethod
    def get(plan_id):
        """
        Get a plan by ID.

        Args:
            plan_id (int): Plan ID.

        Returns:
            Plan: Plan instance or None if not found.
        """
        db = Plan.get_db()
        plan_data = db.get(plan_id)
        return Plan(plan_data=plan_data) if plan_data else None

    @staticmethod
    def get_by_customer(customer_id):
        """
        Get all plans for a specific customer.

        Args:
            customer_id (str): Customer ID.

        Returns:
            list: List of Plan instances.
        """
        db = Plan.get_db()
        return [Plan(plan_data=plan) for plan in db.values() if plan['customer_id'] == customer_id]

    @staticmethod
    def get_all():
        """
        Get all plans.

        Returns:
            list: List of Plan instances.
        """
        db = Plan.get_db()
        return [Plan(plan_data=plan) for plan in db.values()]

    def save(self):
        """
        Save the plan to the database.

        Returns:
            bool: True if successful, False otherwise.
        """
        db = get_db()
        plans = db.get('plans', {})

        # Assign an ID if new plan
        if not self.id:
            self.id = max(plans.keys(), default=0) + 1

        plans[self.id] = {
            'id': self.id,
            'customer_id': self.customer_id,
            'plan_type': self.plan_type,
            'amount': self.amount,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        db['plans'] = plans
        db.sync()
        return True

    def update(self, **kwargs):
        """
        Update plan details.

        Args:
            **kwargs: Fields to update.

        Returns:
            bool: True if updated, False otherwise.
        """
        db = get_db()
        plans = db.get('plans', {})

        if self.id in plans:
            for key, value in kwargs.items():
                if key in plans[self.id]:
                    setattr(self, key, value)
                    plans[self.id][key] = value
            self.updated_at = datetime.utcnow().isoformat()
            plans[self.id]['updated_at'] = self.updated_at

            db['plans'] = plans
            db.sync()
            return True
        return False
