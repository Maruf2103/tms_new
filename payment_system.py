# payment_system.py - Online payment processing system
from datetime import datetime
import random

class PaymentProcessor:
    def __init__(self):
        self.transactions = {}
        self.payment_methods = ['bkash', 'nagad', 'rocket', 'card']
    
    def process_payment(self, user_id, amount, payment_method="bkash", bus_id=None):
        """Process payment - simulate for demo"""
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
        
        # Simulate payment processing
        transaction_data = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'bus_id': bus_id,
            'amount': amount,
            'payment_method': payment_method,
            'status': 'completed',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'reference': f"REF{random.randint(10000,99999)}"
        }
        
        self.transactions[transaction_id] = transaction_data
        return transaction_data
    
    def verify_payment(self, transaction_id):
        """Verify payment status"""
        return self.transactions.get(transaction_id, {})
    
    def get_user_payments(self, user_id):
        """Get all payments for a user"""
        user_payments = []
        for transaction in self.transactions.values():
            if transaction['user_id'] == user_id:
                user_payments.append(transaction)
        return user_payments
    
    def get_payment_methods(self):
        """Get available payment methods"""
        return self.payment_methods

payment_processor = PaymentProcessor()
print("? Payment System Module Loaded")
