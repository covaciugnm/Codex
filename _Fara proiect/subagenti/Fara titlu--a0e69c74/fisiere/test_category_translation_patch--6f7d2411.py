"""Regression for category edits; runs against an isolated in-memory database."""
import unittest
from unittest.mock import patch

from sqlalchemy import create_engine, text

from app.api.admin.resources import categories


class CategoryDescriptionPatchTest(unittest.TestCase):
    def test_omitted_description_survives_and_explicit_empty_clears(self):
        engine = create_engine('sqlite://')
        with engine.begin() as session, patch.object(categories, 'LOCALES', ('ro', 'en')):
            session.execute(text("ATTACH DATABASE ':memory:' AS catalog"))
            session.execute(text('''CREATE TABLE catalog.category_translations (
                category_id TEXT, tenant_id TEXT, locale TEXT,
                name TEXT, slug TEXT, description TEXT,
                UNIQUE (category_id, locale))'''))

            def write(names, descriptions):
                categories._write_translations(session, 'tenant', 'category', names, {}, descriptions)

            def descriptions():
                return dict(session.execute(text(
                    'SELECT locale, description FROM catalog.category_translations'
                )).all())

            write({'ro': 'Haine', 'en': 'Clothing'}, {'ro': 'Descriere', 'en': 'Description'})
            # The admin form saves names/slugs without a description field.
            write({'ro': 'Haine noi', 'en': 'New clothing'}, {})
            self.assertEqual(descriptions(), {'ro': 'Descriere', 'en': 'Description'})
            write({'ro': 'Haine noi', 'en': 'New clothing'}, {'ro': 'Actualizata'})
            self.assertEqual(descriptions(), {'ro': 'Actualizata', 'en': 'Description'})
            write({'ro': 'Haine noi', 'en': 'New clothing'}, {'ro': ''})
            self.assertEqual(descriptions(), {'ro': '', 'en': 'Description'})
        engine.dispose()


if __name__ == '__main__':
    unittest.main()
