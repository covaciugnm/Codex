/**
 * Registrul aplicatiilor din dock.
 *
 * Lista si ordinea vin din `src/app/navigation.ts` (sursa unica de adevar a
 * meniului, intretinuta de P4) — aici se adauga doar ce tine de shell: iconul,
 * dimensiunea implicita a ferestrei si componenta incarcata lazy.
 *
 * Cand P4 adauga un modul nou in `navItems`, dockul il preia automat; daca nu
 * are intrare in `APP_META`, primeste un icon generic si un placeholder.
 */
import { lazy, Suspense } from 'react';
import type { ComponentType } from 'react';
import { useTranslation } from 'react-i18next';
import { navItems } from '../app/navigation';
import type { AppDefinition, AppId, AppWindowProps } from './types';
import {
  IconAppearance,
  IconCategories,
  IconCod,
  IconPromo,
  IconCustomers,
  IconDashboard,
  IconLegal,
  IconMarketplace,
  IconIntegrations,
  IconMedia,
  IconOnboarding,
  IconOrders,
  IconPages,
  IconPreview,
  IconProducts,
  IconSettings,
  IconTranslations,
  IconUsers,
  IconWarehouse,
} from './icons';
import { WarehouseDockBadge } from '../features/warehouse/Notifications';
import { OnboardingDockBadge } from '../features/onboarding/OnboardingShell';
import { PreviewApp } from './PreviewApp';

interface AppMeta {
  icon: ComponentType<{ className?: string }>;
  component: ComponentType<AppWindowProps>;
  defaultSize: { width: number; height: number };
  roles?: readonly string[];
  badge?: ComponentType;
}

/** Ambaleaza un import dinamic intr-un `React.lazy` cu fallback de incarcare. */
function lazyPage(
  loader: () => Promise<{ default: ComponentType }>,
): ComponentType<AppWindowProps> {
  const Lazy = lazy(loader);
  function LazyWindowBody() {
    return (
      <Suspense fallback={<WindowLoading />}>
        <Lazy />
      </Suspense>
    );
  }
  return LazyWindowBody;
}

function WindowLoading() {
  const { t } = useTranslation();
  return <div className="os-window-loading">{t('table.loading')}</div>;
}

function Unknown() {
  const { t } = useTranslation();
  return <div className="os-coming-soon">{t('shell.comingSoon')}</div>;
}

const APP_META: Record<string, AppMeta> = {
  inquiries: {
    icon: IconCustomers,
    component: lazyPage(() => import('../features/inquiries/InquiriesPage')),
    defaultSize: { width: 980, height: 620 },
  },
  dashboard: {
    icon: IconDashboard,
    component: lazyPage(() => import('../features/dashboard/DashboardPage')),
    defaultSize: { width: 980, height: 620 },
  },
  products: {
    icon: IconProducts,
    component: lazyPage(() => import('../features/products/ProductsPage')),
    defaultSize: { width: 1120, height: 680 },
  },
  warehouse: {
    icon: IconWarehouse,
    component: lazyPage(() => import('../features/warehouse/WarehousePage')),
    defaultSize: { width: 1240, height: 760 },
    badge: WarehouseDockBadge,
  },
  categories: {
    icon: IconCategories,
    component: lazyPage(() => import('../features/categories/CategoriesPage')),
    defaultSize: { width: 900, height: 620 },
  },
  orders: {
    icon: IconOrders,
    component: lazyPage(() => import('../features/orders/OrdersPage')),
    defaultSize: { width: 1080, height: 660 },
  },
  cod: {
    icon: IconCod,
    component: lazyPage(() => import('../features/reports/CodReportPage')),
    defaultSize: { width: 1180, height: 700 },
  },
  emag: {
    icon: IconMarketplace,
    component: lazyPage(() => import('../features/integrations/EmagPage')),
    defaultSize: { width: 1180, height: 720 },
  },
  integrations: {
    icon: IconIntegrations,
    component: lazyPage(() => import('../features/integrations/IntegrationsHubPage')),
    defaultSize: { width: 1120, height: 720 },
    roles: ['owner'],
  },
  promotions: {
    icon: IconPromo,
    component: lazyPage(() => import('../features/promotions/PromotionsPage')),
    defaultSize: { width: 1100, height: 700 },
    roles: ['owner'],
  },
  customers: {
    icon: IconCustomers,
    component: lazyPage(() => import('../features/customers/CustomersPage')),
    defaultSize: { width: 1000, height: 640 },
  },
  pages: {
    icon: IconPages,
    component: lazyPage(() => import('../features/pages/PagesPage')),
    defaultSize: { width: 1080, height: 680 },
  },
  legal: {
    icon: IconLegal,
    component: lazyPage(() => import('../features/legal/LegalPagesPage')),
    defaultSize: { width: 1000, height: 660 },
  },
  media: {
    icon: IconMedia,
    component: lazyPage(() => import('../features/media/MediaPage')),
    defaultSize: { width: 1040, height: 660 },
  },
  appearance: {
    icon: IconAppearance,
    component: lazyPage(() => import('../features/settings/AppearancePage')),
    defaultSize: { width: 940, height: 620 },
  },
  translations: {
    icon: IconTranslations,
    component: lazyPage(() => import('../features/translations/TranslationsPage')),
    defaultSize: { width: 1100, height: 660 },
  },
  settings: {
    icon: IconSettings,
    component: lazyPage(() => import('../features/settings/SettingsPage')),
    defaultSize: { width: 900, height: 660 },
    roles: ['owner'],
  },
  users: {
    icon: IconUsers,
    component: lazyPage(() => import('../features/users/UsersPage')),
    defaultSize: { width: 880, height: 600 },
    roles: ['owner'],
  },
  onboarding: {
    icon: IconOnboarding,
    component: lazyPage(() => import('../features/onboarding/OnboardingWizard')),
    defaultSize: { width: 1080, height: 740 },
    roles: ['owner'],
    badge: OnboardingDockBadge,
  },
};

const FALLBACK_META: AppMeta = {
  icon: IconPages,
  component: Unknown,
  defaultSize: { width: 900, height: 600 },
};

/** Aplicatia „Preview site”, proprie shell-ului (nu apare in `navItems`). */
const PREVIEW_APP: AppDefinition = {
  id: 'preview',
  titleKey: 'nav.preview',
  path: null,
  icon: IconPreview,
  component: PreviewApp,
  defaultSize: { width: 1060, height: 720 },
  singleton: true,
};

export const APPS: readonly AppDefinition[] = [
  ...navItems.map<AppDefinition>((item) => {
    const meta = APP_META[item.id] ?? FALLBACK_META;
    return {
      id: item.id,
      titleKey: item.labelKey,
      path: item.path,
      icon: meta.icon,
      component: meta.component,
      defaultSize: meta.defaultSize,
      singleton: true,
      roles: meta.roles,
      badge: meta.badge,
    };
  }),
  PREVIEW_APP,
];

const APP_BY_ID = new Map<AppId, AppDefinition>(APPS.map((app) => [app.id, app]));

export function getApp(id: AppId): AppDefinition | undefined {
  return APP_BY_ID.get(id);
}

/** Aplicatia care corespunde unei cai din router (`/products` → `products`). */
export function appByPath(path: string): AppDefinition | undefined {
  const normalized = path === '' ? '/' : path;
  return APPS.find((app) => app.path === normalized);
}

/** Aplicatiile vizibile pentru un rol dat (`undefined` = toate). */
export function appsForRole(role: string | undefined): readonly AppDefinition[] {
  if (!role) return APPS;
  return APPS.filter((app) => !app.roles || app.roles.includes(role));
}
