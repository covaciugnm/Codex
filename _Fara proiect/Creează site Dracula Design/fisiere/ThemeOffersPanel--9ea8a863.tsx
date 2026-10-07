import { keepPreviousData, useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useMemo, useState, type KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';
import * as settingsApi from '../../api/settings';
import { ConfirmDialog, LocalizedField, useIsOwner, useToast } from '../../components';
import { apiErrorMessage } from '../../lib/errors';
import { tr } from '../../lib/format';
import { LANGUAGES, type Language } from '../../types';
import { OfferMatchedList } from './OfferMatchedList';
import { ProductPicker, useDebounced } from './ProductPicker';
import { ThemePreviewButton } from './ThemePreviewButton';
import type { ThemeOffer, ThemeOfferCategory, ThemeOfferPreview, ThemeOfferSelector, ThemeOffers, ThemeOfferTheme } from '../../types';

export const THEME_OFFERS_KEY = ['theme-offers'] as const;

/** Rând din editor: `_key` ține identitatea React și pentru ofertele noi (fără `id`). */
type DraftOffer = ThemeOffer & { _key: string };

let keySeq = 0;
const newKey = () => `offer-${++keySeq}`;

const emptyLabels = (): Record<Language, string> => ({ ro: '', en: '', de: '', hu: '', bg: '', el: '' });

export function useThemeOffers(enabled = true) {
  return useQuery({ queryKey: THEME_OFFERS_KEY, queryFn: settingsApi.getThemeOffers, retry: false, enabled });
}

/** Serverele mai vechi nu trimit `exclude_skus`: îl completăm, ca să nu apară ca modificare. */
function normSelector(selector: ThemeOfferSelector): ThemeOfferSelector {
  return { ...selector, exclude_skus: selector.exclude_skus ?? [] };
}

function toDraft(data: ThemeOffers): DraftOffer[] {
  return [...data.offers]
    .sort((a, b) => a.sort_order - b.sort_order)
    .map((o) => ({ ...o, selector: normSelector(o.selector), labels: { ...emptyLabels(), ...o.labels }, _key: o.id ?? newKey() }));
}

function themeLabel(themes: ThemeOfferTheme[], id: string, lang: string): string {
  const theme = themes.find((th) => th.id === id);
  return (theme && tr(theme.name, lang)) || id;
}

/** Arborele de categorii aplatizat (părinte → copii), cu adâncimea pentru indentare. */
function flattenCategories(categories: ThemeOfferCategory[]): Array<ThemeOfferCategory & { depth: number }> {
  const ids = new Set(categories.map((c) => c.id));
  const children = new Map<string | null, ThemeOfferCategory[]>();
  for (const c of categories) {
    const parent = c.parent_id && ids.has(c.parent_id) ? c.parent_id : null;
    children.set(parent, [...(children.get(parent) ?? []), c]);
  }
  const out: Array<ThemeOfferCategory & { depth: number }> = [];
  const seen = new Set<string>();
  const walk = (parent: string | null, depth: number) => {
    for (const c of [...(children.get(parent) ?? [])].sort((a, b) => a.name.localeCompare(b.name))) {
      if (seen.has(c.id)) continue;
      seen.add(c.id);
      out.push({ ...c, depth });
      walk(c.id, depth + 1);
    }
  };
  walk(null, 0);
  return out;
}

export { useDebounced };

/** `offers[3].percent`, `offers.3.percent`, `body.offers.3.selector.keywords` → `offers.3.percent` … */
export function flattenDetails(err: unknown): Record<string, string> {
  const details = (err as { details?: Record<string, string[] | string> } | null)?.details ?? {};
  const flat: Record<string, string> = {};
  for (const [key, value] of Object.entries(details)) {
    const msg = Array.isArray(value) ? value[0] : value;
    if (msg) flat[key.replace(/^body\./, '').replace(/\[(\d+)\]/g, '.$1')] = String(msg);
  }
  return flat;
}

interface PanelProps {
  /** Tema după care se filtrează lista (`''` = toate). Controlată din AppearancePage, ca să poată sări din calendar. */
  themeFilter: string;
  onThemeFilterChange: (themeId: string) => void;
  /** Link „Vitrina temei” pe fiecare ofertă: deschide tabul vitrinei pe tema ofertei. */
  onShowShowcase?: (themeId: string) => void;
}

/** Oferte automate legate de teme: procent, selecție de produse, badge în 6 limbi și previzualizarea cardului. */
export function ThemeOffersPanel({ themeFilter, onThemeFilterChange, onShowShowcase }: PanelProps) {
  const { t, i18n } = useTranslation();
  const toast = useToast();
  const qc = useQueryClient();
  const owner = useIsOwner();
  const readOnly = !owner;
  const lang = i18n.language;
  const { data, isLoading, error } = useThemeOffers();
  const [draft, setDraft] = useState<DraftOffer[] | null>(null);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  const serverDraft = useMemo(() => (data ? toDraft(data) : null), [data]);
  const current = draft ?? serverDraft;
  const dirty = draft !== null;

  const save = useMutation({
    mutationFn: (offers: DraftOffer[]) =>
      settingsApi.saveThemeOffers({
        offers: offers.map(({ _key, matched_count, eligible_count, ...rest }, index) => {
          void _key;
          void matched_count;
          void eligible_count;
          return { ...rest, sort_order: index };
        }),
      }),
    onSuccess: (next) => {
      qc.setQueryData(THEME_OFFERS_KEY, next);
      setDraft(null);
      setFieldErrors({});
      setExpanded(new Set());
      toast.success(t('settings.theme_offers.saved'));
      void qc.invalidateQueries({ queryKey: THEME_OFFERS_KEY });
    },
    onError: (err: unknown) => {
      setFieldErrors(flattenDetails(err));
      toast.error(apiErrorMessage(err, t));
    },
  });

  if (isLoading) return <p>{t('table.loading')}</p>;
  if (error || !data || !current) {
    return <div className="placeholder-note" role="alert" data-testid="theme-offers-error">{apiErrorMessage(error, t)}</div>;
  }

  const themes = data.themes;
  const setOffers = (offers: DraftOffer[]) => setDraft(offers);
  const update = (key: string, patch: Partial<ThemeOffer>) =>
    setOffers(current.map((o) => (o._key === key ? { ...o, ...patch } : o)));
  const toggle = (key: string) => {
    const next = new Set(expanded);
    if (next.has(key)) next.delete(key); else next.add(key);
    setExpanded(next);
  };

  const addOffer = () => {
    const themeId = themeFilter || themes.find((th) => th.kind !== 'base')?.id || themes[0]?.id || '';
    const offer: DraftOffer = {
      _key: newKey(), theme_id: themeId, name: '', labels: emptyLabels(), percent: 10,
      selector: { all: false, category_ids: [], keywords: [], skus: [], exclude_skus: [], exclude_on_sale: true },
      enabled: true, priority: 0, sort_order: current.length, matched_count: 0,
    };
    setOffers([...current, offer]);
    setExpanded(new Set(expanded).add(offer._key));
  };

  const duplicate = (key: string) => {
    const index = current.findIndex((o) => o._key === key);
    if (index < 0) return;
    const src = current[index];
    const copy: DraftOffer = {
      ...src, id: undefined, _key: newKey(), name: t('settings.theme_offers.copy_name', { name: src.name || themeLabel(themes, src.theme_id, lang) }),
      selector: { ...src.selector, category_ids: [...src.selector.category_ids], keywords: [...src.selector.keywords], skus: [...src.selector.skus], exclude_skus: [...src.selector.exclude_skus] },
      labels: { ...src.labels },
    };
    setOffers([...current.slice(0, index + 1), copy, ...current.slice(index + 1)]);
    setExpanded(new Set(expanded).add(copy._key));
  };

  /* Validare locală (serverul validează oricum): procent întreg 1–90, temă aleasă. */
  const localErrors: Record<string, string> = {};
  current.forEach((o, i) => {
    if (!Number.isInteger(o.percent) || o.percent < 1 || o.percent > 90) localErrors[`offers.${i}.percent`] = t('settings.theme_offers.percent_range');
    if (!o.theme_id) localErrors[`offers.${i}.theme_id`] = t('validation.required');
  });
  const errors = { ...fieldErrors, ...localErrors };
  const hasLocalErrors = Object.keys(localErrors).length > 0;

  const shown = current.map((offer, index) => ({ offer, index })).filter(({ offer }) => !themeFilter || offer.theme_id === themeFilter);
  const toDelete = current.find((o) => o._key === confirmDelete);

  /* Erorile care nu pot fi legate de un rând afișat apar sub butonul de salvare. */
  const shownIndexes = new Set(shown.map(({ index }) => index));
  const looseErrors = Object.entries(fieldErrors).filter(([key]) => {
    const m = /^offers\.(\d+)/.exec(key);
    return !m || !shownIndexes.has(Number(m[1]));
  });

  const themeOptions = themes.map((th) => ({ value: th.id, label: tr(th.name, lang) || th.id }));

  return (
    <div className="theme-offers" data-testid="theme-offers">
      {readOnly && <div className="placeholder-note">{t('settings.theme_offers.readonly')}</div>}
      <p className="field__hint">{t('settings.theme_offers.intro')}</p>

      <div className="theme-offers__toolbar">
        <label className="theme-offers__filter">
          <span className="field__label">{t('settings.theme_offers.filter_theme')}</span>
          <select className="field__input" data-testid="offers-filter" value={themeFilter} onChange={(e) => onThemeFilterChange(e.target.value)}>
            <option value="">{t('settings.theme_offers.all_themes')}</option>
            {themeOptions.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label} ({current.filter((x) => x.theme_id === o.value).length})
              </option>
            ))}
          </select>
        </label>
        {themeFilter && (
          <ThemePreviewButton themeId={themeFilter} className="btn btn--ghost btn--small" testId="offers-preview"
            label={t('settings.theme_preview.button_store')} />
        )}
        {!readOnly && (
          <button type="button" className="btn btn--primary" data-testid="offers-add" onClick={addOffer}>
            {t('settings.theme_offers.add')}
          </button>
        )}
      </div>

      {shown.length === 0 && (
        <p className="placeholder-note" data-testid="offers-empty">
          {themeFilter ? t('settings.theme_offers.empty_theme') : t('settings.theme_offers.empty')}
        </p>
      )}

      <ul className="theme-offers__list">
        {shown.map(({ offer, index }) => (
          <OfferRow
            key={offer._key}
            offer={offer}
            index={index}
            server={data.offers.find((o) => o.id && o.id === offer.id)}
            themes={themes}
            categories={data.categories}
            live={!!data.effective_theme && offer.theme_id === data.effective_theme}
            expanded={expanded.has(offer._key)}
            readOnly={readOnly}
            errors={errors}
            onToggle={() => toggle(offer._key)}
            onChange={(patch) => update(offer._key, patch)}
            onDuplicate={() => duplicate(offer._key)}
            onDelete={() => setConfirmDelete(offer._key)}
            onShowShowcase={onShowShowcase}
          />
        ))}
      </ul>

      {!readOnly && (
        <div className="theme-sched__actions">
          <button type="button" className="btn btn--primary" data-testid="offers-save" disabled={!dirty || save.isPending || hasLocalErrors}
            onClick={() => save.mutate(current)}>
            {t('settings.theme_offers.save')}
          </button>
          {dirty && (
            <button type="button" className="btn btn--ghost" data-testid="offers-discard" disabled={save.isPending}
              onClick={() => { setDraft(null); setFieldErrors({}); }}>
              {t('settings.theme_offers.discard')}
            </button>
          )}
          {dirty && <span className="field__hint">{t('common.unsaved')}</span>}
          {hasLocalErrors && <span className="field__error">{t('settings.theme_offers.fix_errors')}</span>}
        </div>
      )}
      {looseErrors.length > 0 && (
        <ul className="ship-v2__errors" role="alert" data-testid="offers-errors">
          {looseErrors.map(([key, msg]) => <li key={key}>{key}: {msg}</li>)}
        </ul>
      )}

      <ConfirmDialog
        open={!!toDelete}
        danger
        testId="confirm-offer-delete"
        title={t('settings.theme_offers.delete')}
        message={t('settings.theme_offers.delete_confirm', { name: toDelete?.name || themeLabel(themes, toDelete?.theme_id ?? '', lang) })}
        onCancel={() => setConfirmDelete(null)}
        onConfirm={() => {
          setOffers(current.filter((o) => o._key !== confirmDelete));
          /* Erorile serverului sunt pe indici; după ștergere indicii se mută. */
          setFieldErrors({});
          setConfirmDelete(null);
        }}
      />
    </div>
  );
}

