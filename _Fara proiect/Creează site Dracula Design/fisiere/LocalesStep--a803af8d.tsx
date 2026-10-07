import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useMemo } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { z } from 'zod';
import * as settingsApi from '../../../api/settings';
import { SelectField, TextField, useToast } from '../../../components';
import { apiErrorMessage } from '../../../lib/errors';
import { LANGUAGES, type Language } from '../../../types';
import { COUNTRY_RE, currencyCodes, displayName, parseCountries, type StepProps } from '../shared';

/** Pasul 3 — limbile active și cea implicită, moneda, TVA-ul și țările în care se livrează. */
export function LocalesStep({ settings, formId, onSaved, setBusy }: StepProps) {
  const { t, i18n } = useTranslation();
  const toast = useToast();
  const qc = useQueryClient();
  const lang = i18n.language || 'ro';

  const schema = useMemo(
    () => z.object({
      languages: z.array(z.string().regex(/^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$/)).min(1, t('onboarding.v.one_language')),
      default_language: z.string().min(2),
      currency: z.string().trim().toUpperCase().regex(/^[A-Z]{3}$/, t('onboarding.v.currency')),
      vat_percent: z.coerce.number({ invalid_type_error: t('onboarding.v.number') }).min(0, t('onboarding.v.vat')).max(99, t('onboarding.v.vat')),
      countries: z.string().refine((raw) => parseCountries(raw).every((c) => COUNTRY_RE.test(c)), t('onboarding.v.countries')),
    }).refine((v) => v.languages.includes(v.default_language), { path: ['default_language'], message: t('onboarding.v.default_language') }),
    [t],
  );
  type Values = z.infer<typeof schema>;

  const { control, register, handleSubmit, watch, setValue, formState: { errors } } = useForm<Values>({
    resolver: zodResolver(schema),
    defaultValues: {
      languages: settings.languages?.length ? settings.languages : [settings.default_language].filter(Boolean) as Language[],
      default_language: settings.default_language,
      currency: settings.currency ?? '',
      vat_percent: Math.round(Number(settings.vat_rate ?? 0) * 1000) / 10,
      countries: (settings.shipping_rules?.countries ?? []).join(', '),
    },
  });
  const languages = watch('languages');
  const countries = parseCountries(watch('countries') ?? '');
  const currencies = useMemo(currencyCodes, []);

  const save = useMutation({
    mutationFn: (v: Values) => {
      const rules = settings.shipping_rules ?? { countries: [], rules: settings.shipping ?? [] };
      return settingsApi.updateSettings({
        languages: v.languages,
        default_language: v.default_language,
        currency: v.currency.toUpperCase(),
        vat_rate: Math.round(v.vat_percent * 10) / 1000,
        /* `shipping_rules` se rescrie întreg pe server: păstrăm regulile și metodele de plată existente. */
        shipping_rules: { ...rules, rules: rules.rules ?? settings.shipping ?? [], countries: parseCountries(v.countries) },
      });
    },
    onMutate: () => setBusy(true),
    onSettled: () => setBusy(false),
    onSuccess: (data) => {
      qc.setQueryData(['settings'], data);
      onSaved();
    },
    onError: (error) => toast.error(apiErrorMessage(error, t)),
  });

  return (
    <form id={formId} className="ob-form" noValidate onSubmit={handleSubmit((v) => save.mutate(v))} data-testid="ob-locales-form">
      <p className="ob-lead">{t('onboarding.locales.lead')}</p>
      <fieldset className="ob-fieldset">
        <legend>{t('onboarding.locales.languages')}</legend>
        <Controller
          control={control}
          name="languages"
          render={({ field }) => (
            <div className="checkbox-row">
              {LANGUAGES.map((code) => (
                <label key={code} className="checkbox">
                  <input
                    type="checkbox"
                    data-testid={`ob-lang-${code}`}
                    checked={field.value.includes(code)}
                    onChange={(e) => field.onChange(e.target.checked ? LANGUAGES.filter((l) => l === code || field.value.includes(l)) : field.value.filter((l) => l !== code))}
                  />
                  {displayName(lang, 'language', code)} ({code.toUpperCase()})
                </label>
              ))}
            </div>
          )}
        />
        {errors.languages?.message && <p className="field__error" role="alert">{errors.languages.message}</p>}
      </fieldset>
      <div className="field-row">
        <SelectField
          id="ob-default-language"
          data-testid="ob-default-language"
          label={t('onboarding.locales.default_language')}
          error={errors.default_language?.message}
          options={languages.map((code) => ({ value: code, label: displayName(lang, 'language', code) }))}
          {...register('default_language')}
        />
        <TextField id="ob-currency" data-testid="ob-currency" list="ob-currency-list" label={t('onboarding.locales.currency')} hint={t('onboarding.locales.currency_hint')}
          error={errors.currency?.message} {...register('currency', { onBlur: (e) => setValue('currency', String(e.target.value).toUpperCase()) })} />
        <datalist id="ob-currency-list">
          {currencies.map((c) => <option key={c} value={c}>{displayName(lang, 'currency', c)}</option>)}
        </datalist>
        <TextField id="ob-vat" data-testid="ob-vat" type="number" step="0.5" min={0} max={99} label={t('onboarding.locales.vat')} error={errors.vat_percent?.message} {...register('vat_percent')} />
      </div>
      <TextField id="ob-countries" data-testid="ob-countries" label={t('onboarding.locales.countries')} hint={t('onboarding.locales.countries_hint')}
        error={errors.countries?.message} {...register('countries')} />
      {countries.length > 0 && (
        <ul className="ob-chips" data-testid="ob-country-chips">
          {countries.map((c) => (
            <li key={c} className={COUNTRY_RE.test(c) ? 'ob-chip' : 'ob-chip ob-chip--bad'}>
              {COUNTRY_RE.test(c) ? `${displayName(lang, 'region', c)} (${c})` : c}
            </li>
          ))}
        </ul>
      )}
    </form>
  );
}
