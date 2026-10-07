/** Sursa unica de adevar pentru meniu — P3 o va refolosi pentru dock/ferestre. */
export interface NavItem {
  /** Cheie i18n (nav.*) */
  labelKey: string;
  /** Cale relativa la basename `/admin` */
  path: string;
  /** Identificator stabil pentru viitoarele ferestre (P3). */
  id: string;
}

export const navItems: NavItem[] = [
  { id: 'inquiries', labelKey: 'nav.inquiries', path: '/inquiries' },
  { id: 'dashboard', labelKey: 'nav.dashboard', path: '/' },
  { id: 'products', labelKey: 'nav.products', path: '/products' },
  { id: 'warehouse', labelKey: 'nav.warehouse', path: '/warehouse' },
  { id: 'categories', labelKey: 'nav.categories', path: '/categories' },
  { id: 'orders', labelKey: 'nav.orders', path: '/orders' },
  { id: 'cod', labelKey: 'nav.cod', path: '/reports/cod' },
  { id: 'emag', labelKey: 'nav.emag', path: '/integrations/emag' },
  { id: 'integrations', labelKey: 'nav.integrations', path: '/integrations' },
  { id: 'promotions', labelKey: 'nav.promotions', path: '/promotions' },
  { id: 'customers', labelKey: 'nav.customers', path: '/customers' },
  { id: 'pages', labelKey: 'nav.pages', path: '/pages' },
  { id: 'legal', labelKey: 'nav.legal', path: '/legal-pages' },
  { id: 'media', labelKey: 'nav.media', path: '/media' },
  { id: 'appearance', labelKey: 'nav.appearance', path: '/appearance' },
  { id: 'translations', labelKey: 'nav.translations', path: '/translations' },
  { id: 'settings', labelKey: 'nav.settings', path: '/settings' },
  { id: 'users', labelKey: 'nav.users', path: '/users' },
  { id: 'onboarding', labelKey: 'nav.onboarding', path: '/onboarding' },
];