interface RowProps {
  offer: DraftOffer;
  index: number;
  server: ThemeOffer | undefined;
  themes: ThemeOfferTheme[];
  categories: ThemeOfferCategory[];
  /** Tema ofertei e cea afișată acum în magazin. */
  live: boolean;
  expanded: boolean;
  readOnly: boolean;
  errors: Record<string, string>;
  onToggle: () => void;
  onChange: (patch: Partial<ThemeOffer>) => void;
  onDuplicate: () => void;
  onDelete: () => void;
  onShowShowcase?: (themeId: string) => void;
}

function sameSelector(a: ThemeOfferSelector, b: ThemeOfferSelector | undefined): boolean {
  return !!b && JSON.stringify(normSelector(a)) === JSON.stringify(normSelector(b));
}

/** O ofertă: antetul cu câmpurile de bază și, extins, editorul de selecție + badge + previzualizare. */
function OfferRow({ offer, index, server, themes, categories, live, expanded, readOnly, errors, onToggle, onChange, onDuplicate, onDelete, onShowShowcase }: RowProps) {
  const { t, i18n } = useTranslation();
  const lang = i18n.language;
  const id = `offer-${index}`;
  const err = (field: string) => errors[`offers.${index}.${field}`];

  /* Previzualizarea rulează când rândul e deschis sau când selecția/procentul diferă de ce a calculat serverul. */
  const changed = !server || !sameSelector(offer.selector, server.selector) || server.percent !== offer.percent;
  const previewInput = useMemo(
    () => ({ selector: offer.selector, percent: offer.percent, theme_id: offer.theme_id || undefined }),
    [offer.selector, offer.percent, offer.theme_id],
  );
  const debounced = useDebounced(previewInput, 500);
  const pending = debounced !== previewInput;
  const preview = useQuery({
    queryKey: ['theme-offer-preview', debounced],
    queryFn: () => settingsApi.previewThemeOffer(debounced),
    enabled: (expanded || changed) && debounced.percent >= 1 && debounced.percent <= 90,
    placeholderData: keepPreviousData,
    retry: false,
    staleTime: 30_000,
  });
  const fromPreview = !!preview.data && (expanded || changed);
  const count = fromPreview ? preview.data!.matched_count : offer.matched_count;
  const eligible = fromPreview ? preview.data!.eligible_count : offer.eligible_count;
  const effective = eligible ?? count;
  const themeName = themeLabel(themes, offer.theme_id, lang);

  const setSelector = (patch: Partial<ThemeOfferSelector>) => onChange({ selector: { ...offer.selector, ...patch } });
  const autofill = () => {
    const theme = themes.find((th) => th.id === offer.theme_id);
    const labels = emptyLabels();
    for (const l of LANGUAGES) labels[l] = `-${offer.percent}% ${theme ? tr(theme.name, l) || theme.id : offer.theme_id}`.trim();
    onChange({ labels });
  };

  return (
    <li className={offer.enabled ? 'theme-offer' : 'theme-offer theme-offer--off'} data-testid={`offer-${index}`} data-expanded={expanded}>
      <div className="theme-offer__head">
        <label className="theme-offer__cell theme-offer__cell--theme">
          <span className="field__label">{t('settings.theme_offers.col_theme')}</span>
          <select className="field__input" disabled={readOnly} value={offer.theme_id} aria-invalid={!!err('theme_id')}
            data-testid={`${id}-theme`} onChange={(e) => onChange({ theme_id: e.target.value })}>
            {!themes.some((th) => th.id === offer.theme_id) && <option value={offer.theme_id}>{offer.theme_id || '—'}</option>}
            {themes.map((th) => <option key={th.id} value={th.id}>{tr(th.name, lang) || th.id}</option>)}
          </select>
          {err('theme_id') && <span className="field__error" role="alert">{err('theme_id')}</span>}
          {live && <span className="theme-offer__live" data-testid={`${id}-live`}>{t('settings.theme_offers.live_now')}</span>}
          {onShowShowcase && offer.theme_id && (
            <button type="button" className="theme-sched__offers theme-offer__showcase" data-testid={`${id}-showcase`}
              title={t('settings.theme_showcase.link_title')} onClick={(e) => { e.preventDefault(); onShowShowcase(offer.theme_id); }}>
              {t('settings.theme_showcase.link')}
            </button>
          )}
        </label>
        <label className="theme-offer__cell theme-offer__cell--name">
          <span className="field__label">{t('settings.theme_offers.col_name')}</span>
          <input className="field__input" maxLength={120} disabled={readOnly} value={offer.name} data-testid={`${id}-name`}
            placeholder={t('settings.theme_offers.name_placeholder')} aria-invalid={!!err('name')}
            onChange={(e) => onChange({ name: e.target.value })} />
          {err('name') && <span className="field__error" role="alert">{err('name')}</span>}
        </label>
        <label className="theme-offer__cell">
          <span className="field__label">{t('settings.theme_offers.col_percent')}</span>
          <span className="theme-offer__percent">
            <input className="field__input theme-sched__num" type="number" min={1} max={90} step={1} disabled={readOnly}
              value={Number.isFinite(offer.percent) ? offer.percent : ''} aria-invalid={!!err('percent')} data-testid={`${id}-percent`}
              onChange={(e) => onChange({ percent: e.target.value === '' ? NaN : Math.trunc(Number(e.target.value)) })} />
            <span aria-hidden="true">%</span>
          </span>
          {err('percent') && <span className="field__error" role="alert">{err('percent')}</span>}
        </label>
        <label className="theme-offer__cell">
          <span className="field__label">{t('settings.theme_offers.col_priority')}</span>
          <input className="field__input theme-sched__num" type="number" step={1} disabled={readOnly} value={offer.priority}
            aria-invalid={!!err('priority')} data-testid={`${id}-priority`}
            onChange={(e) => onChange({ priority: Math.trunc(Number(e.target.value) || 0) })} />
          {err('priority') && <span className="field__error" role="alert">{err('priority')}</span>}
        </label>
        <label className="theme-offer__cell theme-offer__cell--check">
          <span className="field__label">{t('settings.theme_offers.col_enabled')}</span>
          <input type="checkbox" checked={offer.enabled} disabled={readOnly} data-testid={`${id}-enabled`}
            onChange={(e) => onChange({ enabled: e.target.checked })} />
        </label>
        <div className="theme-offer__cell theme-offer__count" data-testid={`${id}-count`} data-count={count}>
          <span className="field__label">{t('settings.theme_offers.matched_label')}</span>
          <strong className={effective === 0 ? 'theme-offer__zero' : undefined}>
            {(expanded || changed) && (pending || preview.isFetching) ? '…' : count}
          </strong>
          {eligible !== undefined && !((expanded || changed) && (pending || preview.isFetching)) && (
            <span className="theme-offer__elig" data-testid={`${id}-eligible`} title={t('settings.theme_offers.eligible_hint')}>
              {t('settings.theme_offers.eligible', { count: eligible })}
            </span>
          )}
        </div>
        <div className="theme-offer__actions">
          <button type="button" className="btn btn--ghost btn--small" aria-expanded={expanded} data-testid={`${id}-toggle`} onClick={onToggle}>
            {expanded ? t('settings.theme_offers.collapse') : t('settings.theme_offers.edit')}
          </button>
          {!readOnly && (
            <>
              <button type="button" className="btn btn--ghost btn--small" data-testid={`${id}-duplicate`} onClick={onDuplicate}>
                {t('settings.theme_offers.duplicate')}
              </button>
              <button type="button" className="btn btn--danger btn--small" data-testid={`${id}-delete`} onClick={onDelete}>
                {t('settings.theme_offers.delete')}
              </button>
            </>
          )}
        </div>
      </div>

      {expanded && (
        <div className="theme-offer__body">
          <div className="theme-offer__editor">
            <fieldset className="theme-offer__fieldset" disabled={readOnly}>
              <legend>{t('settings.theme_offers.selection')}</legend>
              <label className="theme-offer__switch">
                <input type="checkbox" checked={offer.selector.all} data-testid={`${id}-all`}
                  onChange={(e) => setSelector({ all: e.target.checked })} />
                <span>{t('settings.theme_offers.all_products')}</span>
              </label>
              {offer.selector.all && <p className="field__hint">{t('settings.theme_offers.all_products_hint')}</p>}

              <div className={offer.selector.all ? 'theme-offer__criteria theme-offer__criteria--muted' : 'theme-offer__criteria'}>
                <CategoryPicker
                  id={`${id}-cats`}
                  categories={categories}
                  value={offer.selector.category_ids}
                  disabled={readOnly || offer.selector.all}
                  error={err('selector.category_ids')}
                  onChange={(category_ids) => setSelector({ category_ids })}
                />
                <ChipsInput
                  id={`${id}-keywords`}
                  label={t('settings.theme_offers.keywords')}
                  hint={t('settings.theme_offers.keywords_hint')}
                  placeholder={t('settings.theme_offers.chips_placeholder')}
                  values={offer.selector.keywords}
                  disabled={readOnly || offer.selector.all}
                  error={err('selector.keywords')}
                  onChange={(keywords) => setSelector({ keywords })}
                />
                <ProductPicker
                  id={`${id}-skus`}
                  label={t('settings.theme_offers.pick_include')}
                  hint={t('settings.theme_offers.pick_include_hint')}
                  emptyText={t('settings.theme_offers.pick_include_empty')}
                  value={offer.selector.skus}
                  allowPaste
                  readOnly={readOnly || offer.selector.all}
                  error={err('selector.skus')}
                  onChange={(skus) => setSelector({ skus })}
                />
              </div>
              {/* Excluderea se aplică și când oferta prinde tot catalogul. */}
              <ProductPicker
                id={`${id}-exclude-skus`}
                label={t('settings.theme_offers.pick_exclude')}
                hint={t('settings.theme_offers.pick_exclude_hint')}
                emptyText={t('settings.theme_offers.pick_exclude_empty')}
                value={offer.selector.exclude_skus}
                allowPaste
                readOnly={readOnly}
                error={err('selector.exclude_skus')}
                onChange={(exclude_skus) => setSelector({ exclude_skus })}
              />
              <label className="theme-offer__switch">
                <input type="checkbox" checked={offer.selector.exclude_on_sale} data-testid={`${id}-exclude`}
                  onChange={(e) => setSelector({ exclude_on_sale: e.target.checked })} />
                <span>{t('settings.theme_offers.exclude_on_sale')}</span>
              </label>
              {err('selector') && <p className="field__error" role="alert">{err('selector')}</p>}
            </fieldset>

            <fieldset className="theme-offer__fieldset">
              <legend>{t('settings.theme_offers.badge')}</legend>
              {readOnly ? (
                <dl className="theme-offer__labels" data-testid={`${id}-labels`}>
                  {LANGUAGES.map((l) => (
                    <div key={l}><dt>{l.toUpperCase()}</dt><dd>{offer.labels[l] || '—'}</dd></div>
                  ))}
                </dl>
              ) : (<>
              <LocalizedField
                label={t('settings.theme_offers.badge_label')}
                hint={t('settings.theme_offers.badge_hint')}
                value={offer.labels}
                error={LANGUAGES.map((l) => err(`labels.${l}`)).find(Boolean) ?? err('labels')}
                onChange={(value) => onChange({ labels: Object.fromEntries(Object.entries({ ...emptyLabels(), ...offer.labels, ...value }).map(([key, label]) => [key, label ?? ''])) })}
              />
              <div>
                <button type="button" className="btn btn--ghost btn--small" data-testid={`${id}-autofill`} onClick={autofill}>
                  {t('settings.theme_offers.autofill')}
                </button>
                <span className="field__hint theme-offer__autofill-hint">
                  {t('settings.theme_offers.autofill_hint', { example: `-${offer.percent}% ${themeName}` })}
                </span>
              </div>
              </>)}
            </fieldset>
          </div>

          <OfferPreview
            id={id}
            offer={offer}
            lang={lang}
            themeName={themeName}
            data={preview.data}
            loading={pending || preview.isFetching}
            error={preview.error}
            readOnly={readOnly}
            onSelector={setSelector}
          />
        </div>
      )}
    </li>
  );
}

