"""Cart boundary regression checks; no server or persistent database required."""
import unittest
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from flask import Flask

from app.api import storefront


class CartQuantityValidationTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(storefront, 'get_settings', return_value=SimpleNamespace(postgres_enabled=True)))
        self.locale = self.stack.enter_context(patch.object(storefront, '_locale', return_value='ro'))
        ctx = SimpleNamespace(session=object(), tenant_id='tenant', tenant_slug='design', user_id=None)
        self.open_ctx = self.stack.enter_context(patch.object(storefront, '_open_ctx', return_value=(object(), ctx)))
        self.stack.enter_context(patch.object(storefront, '_close_ctx'))
        self.repo = MagicMock()
        self.repo.get_or_create.return_value = 'cart'
        self.repo.read.return_value = {'items': []}
        self.stack.enter_context(patch.object(storefront, 'CartRepo', return_value=self.repo))
        self.stack.enter_context(patch.object(storefront, '_resolve', return_value={'id': 'product', 'price_ron': 49}))
        self.stack.enter_context(patch.object(storefront, '_cart_payload', return_value={'items': []}))
        self.stack.enter_context(patch.object(storefront, '_with_cart_cookie', side_effect=lambda response, token: response))
        self.app.add_url_rule('/cart/<action>', view_func=lambda action: storefront._mutate_cart(action, 'product'), methods=['POST'])
        self.client = self.app.test_client()

    def test_invalid_quantities_never_open_database_or_create_cart(self):
        values = ['invalid', -1, 1.5, '1.5', True, False, None, [], {}, 'NaN', '', '-1']
        for action in ('add', 'set'):
            for value in values:
                with self.subTest(action=action, value=value):
                    response = self.client.post('/cart/' + action, json={'qty': value})
                    self.assertEqual(response.status_code, 400)
                    self.assertEqual(response.json['error'], 'invalid_quantity')
        self.locale.assert_not_called()
        self.open_ctx.assert_not_called()
        self.repo.get_or_create.assert_not_called()

    def test_add_default_numeric_string_and_patch_zero(self):
        self.assertEqual(self.client.post('/cart/add', json={}).status_code, 200)
        self.assertEqual(self.repo.add.call_args.args[2], 1)
        self.assertEqual(self.client.post('/cart/add', json={'qty': '3'}).status_code, 200)
        self.assertEqual(self.repo.add.call_args.args[2], 3)
        self.assertEqual(self.client.post('/cart/set', json={'qty': 0}).status_code, 200)
        self.assertEqual(self.repo.set_qty.call_args.args[2], 0)

    def test_zero_add_and_missing_patch_are_rejected(self):
        self.assertEqual(self.client.post('/cart/add', json={'qty': 0}).status_code, 400)
        self.assertEqual(self.client.post('/cart/set', json={}).status_code, 400)
        self.open_ctx.assert_not_called()

    def test_sync_validates_entire_batch_before_writing(self):
        response = self.client.post('/cart/sync', json={'items': [
            {'product_id': 'first', 'qty': 2}, {'product_id': 'second', 'qty': -1},
        ]})
        self.assertEqual(response.status_code, 400)
        self.open_ctx.assert_not_called()
        self.repo.set_qty.assert_not_called()
        self.assertEqual(self.client.post('/cart/sync', json={'items': [
            {'product_id': 'first', 'qty': '2'},
        ]}).status_code, 200)
        self.assertEqual(self.repo.set_qty.call_args.args[2], 2)

    def test_delete_does_not_require_quantity(self):
        self.assertEqual(self.client.post('/cart/remove', json={}).status_code, 200)
        self.repo.remove.assert_called_once_with('cart', 'product')


if __name__ == '__main__':
    unittest.main()
