"""Tests of live-launch protection; synthetic data never reaches the database."""
import copy
import unittest
from app.commerce_readiness import validate_readiness


def fixture():
    cfg = {'tenant': 'dracula-design', 'currency': 'RON',
           'legal': {'company_name': 'Synthetic', 'cui': 'TEST', 'registration': 'TEST',
                     'address': 'Test address', 'phone': '000', 'email': 'test@example.invalid', 'website': 'https://example.invalid'},
           'seller': {'legal_name': 'Synthetic', 'address': 'Test address'},
           'tax': {'vat_rate': 0, 'prices_include_vat': True, 'requires_review': False},
           'shipping_rules': {'countries': ['RO'], 'rules': [{'country': 'RO', 'price_ron': 0}],
                              'delivery_methods': [{'code': 'courier'}], 'payment_methods': [{'code': 'cash_on_delivery'}]},
           'settings': {'demo_prices': False, 'commerce_approval': {
               'legal_pages_confirmed': True, 'shipping_confirmed': True, 'tax_confirmed': True,
               'payments_confirmed': True, 'products': {'TEST': {
                   'confirmed_price_ron': 10, 'stock_confirmed': True, 'content_confirmed': True}}}}}
    products = [{'sku': 'TEST', 'price_ron': 10, 'stock_quantity': 0, 'manage_stock': True, 'needs_price_review': False}]
    return cfg, products, {'COMMERCE_MODE': 'live', 'COMMERCE_READY': 'true'}


class ReadinessTests(unittest.TestCase):
    def test_complete_cash_on_delivery_can_pass_without_card_credentials(self):
        self.assertTrue(validate_readiness(*fixture())['ready'])

    def test_activation_flag_does_not_bypass_missing_data(self):
        cfg, products, env = fixture()
        cfg['legal']['cui'] = ''
        self.assertFalse(validate_readiness(cfg, products, env)['ready'])

    def test_price_change_requires_new_confirmation(self):
        cfg, products, env = fixture()
        products[0]['price_ron'] = 11
        self.assertFalse(validate_readiness(cfg, products, env)['ready'])

    def test_zero_confirmed_tax_is_valid(self):
        cfg, products, env = fixture()
        self.assertEqual(cfg['tax']['vat_rate'], 0)
        self.assertTrue(validate_readiness(cfg, products, env)['ready'])

    def test_demo_inventory_cannot_be_silently_used(self):
        cfg, products, env = fixture()
        cfg['settings']['commerce_approval']['products']['TEST']['stock_confirmed'] = False
        self.assertFalse(validate_readiness(cfg, products, env)['ready'])

    def test_food_requires_information_confirmation(self):
        cfg, products, env = fixture()
        cfg['tenant'] = 'dracula-food'
        self.assertFalse(validate_readiness(cfg, products, env)['ready'])
        cfg['settings']['commerce_approval']['products']['TEST']['food_information_confirmed'] = True
        self.assertTrue(validate_readiness(cfg, products, env)['ready'])

    def test_card_test_key_is_rejected_and_never_returned(self):
        cfg, products, env = fixture()
        env.update(STRIPE_ENABLED='true', STRIPE_SECRET_KEY='sk_test_never_report_this')
        report = validate_readiness(cfg, products, env)
        self.assertFalse(report['ready'])
        self.assertNotIn('never_report_this', str(report))

    def test_nonfinite_or_negative_values_are_rejected(self):
        for value in [float('nan'), float('inf'), -1, None, 'garbage']:
            cfg, products, env = fixture()
            products[0]['price_ron'] = value
            self.assertFalse(validate_readiness(cfg, products, env)['ready'])


if __name__ == '__main__':
    unittest.main()
