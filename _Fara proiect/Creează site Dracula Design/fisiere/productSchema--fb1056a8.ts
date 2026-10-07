import { z } from 'zod';

const localizedString = z.string().optional();

const translationSchema = z.object({
  name: localizedString,
  slug: localizedString,
  short_description: localizedString,
  description: localizedString,
  seo_title: localizedString,
  seo_description: localizedString,
});

/** Traduceri pe cele 6 limbi; `ro.name` este singura obligatorie. */
const translationsSchema = z
  .record(translationSchema)
  .superRefine((value, ctx) => {
    if (!Object.values(value).some(v => v.name?.trim())) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, path: ['ro', 'name'], message: 'validation.required' });
    }
  });

/** Câmp numeric opțional: gol = necompletat (null), altfel ≥ 0. */
const optionalNumber = z.preprocess(
  (v) => (v === '' || v === null || v === undefined ? undefined : Number(v)),
  z.number().min(0, 'validation.positive').optional(),
);

export const productSchema = z.object({
  sku: z.string().min(2, 'validation.min'),
  ean: z
    .string()
    .optional()
    .refine((v) => !v || /^\d{8,14}$/.test(v), 'validation.ean'),
  translations: translationsSchema,
  price_ron: z.coerce.number().positive('validation.positive'),
  regular_price_ron: z.coerce.number().min(0).optional(),
  on_sale: z.boolean(),
  vat_rate: z.coerce.number().min(0).max(100),
  stock_quantity: z.coerce.number().int().min(0, 'validation.positive'),
  manage_stock: z.boolean(),
  is_in_stock: z.boolean(),
  status: z.enum(['draft', 'published', 'archived']),
  category_ids: z.array(z.string()),
  /* Livrare v2: greutatea și dimensiunile unei bucăți ambalate + cum se împachetează. */
  weight_kg: optionalNumber,
  length_cm: optionalNumber,
  width_cm: optionalNumber,
  height_cm: optionalNumber,
  packaging: z.enum(['own_box', 'mixed', '']).optional(),
});

export type ProductFormValues = z.input<typeof productSchema>;
export type ProductFormOutput = z.output<typeof productSchema>;