/** Previzualizarea: contoarele serverului și lista COMPLETĂ a produselor prinse (× exclude, „Readu”, „Adaugă produs”). */
function OfferPreview({ id, offer, lang, themeName, data, loading, error, readOnly, onSelector }: {
  id: string; offer: ThemeOffer; lang: string; themeName: string;
  data: ThemeOfferPreview | undefined;
  loading: boolean; error: unknown; readOnly: boolean;
  onSelector: (patch: Partial<ThemeOfferSelector>) => void;
}) {
  const { t } = useTranslation();
  const badge = offer.labels[lang as Language]?.trim() || offer.labels.ro?.trim() || `-${offer.percent}%`;
  return (
    <section className="offer-preview" aria-live="polite" data-testid={`${id}-preview`}>
      <div className="offer-preview__head">
        <h4>{t('settings.theme_offers.preview')}</h4>
        <span className="offer-preview__count" data-testid={`${id}-preview-count`}>
          {t('settings.theme_offers.matched', { count: data?.matched_count ?? 0 })}
          {data?.eligible_count !== undefined && ` · ${t('settings.theme_offers.eligible', { count: data.eligible_count })}`}
          {loading && <span className="offer-preview__spinner" aria-label={t('table.loading')} />}
        </span>
      </div>
      <p className="field__hint">{t('settings.theme_offers.preview_hint', { theme: themeName })}</p>
      {offer.selector.exclude_on_sale && data?.eligible_count !== undefined && (
        <p className="field__hint" data-testid={`${id}-eligible-hint`}>{t('settings.theme_offers.eligible_hint')}</p>
      )}
      {!!error && <div className="placeholder-note" role="alert">{apiErrorMessage(error, t)}</div>}
      {data && (data.eligible_count ?? data.matched_count) === 0 && !loading && (
        <div className="offer-preview__warn" role="alert" data-testid={`${id}-zero`}>{t('settings.theme_offers.zero_warning')}</div>
      )}
      <OfferMatchedList id={id} offer={offer} badge={badge} readOnly={readOnly} onSelector={onSelector} />
    </section>
  );
}

