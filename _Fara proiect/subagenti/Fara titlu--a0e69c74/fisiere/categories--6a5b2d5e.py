"""Categorii: arbore + CRUD, cu nume/slug/descriere pe 6 limbi."""
from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify
from pydantic import BaseModel, Field
from sqlalchemy import text

from ...errors import ApiError
from ..deps import pagination, require_role, tenant_db
from ._common import (
    DEFAULT_LOCALE,
    LOCALES,
    arg_locale,
    arg_str,
    clean_translated,
    invalidate_catalog_cache,
    listing,
    not_found,
    patch_fields,
    slugify,
    validate,
)


class CategoryIn(BaseModel):
    external_id: str | None = None
    parent_id: str | None = None
    position: int = 0
    is_active: bool = True
    name: dict[str, str] = Field(default_factory=dict)
    slug: dict[str, str] = Field(default_factory=dict)
    description: dict[str, str] = Field(default_factory=dict)


class CategoryPatch(BaseModel):
    parent_id: str | None = None
    position: int | None = None
    is_active: bool | None = None
    name: dict[str, str] | None = None
    slug: dict[str, str] | None = None
    description: dict[str, str] | None = None
    # taxonomia Google (null = fără mapare)
    google_category_id: int | None = None


# Admin totals include every directly assigned product, regardless of status,
# and count secondary memberships too. The stored counter can become stale.
_CATEGORY_SELECT = """
    SELECT c.id, c.external_id, c.parent_id, c.path, c.position,
           (SELECT count(DISTINCT pc.product_id)
              FROM catalog.product_categories pc
              JOIN catalog.products p ON p.id = pc.product_id
                                     AND p.tenant_id = c.tenant_id
             WHERE pc.category_id = c.id AND pc.tenant_id = c.tenant_id
           ) AS product_count,
           c.is_active, c.google_category_id
      FROM catalog.categories c
"""


def _serialize(row: Any, translations: dict[str, dict[str, str]]) -> dict[str, Any]:
    names = {loc: values.get("name", "") for loc, values in translations.items()}
    slugs = {loc: values.get("slug", "") for loc, values in translations.items()}
    descriptions = {loc: values.get("description", "") for loc, values in translations.items()}
    return {
        "id": str(row.id),
        "external_id": row.external_id,
        "parent_id": str(row.parent_id) if row.parent_id else None,
        "path": row.path,
        "position": int(row.position or 0),
        "product_count": int(row.product_count or 0),
        "is_active": bool(row.is_active),
        "google_category_id": getattr(row, "google_category_id", None),
        "name": names,
        "slug": slugs,
        "description": descriptions,
    }


def _translations_for(session: Any, category_ids: list[str]) -> dict[str, dict[str, dict[str, str]]]:
    if not category_ids:
        return {}
    rows = session.execute(
        text(
            """
            SELECT category_id, locale, name, slug, description
              FROM catalog.category_translations
             WHERE category_id = ANY(CAST(:ids AS uuid[]))
            """
        ),
        {"ids": category_ids},
    ).all()
    out: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        if row.locale not in LOCALES:
            continue
        out.setdefault(str(row.category_id), {})[row.locale] = {
            "name": row.name or "",
            "slug": row.slug or "",
            "description": row.description or "",
        }
    return out


def _write_translations(session: Any, tenant_id: str, category_id: str,
                        name: dict[str, str], slug: dict[str, str],
                        description: dict[str, str]) -> None:
    locales = set(name) | set(slug) | set(description)
    for locale in sorted(locales & set(LOCALES)):
        value_name = name.get(locale, "")
        value_slug = slug.get(locale) or (slugify(value_name) if value_name else "")
        session.execute(
            text(
                """
                INSERT INTO catalog.category_translations
                       (category_id, tenant_id, locale, name, slug, description)
                VALUES (:cid, :t, :locale, :name, :slug, :description)
                ON CONFLICT (category_id, locale) DO UPDATE SET
                       name = EXCLUDED.name,
                       slug = COALESCE(NULLIF(EXCLUDED.slug, ''),
                                       catalog.category_translations.slug),
                       description = CASE WHEN :write_description
                           THEN EXCLUDED.description
                           ELSE catalog.category_translations.description END
                """
            ),
            {
                "cid": category_id,
                "t": tenant_id,
                "locale": locale,
                "name": value_name,
                "slug": value_slug,
                "description": description.get(locale, ""),
                "write_description": locale in description,
            },
        )


