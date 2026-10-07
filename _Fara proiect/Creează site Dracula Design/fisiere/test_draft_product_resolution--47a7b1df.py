import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from app.api.storefront import _resolve
from app.repositories.tenant_repo import vat_rate

class DraftResolutionTest(unittest.TestCase):
    def test_only_published_products_are_resolved_for_purchase(self):
        for ref in ({'product_id':'11111111-1111-1111-1111-111111111111'}, {'external_id':'concept'}, {'sku':'QA-001'}):
            for status in ('draft','archived','published'):
                product={'id':'product','status':status}
                repo=SimpleNamespace(resolve_product=Mock(return_value=product))
                with self.subTest(ref=ref,status=status):
                    self.assertEqual(_resolve(repo,ref),product if status=='published' else None)
                    self.assertEqual(_resolve(repo,ref,allow_unpublished=True),product)

    def test_explicit_zero_tax_is_preserved(self):
        self.assertEqual(vat_rate({'tax':{'vat_rate':0}}),0)
        self.assertEqual(vat_rate({'tax':{'vat_rate':0.19}}),0.19)
        self.assertEqual(vat_rate({}),0.21)

if __name__=='__main__':unittest.main()
