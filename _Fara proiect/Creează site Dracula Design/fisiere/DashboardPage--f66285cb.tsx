import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { OrderStatusPill } from '../../components';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import * as ordersApi from '../../api/orders';
import * as settingsApi from '../../api/settings';
import { Modal, PageHeader, SelectField } from '../../components';
import * as productsApi from '../../api/products';
import ProductEditor from '../products/ProductEditor';
import { LowPiecesCard } from '../warehouse/LowPiecesCard';
import { config } from '../../lib/config';
import { formatDate, formatMoney } from '../../lib/format';
import './DashboardPage.css';

const RANGES = ['7d', '30d', '90d'] as const;
type Range = (typeof RANGES)[number];

export function DashboardPage() {
  const { t, i18n } = useTranslation();
  // P2.4 — perioada era fixata pe 30 de zile in cod; acum o alege utilizatorul.
  const [range, setRange] = useState<Range>('30d');
  /* Click pe un produs din Top / Stoc scăzut → editorul produsului (A2: `id` + `image`). */
  const [openProduct, setOpenProduct] = useState<string | null>(null);
  const { data: productFull } = useQuery({
    queryKey: ['product', openProduct],
    queryFn: () => productsApi.getProduct(openProduct!),
    enabled: !!openProduct,
  });
  const { data, isLoading } = useQuery({
    queryKey: ['dashboard', range],
    queryFn: () => settingsApi.getDashboard(range),
  });
  const { data: recent } = useQuery({
    queryKey: ['orders', 'recent'],
    queryFn: () => ordersApi.listOrders({ per_page: 6, sort: 'created_at:desc' }),
  });

  const stats = [
    { label: t(`dashboard.revenue_range`, { range: t(`dashboard.range_${range}`) }),
      value: data ? formatMoney(data.orders.total_ron, 'RON', i18n.language) : '—' },
    { label: t(`dashboard.orders_range`, { range: t(`dashboard.range_${range}`) }),
      value: data ? String(data.orders.count) : '—' },
    { label: t('dashboard.new_customers'), value: data ? String(data.new_customers) : '—' },
    { label: t('dashboard.products_published'), value: data ? String(data.products_published) : '—' },
  ];

  const chartData = (data?.revenue_series ?? []).map((point) => ({
    ...point,
    label: new Intl.DateTimeFormat(i18n.language, { day: '2-digit', month: 'short' }).format(new Date(point.date)),
  }));

  return (
    <section>
      <PageHeader
        title={t('dashboard.title')}
        subtitle={t('app.title')}
        actions={
          <SelectField
            id="dashboard-range"
            data-testid="dashboard-range"
            label={t('dashboard.range')}
            value={range}
            onChange={(e) => setRange(e.target.value as Range)}
            options={RANGES.map((value) => ({ value, label: t(`dashboard.range_${value}`) }))}
          />
        }
      />
      {config.useMocks && <div className="placeholder-note">{t('common.mockNotice')}</div>}

      <div className="stats">
        {stats.map((stat) => (
          <div className="stats__card" key={stat.label}>
            <span className="stats__label">{stat.label}</span>
            <strong className="stats__value">{isLoading ? '…' : stat.value}</strong>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <h2>{t('dashboard.chart_title')}</h2>
        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer>
            <AreaChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="revFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--admin-primary)" stopOpacity={0.35} />
                  <stop offset="100%" stopColor="var(--admin-primary)" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="var(--color-border-soft)" vertical={false} />
              <XAxis dataKey="label" tick={{ fontSize: 11, fill: 'var(--color-muted)' }} tickLine={false} axisLine={false} minTickGap={18} />
              <YAxis tick={{ fontSize: 11, fill: 'var(--color-muted)' }} tickLine={false} axisLine={false} width={56} />
              <Tooltip
                formatter={(value) => formatMoney(Number(value) || 0, 'RON', i18n.language)}
                contentStyle={{ borderRadius: 8, border: '1px solid var(--color-border)', fontSize: 12 }}
              />
              <Area type="monotone" dataKey="total_ron" stroke="var(--admin-primary)" strokeWidth={2} fill="url(#revFill)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="dash-grid">
        <div className="card">
          <h2>{t('dashboard.recent_orders')}</h2>
          <ul className="recent">
            {(recent?.items ?? []).map((order) => (
              <li key={order.id} className="recent__item">
                <span className="recent__num">{order.order_number}</span>
                <OrderStatusPill code={order.status} />
                <span className="recent__date">{formatDate(order.created_at, i18n.language)}</span>
                <strong>{formatMoney(order.total_ron, order.currency, i18n.language)}</strong>
              </li>
            ))}
            {(recent?.items?.length ?? 0) === 0 && <li className="recent__item">{t('table.empty')}</li>}
          </ul>
        </div>

        <div className="card">
          <h2>{t('dashboard.low_stock')}</h2>
          <ul className="recent">
            {(data?.low_stock ?? []).map((item) => (
              <li key={item.id} className="recent__item">
                {item.image
                  ? <img className="recent__thumb" src={item.image} alt="" loading="lazy" width={36} height={36} />
                  : <span className="recent__thumb recent__thumb--empty" aria-hidden="true">—</span>}
                <button type="button" className="recent__product recent__product--link" title={`${item.name} · ${item.sku}`}
                  disabled={!item.id} onClick={() => item.id && setOpenProduct(item.id)}>
                  <span className="recent__product-name">{item.name}</span>
                  <small>{item.sku}</small>
                </button>
                <strong style={{ color: item.stock_quantity === 0 ? 'var(--color-danger)' : 'var(--color-warning-text)' }}>
                  {item.stock_quantity}
                </strong>
              </li>
            ))}
            {(data?.low_stock?.length ?? 0) === 0 && <li className="recent__item">{t('table.empty')}</li>}
          </ul>
        </div>

        <div className="card">
          <h2>{t('dashboard.top_products')}</h2>
          <ul className="recent">
            {(data?.top_products ?? []).map((item) => (
              <li key={item.sku} className="recent__item">
                {item.image
                  ? <img className="recent__thumb" src={item.image} alt="" loading="lazy" width={36} height={36} />
                  : <span className="recent__thumb recent__thumb--empty" aria-hidden="true">—</span>}
                <button type="button" className="recent__product recent__product--link" title={`${item.name} · ${item.sku}`}
                  disabled={!item.id} onClick={() => item.id && setOpenProduct(item.id)}>
                  <span className="recent__product-name">{item.name}</span>
                  <small>{item.sku}</small>
                </button>
                <span className="badge badge--muted">{item.qty}</span>
                <strong>{formatMoney(item.total, 'RON', i18n.language)}</strong>
              </li>
            ))}
          </ul>
        </div>

        {/* Sanatatea catalogului: `catalog` venea deja de la server, dar nu era afisat. */}
        <LowPiecesCard />

        <div className="card" data-testid="dashboard-catalog">
          <h2>{t('dashboard.catalog_health')}</h2>
          <ul className="recent">
            <li className="recent__item"><span>{t('dashboard.catalog_no_images')}</span>
              <strong style={{ color: (data?.catalog?.no_images ?? 0) > 0 ? 'var(--color-warning-text)' : undefined }}>{data?.catalog?.no_images ?? '—'}</strong></li>
            <li className="recent__item"><span>{t('dashboard.catalog_zero_price')}</span>
              <strong style={{ color: (data?.catalog?.zero_price ?? 0) > 0 ? 'var(--color-danger)' : undefined }}>{data?.catalog?.zero_price ?? '—'}</strong></li>
            <li className="recent__item"><span>{t('dashboard.catalog_missing_translations')}</span>
              <strong>{Object.values(data?.catalog?.missing_translations ?? {}).reduce<number>((a, b) => a + (b ?? 0), 0)}</strong></li>
          </ul>
        </div>

        <div className="card">
          <h2>{t('dashboard.by_status')}</h2>
          <ul className="recent">
            {Object.entries(data?.orders.by_status ?? {}).map(([status, count]) => (
              <li key={status} className="recent__item">
                <OrderStatusPill code={status} />
                <strong className="recent__date" style={{ textAlign: 'right' }}>
                  {count}
                </strong>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <Modal open={!!openProduct} title={productFull ? `${t('products.editor')} · ${productFull.sku}` : t('table.loading')} onClose={() => setOpenProduct(null)} width={860}>
        {openProduct && (productFull
          ? <ProductEditor key={openProduct} product={productFull} onCancel={() => setOpenProduct(null)} onSaved={() => setOpenProduct(null)} />
          : <p>{t('table.loading')}</p>)}
      </Modal>
    </section>
  );
}

export default DashboardPage;
