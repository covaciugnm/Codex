"""Reject malformed client totals before any checkout side effects."""
import unittest
from pydantic import ValidationError
from app.dracula import DraculaCheckoutIn

class CheckoutTotalValidationTest(unittest.TestCase):
    def payload(self, total):
        return dict(customer=dict(first_name='Audit', last_name='Client', email='audit@example.com', phone='+40721123456'), shipping_address=dict(line1='Strada Test 10', city='Bucuresti', county='Bucuresti', postal_code='010101', country='RO'), delivery_method='courier', payment_method='cash_on_delivery', accept_terms=True, expected_total_ron=total)

    def test_rejects_nonfinite_and_nonnumeric_totals(self):
        for total in ({'invalid': True}, [], True, False, None, '74', float('nan'), float('inf'), -1):
            with self.subTest(total=total), self.assertRaises(ValidationError):
                DraculaCheckoutIn.model_validate(self.payload(total))

    def test_accepts_finite_nonnegative_amounts(self):
        for total in (0, 74, 74.25):
            with self.subTest(total=total):
                self.assertEqual(DraculaCheckoutIn.model_validate(self.payload(total)).expected_total_ron, total)

if __name__ == '__main__':
    unittest.main()