/** Multi-select simplu cu checkbox-uri, căutare și indentare după `parent_id`. */
function CategoryPicker({ id, categories, value, disabled, error, onChange }: {
  id: string; categories: ThemeOfferCategory[]; value: string[]; disabled?: boolean; error?: string; onChange: (ids: string[]) => void;
}) {
  const { t } = useTranslation();
  const [query, setQuery] = useState('');
  const flat = useMemo(() => flattenCategories(categories), [categories]);
  const selected = new Set(value);
  const q = query.trim().toLowerCase();
  const visible = q ? flat.filter((c) => c.name.toLowerCase().includes(q)) : flat;
  const toggle = (catId: string, on: boolean) =>
    onChange(on ? [...value, catId] : value.filter((v) => v !== catId));
  const names = value.map((v) => categories.find((c) => c.id === v)?.name ?? v);

  return (
    <div className={error ? 'field field--error' : 'field'}>
      <span className="field__label" id={`${id}-label`}>
        {t('settings.theme_offers.categories')} {value.length > 0 && <span className="badge">{value.length}</span>}
      </span>
      <input className="field__input" type="search" value={query} disabled={disabled} data-testid={`${id}-search`}
        placeholder={t('settings.theme_offers.categories_search')} aria-label={t('settings.theme_offers.categories_search')}
        onChange={(e) => setQuery(e.target.value)} />
      <div className="catpick" role="group" aria-labelledby={`${id}-label`} data-testid={id}>
        {visible.length === 0 && <p className="field__hint">{t('settings.theme_offers.categories_none')}</p>}
        {visible.map((c) => (
          <label key={c.id} className="catpick__item" style={{ paddingLeft: 6 + (q ? 0 : c.depth * 18) }}>
            <input type="checkbox" checked={selected.has(c.id)} disabled={disabled} onChange={(e) => toggle(c.id, e.target.checked)} />
            <span>{c.name}</span>
          </label>
        ))}
      </div>
      {names.length > 0 && <p className="field__hint">{t('settings.theme_offers.categories_selected', { names: names.join(', ') })}</p>}
      {!error && <p className="field__hint">{t('settings.theme_offers.categories_hint')}</p>}
      {error && <p className="field__error" role="alert">{error}</p>}
    </div>
  );
}

