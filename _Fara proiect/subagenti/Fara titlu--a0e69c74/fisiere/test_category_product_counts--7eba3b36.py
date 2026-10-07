"""Admin category totals follow live product memberships, not cached counters."""
import unittest

from sqlalchemy import create_engine, text

from app.api.admin.resources.categories import _CATEGORY_SELECT


class CategoryProductCountsTest(unittest.TestCase):
    def test_counts_all_statuses_and_secondary_memberships_per_tenant(self):
        engine = create_engine('sqlite://')
        with engine.begin() as session:
            session.execute(text("ATTACH DATABASE ':memory:' AS catalog"))
            session.execute(text('''CREATE TABLE catalog.categories (
                id TEXT, tenant_id TEXT, external_id TEXT, parent_id TEXT,
                path TEXT, position INTEGER, product_count INTEGER,
                is_active BOOLEAN, google_category_id INTEGER)'''))
            session.execute(text('''CREATE TABLE catalog.products (
                id TEXT, tenant_id TEXT, status TEXT)'''))
            session.execute(text('''CREATE TABLE catalog.product_categories (
                product_id TEXT, category_id TEXT, tenant_id TEXT, is_primary BOOLEAN)'''))
            for category in ('business', 'accessories', 'empty'):
                session.execute(text('''INSERT INTO catalog.categories
                    (id, tenant_id, external_id, path, position, product_count, is_active)
                    VALUES (:id, 'design', :id, :id, 0, 999, 1)'''), {'id': category})
            session.execute(text('''INSERT INTO catalog.products VALUES
                ('published', 'design', 'published'),
                ('draft', 'design', 'draft'),
                ('archived', 'design', 'archived'),
                ('foreign', 'food', 'published')'''))
            session.execute(text('''INSERT INTO catalog.product_categories VALUES
                ('published', 'business', 'design', 1),
                ('published', 'accessories', 'design', 0),
                ('draft', 'accessories', 'design', 1),
                ('archived', 'accessories', 'design', 1),
                ('foreign', 'accessories', 'food', 1)'''))

            def counts():
                return {row.id: row.product_count for row in session.execute(text(
                    _CATEGORY_SELECT + ' WHERE c.tenant_id = :tenant'
                ), {'tenant': 'design'})}

            self.assertEqual(counts(), {'business': 1, 'accessories': 3, 'empty': 0})
            # Membership edits are reflected immediately without reseeding counters.
            session.execute(text('''DELETE FROM catalog.product_categories
                WHERE product_id = 'draft' AND category_id = 'accessories' '''))
            self.assertEqual(counts(), {'business': 1, 'accessories': 2, 'empty': 0})
        engine.dispose()


if __name__ == '__main__':
    unittest.main()
