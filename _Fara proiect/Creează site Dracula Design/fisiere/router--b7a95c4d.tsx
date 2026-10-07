import { Suspense, lazy } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { LoginPage, RequireAuth } from '../features/auth';
import { config } from '../lib/config';
import { AdminLayout } from '../shell';

/**
 * Paginile se incarca lazy, ca Rollup sa poata separa chunk-urile.
 * `shell/apps.registry.tsx` foloseste aceleasi module, deci chunk-ul e partajat.
 */
const DashboardPage = lazy(() => import('../features/dashboard/DashboardPage'));
const InquiriesPage = lazy(() => import('../features/inquiries/InquiriesPage'));
const ProductsPage = lazy(() => import('../features/products/ProductsPage'));
const WarehousePage = lazy(() => import('../features/warehouse/WarehousePage'));
const CategoriesPage = lazy(() => import('../features/categories/CategoriesPage'));
const OrdersPage = lazy(() => import('../features/orders/OrdersPage'));
const CodReportPage = lazy(() => import('../features/reports/CodReportPage'));
const EmagPage = lazy(() => import('../features/integrations/EmagPage'));
const IntegrationsHubPage = lazy(() => import('../features/integrations/IntegrationsHubPage'));
const PromotionsPage = lazy(() => import('../features/promotions/PromotionsPage'));
const CustomersPage = lazy(() => import('../features/customers/CustomersPage'));
const PagesPage = lazy(() => import('../features/pages/PagesPage'));
const LegalPagesPage = lazy(() => import('../features/legal/LegalPagesPage'));
const MediaPage = lazy(() => import('../features/media/MediaPage'));
const AppearancePage = lazy(() => import('../features/settings/AppearancePage'));
const TranslationsPage = lazy(() => import('../features/translations/TranslationsPage'));
const SettingsPage = lazy(() => import('../features/settings/SettingsPage'));
const UsersPage = lazy(() => import('../features/users/UsersPage'));
const OnboardingWizard = lazy(() => import('../features/onboarding/OnboardingWizard'));

function Lazy({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<div className="auth-boot">…</div>}>{children}</Suspense>;
}

export const router = createBrowserRouter(
  [
    { path: '/login', element: <LoginPage /> },
    {
      element: <RequireAuth />,
      children: [
        {
          element: <AdminLayout />,
          children: [
            { index: true, element: <Lazy><DashboardPage /></Lazy> },
            { path: 'inquiries', element: <Lazy><InquiriesPage /></Lazy> },
            { path: 'products', element: <Lazy><ProductsPage /></Lazy> },
            { path: 'warehouse', element: <Lazy><WarehousePage /></Lazy> },
            { path: 'categories', element: <Lazy><CategoriesPage /></Lazy> },
            { path: 'orders', element: <Lazy><OrdersPage /></Lazy> },
            { path: 'reports/cod', element: <Lazy><CodReportPage /></Lazy> },
            { path: 'integrations/emag', element: <Lazy><EmagPage /></Lazy> },
            { path: 'integrations', element: <Lazy><IntegrationsHubPage /></Lazy> },
            { path: 'promotions', element: <Lazy><PromotionsPage /></Lazy> },
            { path: 'customers', element: <Lazy><CustomersPage /></Lazy> },
            { path: 'pages', element: <Lazy><PagesPage /></Lazy> },
            { path: 'legal-pages', element: <Lazy><LegalPagesPage /></Lazy> },
            { path: 'media', element: <Lazy><MediaPage /></Lazy> },
            { path: 'appearance', element: <Lazy><AppearancePage /></Lazy> },
            { path: 'translations', element: <Lazy><TranslationsPage /></Lazy> },
            { path: 'settings', element: <Lazy><SettingsPage /></Lazy> },
            { path: 'users', element: <Lazy><UsersPage /></Lazy> },
            { path: 'onboarding', element: <Lazy><OnboardingWizard /></Lazy> },
          ],
        },
      ],
    },
    { path: '*', element: <Navigate to="/" replace /> },
  ],
  { basename: config.basename },
);