/** Input cu „chips”: Enter sau virgulă adaugă, × șterge, Backspace pe gol scoate ultimul. */
function ChipsInput({ id, label, hint, placeholder, values, disabled, error, normalize = (v) => v, onChange }: {
  id: string; label: string; hint?: string; placeholder?: string; values: string[]; disabled?: boolean; error?: string;
  normalize?: (v: string) => string; onChange: (values: string[]) => void;
}) {
  const { t } = useTranslation();
  const [text, setText] = useState('');
  const commit = (raw: string) => {
    const parts = raw.split(',').map((p) => normalize(p.trim())).filter(Boolean);
    const next = [...values];
    for (const p of parts) if (!next.some((v) => v.toLowerCase() === p.toLowerCase())) next.push(p);
    if (next.length !== values.length) onChange(next);
    setText('');
  };
  const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      if (text.trim()) commit(text);
    } else if (e.key === 'Backspace' && !text && values.length) {
      onChange(values.slice(0, -1));
    }
  };
  return (
    <div className={error ? 'field field--error' : 'field'}>
      <label className="field__label" htmlFor={id}>{label}</label>
      <div className="chips" data-testid={`${id}-chips`}>
        {values.map((v) => (
          <span key={v} className="chips__chip">
            {v}
            {!disabled && (
              <button type="button" className="chips__x" aria-label={t('settings.theme_offers.remove_chip', { value: v })}
                onClick={() => onChange(values.filter((x) => x !== v))}>×</button>
            )}
          </span>
        ))}
        <input id={id} className="chips__input" value={text} disabled={disabled} placeholder={values.length ? '' : placeholder}
          data-testid={id} aria-invalid={!!error}
          onChange={(e) => (e.target.value.includes(',') ? commit(e.target.value) : setText(e.target.value))}
          onKeyDown={onKeyDown} onBlur={() => { if (text.trim()) commit(text); }} />
      </div>
      {hint && !error && <p className="field__hint">{hint}</p>}
      {error && <p className="field__error" role="alert">{error}</p>}
    </div>
  );
}

export default ThemeOffersPanel;