def register(bp: Blueprint) -> None:

    @bp.get("/categories")
    @require_role("viewer")
    def list_categories():
        """`?tree=1` întoarce arborele; altfel lista plată paginată."""
        page, per_page = pagination()
        as_tree = arg_str("tree") in {"1", "true", "yes"}
        locale = arg_locale()
        # A3: `?active=1` → doar active, `?active=0` → doar dezactivate
        active = arg_str("active").lower()
        active_sql = (" AND is_active" if active in {"1", "true", "yes"}
                      else " AND NOT is_active" if active in {"0", "false", "no"} else "")
        with tenant_db() as (session, tenant_id, slug):
            total = session.execute(
                text("SELECT count(*) FROM catalog.categories WHERE tenant_id = :t" + active_sql),
                {"t": tenant_id},
            ).scalar() or 0
            sql = _CATEGORY_SELECT + f"""
                 WHERE c.tenant_id = :t{active_sql}
                 ORDER BY c.path, c.position
            """
            params: dict[str, Any] = {"t": tenant_id}
            if not as_tree:
                sql += " LIMIT :limit OFFSET :offset"
                params.update({"limit": per_page, "offset": (page - 1) * per_page})
            rows = session.execute(text(sql), params).all()
            translations = _translations_for(session, [str(r.id) for r in rows])
            items = [_serialize(row, translations.get(str(row.id), {})) for row in rows]

        for item in items:
            item["label"] = item["name"].get(locale) or item["name"].get(DEFAULT_LOCALE) or ""
        if not as_tree:
            return jsonify(listing(items, total, page, per_page))

        by_id = {item["id"]: {**item, "children": []} for item in items}
        roots: list[dict[str, Any]] = []
        for item in by_id.values():
            parent = by_id.get(item["parent_id"] or "")
            (parent["children"] if parent else roots).append(item)
        return jsonify({"items": roots, "total": len(items), "page": 1, "per_page": len(items)})

    @bp.put("/categories/order")
    @bp.post("/categories/order")
    @require_role("editor")
    def reorder_categories():
        """`{items:[{id, parent_id?, position}]}` sau `{order:[id,...]}`."""
        from ._common import json_body

        body = json_body()
        items = body.get("items")
        if not isinstance(items, list):
            order = body.get("order")
            if not isinstance(order, list) or not order:
                raise ApiError("Trimite `items` sau `order`", code="validation_failed",
                               status=400, details={"items": ["Listă obligatorie"]})
            items = [{"id": cid, "position": index} for index, cid in enumerate(order)]
        with tenant_db("editor") as (session, tenant_id, slug):
            for item in items:
                if not isinstance(item, dict) or not item.get("id"):
                    continue
                sets = ["position = :position"]
                params = {"position": int(item.get("position") or 0),
                          "cid": item["id"], "t": tenant_id}
                if "parent_id" in item:
                    sets.append("parent_id = CAST(:parent AS uuid)")
                    params["parent"] = item.get("parent_id") or None
                session.execute(
                    text(
                        f"""
                        UPDATE catalog.categories SET {', '.join(sets)}, updated_at = now()
                         WHERE id = CAST(:cid AS uuid) AND tenant_id = :t
                        """
                    ),
                    params,
                )
        invalidate_catalog_cache(slug)
        return jsonify({"status": "ok", "count": len(items)})

    @bp.get("/categories/<category_id>")
    @require_role("viewer")
    def get_category(category_id: str):
        with tenant_db() as (session, tenant_id, slug):
            row = session.execute(
                text(
                    _CATEGORY_SELECT + " WHERE c.id = CAST(:cid AS uuid)"
                ),
                {"cid": category_id},
            ).first()
            if row is None:
                raise not_found("Categorie inexistentă")
            translations = _translations_for(session, [category_id])
            from ....google_taxonomy import describe

            payload = _serialize(row, translations.get(category_id, {}))
            payload["google_category"] = describe(session, row.google_category_id,
                                                  arg_locale())
            return jsonify(payload)

    @bp.get("/google-taxonomy")
    @require_role("viewer")
    def google_taxonomy_search():
        """Căutare în taxonomia Google (selector în editorul de produs / categorie).
        `?q=` text sau ID, `?lang=` (implicit ro), `?limit=` (max 100)."""
        from ....google_taxonomy import search

        with tenant_db() as (session, tenant_id, slug):
            items = search(session, arg_str("q"), arg_str("lang") or "ro",
                           int(arg_str("limit") or 30))
        return jsonify({"items": items, "version": "2021-09-21"})

    @bp.post("/categories")
    @require_role("editor")
    def create_category():
        body = validate(CategoryIn)
        name = clean_translated(body.name)
        if not name.get(DEFAULT_LOCALE):
            raise ApiError("Numele în română este obligatoriu", code="validation_failed",
                           status=400, details={"name.ro": ["Câmp obligatoriu"]})
        with tenant_db("editor") as (session, tenant_id, slug):
            external_id = body.external_id or slugify(name[DEFAULT_LOCALE])
            parent_path = ""
            if body.parent_id:
                parent_path = session.execute(
                    text("SELECT path FROM catalog.categories WHERE id = CAST(:p AS uuid)"),
                    {"p": body.parent_id},
                ).scalar() or ""
                if not parent_path:
                    raise not_found("Categoria părinte nu există")
            path = f"{parent_path}/{external_id}".strip("/")
            category_id = str(
                session.execute(
                    text(
                        """
                        INSERT INTO catalog.categories
                               (tenant_id, external_id, parent_id, path, position, is_active)
                        VALUES (:t, :external_id, CAST(:parent AS uuid), :path, :position, :active)
                        RETURNING id
                        """
                    ),
                    {
                        "t": tenant_id,
                        "external_id": external_id,
                        "parent": body.parent_id,
                        "path": path,
                        "position": body.position,
                        "active": body.is_active,
                    },
                ).scalar()
            )
            _write_translations(session, tenant_id, category_id, name,
                                clean_translated(body.slug), clean_translated(body.description))
            row = session.execute(
                text(
                    _CATEGORY_SELECT + " WHERE c.id = CAST(:cid AS uuid)"
                ),
                {"cid": category_id},
            ).first()
            payload = _serialize(row, _translations_for(session, [category_id]).get(category_id, {}))
        invalidate_catalog_cache(slug)
        return jsonify(payload), 201

    def _update(category_id: str):
        body = validate(CategoryPatch)
        fields = patch_fields(body)
        if not fields:
            raise ApiError("Nimic de actualizat", code="bad_request", status=400)
        with tenant_db("editor") as (session, tenant_id, slug):
            exists = session.execute(
                text("SELECT id FROM catalog.categories WHERE id = CAST(:cid AS uuid)"),
                {"cid": category_id},
            ).scalar()
            if not exists:
                raise not_found("Categorie inexistentă")
            sets, params = [], {"cid": category_id}
            if "parent_id" in fields:
                sets.append("parent_id = CAST(:parent AS uuid)")
                params["parent"] = fields["parent_id"]
            if "position" in fields:
                sets.append("position = :position")
                params["position"] = fields["position"]
            if "is_active" in fields:
                sets.append("is_active = :active")
                params["active"] = fields["is_active"]
            if "google_category_id" in fields:
                from ....google_taxonomy import exists as _gt_exists

                if fields["google_category_id"] is not None and not _gt_exists(
                        session, fields["google_category_id"]):
                    raise ApiError("ID inexistent în taxonomia Google",
                                   code="validation_failed", status=400,
                                   details={"google_category_id": ["ID Google necunoscut"]})
                sets.append("google_category_id = :gcat")
                params["gcat"] = fields["google_category_id"]
            if sets:
                session.execute(
                    text(
                        f"UPDATE catalog.categories SET {', '.join(sets)}, updated_at = now()"
                        " WHERE id = CAST(:cid AS uuid)"
                    ),
                    params,
                )
            if any(k in fields for k in ("name", "slug", "description")):
                _write_translations(
                    session, tenant_id, category_id,
                    clean_translated(fields.get("name") or {}),
                    clean_translated(fields.get("slug") or {}),
                    clean_translated(fields.get("description") or {}),
                )
            row = session.execute(
                text(
                    _CATEGORY_SELECT + " WHERE c.id = CAST(:cid AS uuid)"
                ),
                {"cid": category_id},
            ).first()
            payload = _serialize(row, _translations_for(session, [category_id]).get(category_id, {}))
        invalidate_catalog_cache(slug)
        return jsonify(payload)

    @bp.patch("/categories/<category_id>")
    @require_role("editor")
    def patch_category(category_id: str):
        return _update(category_id)

    @bp.put("/categories/<category_id>")
    @require_role("editor")
    def put_category(category_id: str):
        return _update(category_id)

    @bp.delete("/categories/<category_id>")
    @require_role("editor")
    def delete_category(category_id: str):
        """Dezactivare logică; refuz dacă are subcategorii active.

        `?hard=1` (owner): ştergere definitivă, cu regulile din `POST /categories/bulk`."""
        from . import bulk

        if bulk.wants_hard():
            return bulk.hard_delete_one("categories", category_id)
        with tenant_db("editor") as (session, tenant_id, slug):
            children = session.execute(
                text(
                    """
                    SELECT count(*) FROM catalog.categories
                     WHERE parent_id = CAST(:cid AS uuid) AND is_active
                    """
                ),
                {"cid": category_id},
            ).scalar() or 0
            if children:
                raise ApiError(f"Categoria are {children} subcategorii active",
                               code="conflict", status=409)
            updated = session.execute(
                text(
                    """
                    UPDATE catalog.categories SET is_active = false, updated_at = now()
                     WHERE id = CAST(:cid AS uuid) RETURNING id
                    """
                ),
                {"cid": category_id},
            ).scalar()
            if updated is None:
                raise not_found("Categorie inexistentă")
        invalidate_catalog_cache(slug)
        return jsonify({"status": "ok", "id": category_id, "deleted": "soft"})
