import { zodResolver } from '@hookform/resolvers/zod';
import { useQuery } from '@tanstack/react-query';
import { useMemo, useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import * as productsApi from '../../api/products';
import * as settingsApi from '../../api/settings';
import {
  LanguageTabs,
  RichTextEditor,
  SelectField,
  Tabs,
  TextAreaField,
  TextField,
  useToast,
  type TabDef,
} from '../../components';
import { DEFAULT_LANGUAGE, LANGUAGES, type Language, type Product, type ProductImage, type ProductPatch } from '../../types';
import { useOpenApp } from '../../shell/useOpenApp';
import { useWarehouseFocus, useWarehouseSettings } from '../warehouse/useWarehouse';
import ProductImages from './ProductImages';
import { productSchema, type ProductFormValues } from './productSchema';
import './products.css';
import '../warehouse/warehouse.css';

export interface ProductEditorProps {
  product?: Product;
  onSaved?: (product: Product) => void;
  onCancel?: () => void;
  /** Valori inițiale pentru un produs NOU (ex. „Creează piesă draft” din Warehouse). */
  draftDefaults?: { name: string; status: ProductFormValues['status'] };
}

function emptyTranslations(): ProductFormValues['translations'] {
  return Object.fromEntries(
    LANGUAGES.map((l) => [l, { name: '', slug: '', short_description: '', description: '', seo_title: '', seo_description: '' }]),
  ) as ProductFormValues['translations'];
}

function toDefaults(product?: Product): ProductFormValues {
  const translations = emptyTranslations();
  for (const lang of LANGUAGES) {
    // `?.` pe `translations`: la deschiderea din lista, produsul vine in forma de
    // listare, care are `name` plat si NU are `translations` (crapa altfel pe `.ro`).
    const source = product?.translations?.[lang];
    if (source) translations[lang] = { ...translations[lang], ...source };
  }
  if (!translations[DEFAULT_LANGUAGE].name && product?.name) {
    translations[DEFAULT_LANGUAGE].name = product.name;
  }
  return {
    sku: product?.sku ?? '',
    ean: product?.ean ?? '',
    translations,
    price_ron: product?.price_ron ?? 0,
    regular_price_ron: product?.regular_price_ron ?? 0,
    on_sale: product?.on_sale ?? false,
    vat_rate: product?.vat_rate ?? 21,
    stock_quantity: product?.stock_quantity ?? 0,
    manage_stock: product?.manage_stock ?? true,
    is_in_stock: product?.is_in_stock ?? true,
    status: product?.status ?? 'draft',
    category_ids: product?.category_ids ?? [],
    weight_kg: (product?.weight_kg ?? '') as unknown as number,
    length_cm: (product?.length_cm ?? '') as unknown as number,
    width_cm: (product?.width_cm ?? '') as unknown as number,
    height_cm: (product?.height_cm ?? '') as unknown as number,
    packaging: product?.packaging ?? '',
  };
}

/** Editor complet de produs: 6 tab-uri, continut localizat ×6 limbi, imagini ordonabile. */
export function ProductEditor({ product, onSaved, onCancel, draftDefaults }: ProductEditorProps) {
  const { t } = useTranslation();
  const toast = useToast();
  const [tab, setTab] = useState('general');
  const [lang, setLang] = useState<Language>(DEFAULT_LANGUAGE);
  const [images, setImages] = useState<ProductImage[]>(product?.images ?? []);

  /* Cota de TVA e a magazinului (`settings.vat_rate`), nu a produsului: storefrontul
     o ia din `core.tenant_settings.tax`. Randurile din catalog au ramas pe 19 de la
     import si induceau in eroare, asa ca aici o aratam doar, read-only. */
  const { data: shopSettings } = useQuery({ queryKey: ['settings'], queryFn: settingsApi.getSettings });
  const shopVatPercent = shopSettings ? Math.round(Number(shopSettings.vat_rate) * 100) : null;

  /* Warehouse (§6.14): cu modul pornit stocul se administrează doar din Warehouse; seturile
     `assembly` au stoc derivat din piese chiar și în simulare. */
  const { isWarehouse } = useWarehouseSettings();
  const isAssembly = product?.stock_source === 'assembly';
  const stockLocked = isWarehouse || isAssembly;
  const openApp = useOpenApp();
  const requestWarehouse = useWarehouseFocus((s) => s.request);
  const openInWarehouse = () => {
    if (!product) return;
    requestWarehouse(isAssembly ? { tab: 'sets', setId: product.id } : { tab: 'products', q: product.sku });
    openApp('warehouse');
  };

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => productsApi.listAllCategories(),
  });

  const {
    register,
    control,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting, dirtyFields },
  } = useForm<ProductFormValues>({
    resolver: zodResolver(productSchema),
    defaultValues: (() => {
      const d = toDefaults(product);
      if (!product && draftDefaults) {
        d.status = draftDefaults.status;
        d.translations[DEFAULT_LANGUAGE].name = draftDefaults.name;
      }
      return d;
    })(),
  });

  const translations = watch('translations');
  const missingLangs = useMemo(
    () => LANGUAGES.filter((l) => !(translations?.[l]?.name ?? '').trim()),
    [translations],
  );

  const tabs: TabDef[] = [
    { id: 'general', label: t('products.tab_general') },
    { id: 'content', label: t('products.tab_content'), badge: missingLangs.length || undefined },
    { id: 'pricing', label: t('products.tab_pricing') },
    { id: 'images', label: t('products.tab_images'), badge: images.length || undefined },
    { id: 'categories', label: t('products.tab_categories') },
    { id: 'seo', label: t('products.tab_seo') },
  ];

  const submit = handleSubmit(async (values) => {
    // PATCH partial: trimitem doar ce s-a schimbat (P2 §4.3).
    const patch: ProductPatch = {};
    const changed = dirtyFields as Record<string, unknown>;
    if (changed.sku) patch.sku = values.sku;
    if (changed.ean) patch.ean = values.ean || null;
    if (changed.price_ron) patch.price_ron = Number(values.price_ron);
    if (changed.regular_price_ron) patch.regular_price_ron = Number(values.regular_price_ron) || null;
    if (changed.on_sale) patch.on_sale = values.on_sale;
    if (!stockLocked) {
      if (changed.stock_quantity) patch.stock_quantity = Number(values.stock_quantity);
      if (changed.manage_stock) patch.manage_stock = values.manage_stock;
      if (changed.is_in_stock) patch.is_in_stock = values.is_in_stock;
    }
    if (changed.status) patch.status = values.status;
    if (changed.category_ids) patch.category_ids = values.category_ids;
    for (const key of ['weight_kg', 'length_cm', 'width_cm', 'height_cm'] as const) {
      if (changed[key]) patch[key] = values[key] === undefined || values[key] === ('' as unknown) ? null : Number(values[key]);
    }
    if (changed.packaging) patch.packaging = (values.packaging || null) as ProductPatch['packaging'];
    if (changed.translations) {
      patch.translations = Object.fromEntries(
        LANGUAGES.filter((l) => (values.translations[l]?.name ?? '').trim() || l === DEFAULT_LANGUAGE).map((l) => [
          l,
          { ...values.translations[l], name: values.translations[l]?.name ?? '' },
        ]),
      );
    }

    /* Erorile serverului (409 modificat intre timp, 400 validare) se arata; inainte
       promisiunea respinsa se pierdea si butonul parea ca nu face nimic. */
    try {
      const saved = product
        ? await productsApi.updateProduct(product.id, patch, product.updated_at)
        : await productsApi.createProduct({
            ...patch,
            sku: values.sku,
            status: values.status,
            translations: patch.translations ?? Object.fromEntries(
              LANGUAGES.filter((l) => (values.translations[l]?.name ?? '').trim()).map((l) => [l, { ...values.translations[l], name: values.translations[l]?.name ?? '' }]),
            ),
          });
      toast.success(t('app.save_ok'));
      onSaved?.(saved);
    } catch (error) {
      const err = error as { status?: number; code?: string; message?: string; details?: Record<string, string[]> };
      const first = err?.details ? Object.values(err.details)[0]?.[0] : undefined;
      if (err?.code === 'stock_managed_by_warehouse') {
        toast.error(t('warehouse.product_editor.conflict_managed'));
        return;
      }
      toast.error(err?.status === 409 ? t('products.conflict') : first || err?.message || t('common.error'));
    }
  }, () => {
    /* Validare esuata pe un tab ascuns (ex. numele RO in „Descrieri"): spunem unde. */
    toast.error(t('products.fix_errors'));
  });

  return (
    <form onSubmit={submit} noValidate className="prodform" data-testid="product-editor">
      <Tabs tabs={tabs} value={tab} onChange={setTab} />

      {tab === 'general' && (
        <div className="field-row">
          <TextField
            id="sku"
            label={t('fields.sku')}
            required
            error={errors.sku ? t(errors.sku.message as string) : undefined}
            {...register('sku')}
          />
          <TextField id="ean" label={t('fields.ean')} error={errors.ean ? t(errors.ean.message as string) : undefined} {...register('ean')} />
          <SelectField
            id="status"
            label={t('fields.status')}
            options={[
              { value: 'draft', label: t('status.draft') },
              { value: 'published', label: t('status.published') },
              { value: 'archived', label: t('status.archived') },
            ]}
            {...register('status')}
          />
        </div>
      )}

      {tab === 'content' && (
        <>
          <LanguageTabs value={lang} onChange={setLang} missing={missingLangs} />
          <TextField
            id={`name-${lang}`}
            label={`${t('fields.name')} (${lang.toUpperCase()})`}
            required={lang === DEFAULT_LANGUAGE}
            error={
              lang === DEFAULT_LANGUAGE && errors.translations?.ro?.name
                ? t(errors.translations.ro.name.message as string)
                : undefined
            }
            {...register(`translations.${lang}.name` as const)}
          />
          <TextField id={`slug-${lang}`} label={`${t('fields.slug')} (${lang.toUpperCase()})`} {...register(`translations.${lang}.slug` as const)} />
          <TextAreaField
            id={`short-${lang}`}
            label={`${t('fields.short_description')} (${lang.toUpperCase()})`}
            {...register(`translations.${lang}.short_description` as const)}
          />
          <label className="field__label">{`${t('fields.description')} (${lang.toUpperCase()})`}</label>
          <Controller
            control={control}
            name={`translations.${lang}.description` as const}
            render={({ field }) => <RichTextEditor value={field.value ?? ''} onChange={field.onChange} />}
          />
        </>
      )}

      {tab === 'pricing' && (
        <>
          <div className="field-row">
            <TextField
              id="price_ron"
              data-testid="product-price"
              label={`${t('fields.price')} (RON)`}
              type="number"
              step="0.01"
              required
              error={errors.price_ron ? t(errors.price_ron.message as string) : undefined}
              {...register('price_ron')}
            />
            <TextField id="regular_price_ron" label={`${t('fields.regular_price')} (RON)`} type="number" step="0.01" {...register('regular_price_ron')} />
            <div className="field" data-testid="product-vat-readonly">
              <span className="field__label">{t('fields.vat_rate')}</span>
              <p className="field__static">
                {shopVatPercent === null ? '…' : t('products.vat_from_settings', { rate: shopVatPercent })}
              </p>
            </div>
          </div>
          <div className="field-row">
            {stockLocked ? (
              <div className="field" data-testid="product-stock-readonly">
                <span className="field__label">{t('fields.stock_quantity')} <span className="badge">{t('warehouse.product_editor.badge')}</span></span>
                <div className="wh-readonly-stock">
                  <strong>
                    {isAssembly
                      ? t('warehouse.product_editor.derived', {
                          n: product?.stock_quantity ?? 0,
                          name: product?.limiting_component?.name ?? t('common.none'),
                        })
                      : product?.stock_quantity ?? 0}
                  </strong>
                  <span>{t('warehouse.product_editor.managed')}</span>
                  {product && (
                    <button type="button" className="btn btn--link" data-testid="product-stock-open-warehouse" onClick={openInWarehouse}>
                      {t('warehouse.product_editor.open')}
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <TextField
                id="stock_quantity"
                label={t('fields.stock_quantity')}
                type="number"
                error={errors.stock_quantity ? t(errors.stock_quantity.message as string) : undefined}
                {...register('stock_quantity')}
              />
            )}
          </div>
          <fieldset className="prodform__shipping" data-testid="product-shipping">
            <legend>{t('products.shipping_title')}</legend>
            <p className="field__hint">{t('products.shipping_hint')}</p>
            <div className="field-row">
              <TextField id="weight_kg" data-testid="product-weight" label={t('products.weight_kg')} type="number" step="0.001" min="0"
                error={errors.weight_kg ? t(errors.weight_kg.message as string) : undefined} {...register('weight_kg')} />
              <TextField id="length_cm" label={t('products.length_cm')} type="number" step="0.1" min="0" {...register('length_cm')} />
              <TextField id="width_cm" label={t('products.width_cm')} type="number" step="0.1" min="0" {...register('width_cm')} />
              <TextField id="height_cm" label={t('products.height_cm')} type="number" step="0.1" min="0" {...register('height_cm')} />
            </div>
            <div className="field">
              <span className="field__label">{t('products.packaging')}</span>
              <label className="checkbox"><input type="radio" value="own_box" {...register('packaging')} /> {t('products.packaging_own_box')}</label>
              <label className="checkbox"><input type="radio" value="mixed" {...register('packaging')} /> {t('products.packaging_mixed')}</label>
            </div>
          </fieldset>
          <div className="checkbox-row">
            <label className="checkbox">
              <input type="checkbox" {...register('on_sale')} /> {t('fields.on_sale')}
            </label>
            <label className="checkbox">
              <input type="checkbox" disabled={stockLocked} {...register('manage_stock')} /> {t('fields.manage_stock')}
            </label>
            <label className="checkbox">
              <input type="checkbox" disabled={stockLocked} {...register('is_in_stock')} /> {t('fields.is_in_stock')}
            </label>
          </div>
        </>
      )}

      {tab === 'images' && <ProductImages images={images} onChange={setImages} productId={product?.id} />}

      {tab === 'categories' && (
        <Controller
          control={control}
          name="category_ids"
          render={({ field }) => (
            <div className="checkbox-grid">
              {(categories?.items ?? []).map((cat) => (
                <label key={cat.id} className="checkbox">
                  <input
                    type="checkbox"
                    checked={field.value.includes(cat.id)}
                    onChange={(e) =>
                      field.onChange(
                        e.target.checked ? [...field.value, cat.id] : field.value.filter((id: string) => id !== cat.id),
                      )
                    }
                  />
                  {cat.name?.ro ?? cat.label ?? cat.id}
                </label>
              ))}
            </div>
          )}
        />
      )}

      {tab === 'seo' && (
        <>
          <LanguageTabs value={lang} onChange={setLang} missing={missingLangs} />
          <TextField
            id={`seo-title-${lang}`}
            label={`${t('fields.seo_title')} (${lang.toUpperCase()})`}
            {...register(`translations.${lang}.seo_title` as const)}
          />
          <TextAreaField
            id={`seo-desc-${lang}`}
            label={`${t('fields.seo_description')} (${lang.toUpperCase()})`}
            {...register(`translations.${lang}.seo_description` as const)}
          />
        </>
      )}

      <div className="form-actions">
        {onCancel && (
          <button type="button" className="btn" onClick={onCancel}>
            {t('actions.cancel')}
          </button>
        )}
        <button type="submit" className="btn btn--primary" disabled={isSubmitting} data-testid="product-save">
          {t('actions.save')}
        </button>
      </div>
    </form>
  );
}

export default ProductEditor;
