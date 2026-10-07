"""Import the 17 supplied raisin concepts without publishing or resetting edits.

Run inside the Food migrate container, mounting the Food root at /import:
  python /import/backend/import_raisin_drafts.py --root /import --verify
The product image is attached only after the corresponding public file exists,
and only when an administrator has not already supplied an image.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


REVIEW_NOTES = {
    "ro": "Concept de produs în pregătire. Prețul, gramajul, stocul, ingredientele, alergenii, originea și eticheta finală trebuie confirmate înainte de publicare. Valoarea tehnică 0 din administrare nu reprezintă un preț comercial. Imaginea este o machetă de prezentare.",
    "en": "Product concept in preparation. Price, weight, stock, ingredients, allergens, origin and the final label require confirmation before publication. The administrative placeholder 0 is not a selling price. The image is a presentation mockup.",
    "de": "Produktkonzept in Vorbereitung. Preis, Gewicht, Bestand, Zutaten, Allergene, Herkunft und endgültiges Etikett müssen vor Veröffentlichung bestätigt werden. Der administrative Platzhalter 0 ist kein Verkaufspreis. Das Bild ist ein Präsentationsentwurf.",
}


def protected_fingerprint(session, tenant_id):
    """Opaque hashes, without printing any account or order information."""
    result = {}
    for table in ("identity.users", "identity.admin_users", "sales.orders"):
        where = "" if table == "identity.admin_users" else " WHERE tenant_id=:t"
        rows = session.execute(text(f"SELECT to_jsonb(r)::text FROM {table} r{where} ORDER BY id"), {"t": tenant_id}).scalars().all()
        result[table] = {"count": len(rows), "sha256": hashlib.sha256("\n".join(rows).encode()).hexdigest()}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verify", action="store_true", help="Assert the initial 17-draft / 2-public state.")
    args = parser.parse_args()
    source = json.loads((args.root / "food/raisin-drafts.json").read_text(encoding="utf-8"))
    products = source["products"]
    assert len(products) == 17 and len({p["id"] for p in products}) == 17
    assert [sum(p["category"] == category["id"] for p in products) for category in source["categories"]] == [10, 7]
    assert all(set(p["name"]) >= {"ro", "en", "de"} for p in products)
    engine = create_engine(os.environ["SUPERUSER_DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://"))
    report = {"inserted_products": 0, "attached_images": 0, "pending_images": [], "preserved_existing_images": []}
    with Session(engine) as session, session.begin():
        tenant_id = session.execute(text("SELECT id FROM core.tenants WHERE slug=:s"), {"s": os.environ.get("DEFAULT_TENANT", "dracula-food")}).scalar_one()
        # Serializes this importer; no seed routine or account mutations occur.
        session.execute(text("SELECT pg_advisory_xact_lock(hashtext('dracula-food-raisin-import'))"))
        before = protected_fingerprint(session, tenant_id)
        categories = {}
        for position, category in enumerate(source["categories"], 3):
            params = {"t": tenant_id, "code": category["id"], "position": position}
            session.execute(text("INSERT INTO catalog.categories(tenant_id,external_id,position) VALUES(:t,:code,:position) ON CONFLICT DO NOTHING"), params)
            category_id = session.execute(text("SELECT id FROM catalog.categories WHERE tenant_id=:t AND external_id=:code"), params).scalar_one()
            categories[category["id"]] = category_id
            for locale, name in category["name"].items():
                session.execute(text("INSERT INTO catalog.category_translations(category_id,tenant_id,locale,name,slug) VALUES(:c,:t,:l,:n,:s) ON CONFLICT DO NOTHING"), {"c": category_id, "t": tenant_id, "l": locale, "n": name, "s": category["id"]})
        product_ids = []
        for sequence, product in enumerate(products, 3):
            params = {"t": tenant_id, "ext": product["id"], "sku": f"DF-{sequence:03d}", "cat": categories[product["category"]]}
            inserted = session.execute(text("""INSERT INTO catalog.products(tenant_id,external_id,sku,status,currency,price_ron,manage_stock,stock_quantity,is_in_stock,needs_price_review,primary_category_id)
                VALUES(:t,:ext,:sku,'draft','RON',0,true,0,false,true,:cat)
                ON CONFLICT DO NOTHING RETURNING id"""), params).scalar_one_or_none()
            report["inserted_products"] += int(inserted is not None)
            row = session.execute(text("SELECT id, primary_category_id FROM catalog.products WHERE tenant_id=:t AND external_id=:ext"), params).one()
            product_id = row.id
            product_ids.append(product_id)
            for locale in ("ro", "en", "de"):
                description = product["description"][locale]
                session.execute(text("""INSERT INTO catalog.product_translations(product_id,tenant_id,locale,name,slug,short_description,description,seo_title,seo_description,translation_status)
                    VALUES(:p,:t,:l,:n,:s,:short,:body,:title,:short,'manual') ON CONFLICT DO NOTHING"""),
                    {"p": product_id, "t": tenant_id, "l": locale, "n": product["name"][locale], "s": product["id"], "short": description,
                     "body": description + "\n\n" + REVIEW_NOTES[locale], "title": product["name"][locale] + " — Dracula Food"})
            # A rerun must not reintroduce an admin-deleted or changed category.
            if inserted is not None:
                session.execute(text("INSERT INTO catalog.product_categories(product_id,category_id,tenant_id,is_primary) VALUES(:p,:c,:t,true) ON CONFLICT DO NOTHING"), {"p": product_id, "c": params["cat"], "t": tenant_id})
            filename = product["image_brief"]["proposed_filename"]
            if Path(filename).name != filename:
                raise ValueError("Image filenames must not contain directories")
            image_path = args.root / "backend/public/assets/produse" / filename
            if not image_path.is_file() or image_path.stat().st_size == 0:
                report["pending_images"].append(filename)
                continue
            has_image = session.execute(text("SELECT EXISTS(SELECT 1 FROM catalog.product_images WHERE tenant_id=:t AND product_id=:p)"), {"t": tenant_id, "p": product_id}).scalar_one()
            if has_image:
                report["preserved_existing_images"].append(product["id"])
                continue
            session.execute(text("""INSERT INTO catalog.product_images(product_id,tenant_id,source_url,position,alt,checksum)
                VALUES(:p,:t,:url,0,CAST(:alt AS jsonb),:checksum) ON CONFLICT DO NOTHING"""),
                {"p": product_id, "t": tenant_id, "url": "/assets/produse/" + filename, "alt": json.dumps(product["name"], ensure_ascii=False),
                 "checksum": hashlib.sha256(image_path.read_bytes()).hexdigest()})
            report["attached_images"] += 1
        after = protected_fingerprint(session, tenant_id)
        assert before == after, "Account or order data changed during import; transaction rolled back"
        report["accounts_and_orders_unchanged"] = True
        report["protected_row_counts"] = {k: v["count"] for k, v in after.items()}
        report["catalog_status"] = dict(session.execute(text("SELECT status,count(*) FROM catalog.products WHERE tenant_id=:t GROUP BY status"), {"t": tenant_id}).all())
        report["raisin_translations"] = session.execute(text("SELECT count(*) FROM catalog.product_translations WHERE tenant_id=:t AND product_id=ANY(:ids) AND locale IN ('ro','en','de')"), {"t": tenant_id, "ids": product_ids}).scalar_one()
        report["raisin_categories"] = dict(session.execute(text("SELECT c.external_id,count(*) FROM catalog.products p JOIN catalog.categories c ON c.id=p.primary_category_id WHERE p.tenant_id=:t AND p.id=ANY(:ids) GROUP BY c.external_id"), {"t": tenant_id, "ids": product_ids}).all())
        if args.verify:
            assert report["catalog_status"] == {"draft": 17, "published": 2}, report["catalog_status"]
            assert report["raisin_translations"] == 51
            assert report["raisin_categories"] == {"stafide-naturale": 10, "stafide-aromatizate": 7}
            ready = session.execute(text("SELECT count(*) FROM catalog.products WHERE tenant_id=:t AND id=ANY(:ids) AND status='draft' AND needs_price_review AND price_ron=0 AND stock_quantity=0 AND NOT is_in_stock"), {"t": tenant_id, "ids": product_ids}).scalar_one()
            assert ready == 17
    engine.dispose()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
