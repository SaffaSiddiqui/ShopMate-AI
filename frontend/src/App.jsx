import { useEffect, useMemo, useState } from 'react'
import {
  ArrowDownToLine,
  ArrowRight,
  ArrowUpRight,
  Boxes,
  Check,
  ChevronDown,
  CirclePlus,
  Clock3,
  CreditCard,
  MessageCircle,
  MoreHorizontal,
  Package,
  Plus,
  Search,
  Send,
  ShoppingBag,
  Sparkles,
  TrendingUp,
  UsersRound,
  Wallet,
  Wifi,
  WifiOff,
  X,
} from 'lucide-react'
import Sidebar from './components/Sidebar.jsx'
import Topbar from './components/Topbar.jsx'
import MetricCard from './components/MetricCard.jsx'
import GuideChatbot from './components/GuideChatbot.jsx'
import { customers as initialCustomers, orders as initialOrders, products as initialProducts, salesData as initialSalesData } from './data.js'
import { api } from './api.js'

const money = (amount) => `Rs. ${Number(amount).toLocaleString('en-PK')}`
const todayLabel = new Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).format(new Date()).toUpperCase()
const getChartData = (range) => range === '7 days'
  ? initialSalesData
  : [
    { day: 'Week 1', sales: 39700, orders: 51 },
    { day: 'Week 2', sales: 42100, orders: 58 },
    { day: 'Week 3', sales: 45600, orders: 65 },
    { day: 'Week 4', sales: 46850, orders: 74 },
  ]

function SectionHeading({ title, subtitle, action, onAction }) {
  return (
    <div className="section-heading">
      <div><h2>{title}</h2>{subtitle && <p>{subtitle}</p>}</div>
      {action && <button className="text-action" onClick={onAction}>{action}<ArrowRight size={15} /></button>}
    </div>
  )
}

function Avatar({ initials, color = 'blue' }) {
  return <span className={`customer-avatar avatar-${color}`}>{initials}</span>
}

function StatusBadge({ status }) {
  return <span className={`status-badge status-${status.toLowerCase()}`}><i />{status}</span>
}

function SalesChart({ data, tall = false }) {
  const width = 700
  const height = tall ? 250 : 155
  const left = 44
  const right = 9
  const top = 10
  const bottom = 23
  const maxValue = Math.ceil(Math.max(...data.map((item) => item.sales)) / 10000) * 10000
  const x = (index) => left + index * (width - left - right) / Math.max(data.length - 1, 1)
  const y = (value) => top + (maxValue - value) * (height - top - bottom) / maxValue
  const line = data.map((item, index) => `${index ? 'L' : 'M'} ${x(index)} ${y(item.sales)}`).join(' ')
  const area = `${line} L ${x(data.length - 1)} ${height - bottom} L ${left} ${height - bottom} Z`

  return (
    <div className={`chart-container ${tall ? 'chart-tall' : ''}`}>
      <svg className="sales-chart-svg" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Sales by day">
        <defs><linearGradient id={tall ? 'analyticsFill' : 'salesFill'} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#5185f5" stopOpacity=".19" /><stop offset="100%" stopColor="#5185f5" stopOpacity="0" /></linearGradient></defs>
        {[0, 0.5, 1].map((fraction) => {
          const value = maxValue * fraction
          const yPosition = y(value)
          return <g key={fraction}><line x1={left} x2={width - right} y1={yPosition} y2={yPosition} stroke="#edf0f5" /><text x={left - 7} y={yPosition + 3} textAnchor="end" className="chart-axis-label">{value === 0 ? '0' : `${Math.round(value / 1000)}k`}</text></g>
        })}
        <path d={area} fill={`url(#${tall ? 'analyticsFill' : 'salesFill'})`} />
        <path d={line} fill="none" stroke="#4778ed" strokeWidth="2.5" vectorEffect="non-scaling-stroke" />
        {data.map((item, index) => <g key={item.day}><title>{`${item.day}: ${money(item.sales)}`}</title><circle cx={x(index)} cy={y(item.sales)} r="3.5" fill="#4778ed" stroke="#fff" strokeWidth="2" vectorEffect="non-scaling-stroke" /></g>)}
        {data.map((item, index) => <text key={item.day} x={x(index)} y={height - 5} textAnchor="middle" className="chart-axis-label">{item.day}</text>)}
      </svg>
    </div>
  )
}

function Dashboard({ onNavigate, onAddProduct, range, setRange, query, orders, products, backendConnected, salesTrend }) {
  const chartData = salesTrend ?? getChartData(range)
  const chartTotal = chartData.reduce((total, item) => total + item.sales, 0)
  const peakSalesDay = chartData.reduce((peak, item) => item.sales > peak.sales ? item : peak)
  const filteredOrders = orders.filter((order) => `${order.id} ${order.customer} ${order.item}`.toLowerCase().includes(query.toLowerCase())).slice(0, 5)
  const topProducts = [...products].sort((a, b) => b.sold - a.sold).slice(0, 3)
  const lowStockCount = products.filter((product) => product.stock < 10).length

  return (
    <>
      <div className="welcome-row">
        <div><div className="eyebrow"><span className="live-dot" /> {todayLabel}</div><h1>Good morning, Muhammad <span className="wave">✦</span></h1><p>Here&apos;s what&apos;s happening with your store today.</p></div>
        <div className="action-cluster">
          <span className={`status-badge ${backendConnected ? 'status-delivered' : 'status-processing'}`} style={{ padding: '6px 12px', fontSize: '13px' }}>
            <i /> {backendConnected ? 'FastAPI Connected' : 'Local Demo Mode'}
          </span>
          <button className="primary-button" onClick={onAddProduct}><Plus size={16} /> Add product</button>
        </div>
      </div>

      <div className="metrics-grid">
        <MetricCard title="Total sales" label="Total sales" value={money(chartTotal)} change="+12.8%" tone="up" note="vs last week" helper="vs last week" icon={Wallet} />
        <MetricCard title="Total orders" label="Total orders" value={orders.length} change="+8.2%" tone="up" note="across all items" helper="across all items" icon={ShoppingBag} />
        <MetricCard title="Total products" label="Total products" value={products.length} change="+8.3%" tone="up" note="in store catalogue" helper="in store catalogue" icon={Package} />
        <MetricCard title="Low stock alerts" label="Low stock alerts" value={lowStockCount} tone={lowStockCount ? 'down' : 'neutral'} note={lowStockCount ? 'need restocking' : 'shelves healthy'} helper={lowStockCount ? 'need restocking' : 'shelves healthy'} icon={Boxes} />
      </div>

      <div className="dashboard-grid">
        <div className="stack-column">
          <section className="panel chart-panel">
            <div className="panel-heading">
              <div><span className="panel-kicker">REVENUE PERFORMANCE</span><h2>Sales overview</h2><p className="panel-subtitle">Daily earnings in PKR</p></div>
              <label className="select-wrap"><select value={range} onChange={(event) => setRange(event.target.value)}><option>7 days</option><option>30 days</option></select><ChevronDown size={14} /></label>
            </div>
            <div className="chart-summary"><strong>{money(chartTotal)}</strong><span className="summary-change"><ArrowUpRight size={14} /> 12.8%</span><span className="summary-caption">peak: {peakSalesDay.day} ({money(peakSalesDay.sales)})</span></div>
            <SalesChart data={chartData} />
          </section>

          <section className="panel">
            <SectionHeading title="Recent orders" subtitle="Latest store purchases" action="View all orders" onAction={() => onNavigate('Orders')} />
            <OrderTable orders={filteredOrders} />
          </section>
        </div>

        <div className="stack-column side-column">
          <section className="panel ai-feature-panel">
            <div className="ai-feature-tag"><Sparkles size={14} /> ShopMate AI</div>
            <h3>Smart restock recommendation</h3>
            <p>{lowStockCount ? `${lowStockCount} product(s) are running below 10 units. Restock soon to prevent missed sales.` : 'All products are currently well-stocked. Looking good!'}</p>
            <button className="secondary-button" onClick={() => onNavigate('AI Assistant')}>Open AI assistant <ArrowRight size={15} /></button>
          </section>

          <section className="panel">
            <SectionHeading title="Inventory status" subtitle="Items to watch" action="Open inventory" onAction={() => onNavigate('Inventory')} />
            <div className="stock-list">{products.slice(0, 4).map((product) => <StockRow key={product.sku} product={product} />)}</div>
          </section>

          <section className="panel">
            <SectionHeading title="Top selling items" subtitle="By units sold" />
            <div className="top-products-list">
              {topProducts.map((product) => (
                <div className="top-product-row" key={product.sku}>
                  <div className={`product-emoji emoji-${product.color}`}>{product.emoji}</div>
                  <div className="top-product-info"><strong>{product.name}</strong><span>{product.sold} units sold</span></div>
                  <span className="top-product-amount">{money(product.price)}</span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </>
  )
}

function OrderTable({ orders, onStatusChange }) {
  if (!orders.length) return <div className="empty-state"><Search size={22} /><strong>No orders found</strong><span>Try another search term.</span></div>
  return (
    <div className="table-scroll"><table className="data-table">
      <thead><tr><th>ORDER ID</th><th>CUSTOMER</th><th>ITEM</th><th>DATE</th><th>AMOUNT</th><th>STATUS</th><th>NOTIFY</th></tr></thead>
      <tbody>{orders.map((order) => <tr key={order.id}>
        <td className="order-id-cell">{order.id}</td>
        <td><div className="table-customer"><Avatar initials={order.initials} color={order.color} /><span>{order.customer}</span></div></td>
        <td>{order.item}</td>
        <td className="date-cell">{order.date}</td>
        <td className="amount-cell">{money(order.amount)}</td>
        <td>{onStatusChange ? <button className="status-button" onClick={() => onStatusChange(order.id)} title="Click to advance order status"><StatusBadge status={order.status} /></button> : <StatusBadge status={order.status} />}</td>
        <td>
          <button
            className="small-outline-button"
            style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', borderColor: '#25D366', color: '#128C7E', fontSize: '11px', padding: '4px 8px' }}
            title="Send WhatsApp receipt to customer"
            onClick={() => {
              const msg = `Assalam-o-Alaikum ${order.customer}! Your order ${order.id} for "${order.item}" totaling Rs. ${Number(order.amount).toLocaleString('en-PK')} is currently [${order.status}]. Thank you for shopping with Khan's General Store (ShopMate AI)!`
              sendWhatsAppMessage(order.phone || '03001234567', msg)
            }}
          >
            <MessageCircle size={13} /> Receipt
          </button>
        </td>
      </tr>)}</tbody>
    </table></div>
  )
}

function StockRow({ product }) {
  const low = product.stock < 10
  return <div className="stock-row"><div className={`product-emoji emoji-${product.color}`}>{product.emoji}</div><div className="stock-info"><strong>{product.name}</strong><span>{product.sku}</span></div><div className="stock-quantity"><strong className={low ? 'stock-critical' : ''}>{product.stock} left</strong><span className={`stock-pill ${low ? 'pill-critical' : ''}`}>{low ? 'Low stock' : 'Running low'}</span></div></div>
}

function ProductsPage({ products, query, onAddProduct, onRestock }) {
  const filtered = products.filter((p) => `${p.name} ${p.sku} ${p.category}`.toLowerCase().includes(query.toLowerCase()))
  return <div className="page-stack">
    <div className="page-title-row"><div><div className="eyebrow">YOUR CATALOGUE</div><h1>Products</h1><p>Manage your products, prices, and stock levels.</p></div><button className="primary-button" onClick={onAddProduct}><Plus size={17} /> Add product</button></div>
    <div className="mini-metrics"><MiniMetric icon={Package} label="Total products" value={products.length} /><MiniMetric icon={Boxes} label="Low stock" value={products.filter((p) => p.stock < 10).length} tone="orange" /><MiniMetric icon={Wallet} label="Catalogue value" value={money(products.reduce((sum, p) => sum + p.price * p.stock, 0))} /></div>
    <section className="panel full-panel"><div className="list-toolbar"><div><h2>All products <span className="count-chip">{filtered.length}</span></h2><p>Your store catalogue at a glance</p></div><div className="table-search"><Search size={15} /><span>Use the top search to filter</span></div></div>
      <div className="table-scroll"><table className="data-table product-table"><thead><tr><th>PRODUCT</th><th>SKU</th><th>CATEGORY</th><th>PRICE</th><th>STOCK</th><th>ACTION</th></tr></thead>
        <tbody>{filtered.map((product) => <tr key={product.sku}><td><div className="table-customer"><div className={`product-emoji emoji-${product.color}`}>{product.emoji}</div><strong>{product.name}</strong></div></td><td className="sku-cell">{product.sku}</td><td>{product.category}</td><td className="amount-cell">{money(product.price)}</td><td><span className={product.stock < 10 ? 'stock-number-low' : 'stock-number'}>{product.stock} units</span></td><td><button className="small-outline-button" onClick={() => onRestock(product.sku)}>Restock (+20)</button></td></tr>)}</tbody>
      </table></div>
      {!filtered.length && <div className="empty-state"><Search size={22} /><strong>No products found</strong><span>Try another search.</span></div>}
    </section>
  </div>
}

function OrdersPage({ orders, query, onStatusChange, onCreateOrder }) {
  const filtered = orders.filter((o) => `${o.id} ${o.customer} ${o.item} ${o.status}`.toLowerCase().includes(query.toLowerCase()))
  return <div className="page-stack">
    <div className="page-title-row"><div><div className="eyebrow">SALES & FULFILMENT</div><h1>Orders</h1><p>View and manage orders from your customers.</p></div><button className="primary-button" onClick={onCreateOrder}><CirclePlus size={17} /> Create order</button></div>
    <div className="mini-metrics"><MiniMetric icon={ShoppingBag} label="All orders" value={orders.length} /><MiniMetric icon={Clock3} label="Processing" value={orders.filter((o) => o.status === 'Processing').length} tone="orange" /><MiniMetric icon={Check} label="Delivered" value={orders.filter((o) => o.status === 'Delivered').length} tone="green" /></div>
    <section className="panel full-panel"><div className="list-toolbar"><div><h2>All orders <span className="count-chip">{filtered.length}</span></h2><p>Click an order status to advance its progress</p></div><span className="list-note"><span className="live-dot" /> Live updates</span></div><OrderTable orders={filtered} onStatusChange={onStatusChange} /></section>
  </div>
}

function InventoryPage({ products, onRestock }) {
  const attention = products.filter((product) => product.stock < 15)
  return <div className="page-stack">
    <div className="page-title-row"><div><div className="eyebrow">STOCK CONTROL</div><h1>Inventory</h1><p>Stay ahead of stockouts and keep your shelves ready.</p></div><button className="secondary-button" onClick={() => window.print()}><ArrowDownToLine size={16} /> Print report</button></div>
    <div className="mini-metrics"><MiniMetric icon={Boxes} label="Total units" value={products.reduce((sum, product) => sum + product.stock, 0)} /><MiniMetric icon={TrendingUp} label="Well stocked" value={products.filter((product) => product.stock >= 15).length} tone="green" /><MiniMetric icon={Clock3} label="Needs attention" value={attention.length} tone="orange" /></div>
    <section className="panel full-panel"><div className="list-toolbar"><div><h2>Stock levels</h2><p>Restock items before they run out</p></div></div><div className="inventory-list">{products.map((product) => <div className="inventory-item" key={product.sku}><div className={`product-emoji emoji-${product.color}`}>{product.emoji}</div><div className="inventory-product"><strong>{product.name}</strong><span>{product.sku} · {product.category}</span></div><div className="inventory-progress"><div className="progress-meta"><span>Stock level</span><strong className={product.stock < 10 ? 'stock-critical' : ''}>{product.stock} units</strong></div><div className="progress-track"><span className={product.stock < 10 ? 'progress-low' : ''} style={{ width: `${Math.min(product.stock * 2, 100)}%` }} /></div></div><span className={`inventory-tag ${product.stock < 10 ? 'tag-low' : product.stock < 15 ? 'tag-watch' : 'tag-good'}`}>{product.stock < 10 ? 'Low stock' : product.stock < 15 ? 'Running low' : 'In stock'}</span><button className="small-outline-button" onClick={() => onRestock(product.sku)}>Restock (+20)</button></div>)}</div></section>
  </div>
}

// Helper to launch WhatsApp directly with localized Pakistani formatting
function sendWhatsAppMessage(phone, message) {
  let cleaned = (phone || '').replace(/[^0-9]/g, '')
  if (cleaned.startsWith('0')) {
    cleaned = '92' + cleaned.slice(1)
  } else if (!cleaned.startsWith('92') && cleaned.length === 10) {
    cleaned = '92' + cleaned
  }
  const url = `https://wa.me/${cleaned}?text=${encodeURIComponent(message)}`
  window.open(url, '_blank')
}

function CustomersPage({ query, customers }) {
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [customMsg, setCustomMsg] = useState('')
  const filtered = customers.filter((customer) => `${customer.name} ${customer.city} ${customer.phone}`.toLowerCase().includes(query.toLowerCase()))

  const openWhatsAppDialog = (customer) => {
    setSelectedCustomer(customer)
    setCustomMsg(`Assalam-o-Alaikum ${customer.name}! Thank you for being a valued customer at Khan's General Store. We have an exclusive 10% discount on your next order!`)
  }

  const handleSend = (e) => {
    e.preventDefault()
    if (selectedCustomer) {
      sendWhatsAppMessage(selectedCustomer.phone, customMsg)
      setSelectedCustomer(null)
    }
  }

  return <div className="page-stack">
    <div className="page-title-row"><div><div className="eyebrow">PEOPLE WHO LOVE YOUR STORE</div><h1>Customers</h1><p>Get to know the community behind your business.</p></div><button className="secondary-button" onClick={() => downloadCsv('shopmate-customers.csv', ['Name,Phone,City,Orders,Total spent', ...customers.map((c) => `${c.name},${c.phone},${c.city},${c.orders},${c.spent}`)].join('\n'))}><ArrowDownToLine size={16} /> Export customers</button></div>
    <div className="mini-metrics"><MiniMetric icon={UsersRound} label="Total customers" value={customers.length} /><MiniMetric icon={TrendingUp} label="Returning customers" value="68%" tone="green" /><MiniMetric icon={Wallet} label="Average lifetime value" value="Rs. 8,240" /></div>
    <section className="panel full-panel"><div className="list-toolbar"><div><h2>Customer directory <span className="count-chip">{filtered.length}</span></h2><p>Your most recently active customers</p></div><span className="list-note"><span className="live-dot" /> WhatsApp Ready</span></div><div className="table-scroll"><table className="data-table"><thead><tr><th>CUSTOMER</th><th>PHONE</th><th>CITY</th><th>ORDERS</th><th>TOTAL SPENT</th><th>WHATSAPP</th></tr></thead><tbody>{filtered.map((customer) => <tr key={customer.phone}><td><div className="table-customer"><Avatar initials={customer.initials} color={customer.color} /><strong>{customer.name}</strong></div></td><td className="sku-cell">{customer.phone}</td><td>{customer.city}</td><td>{customer.orders} orders</td><td className="amount-cell">{money(customer.spent)}</td><td><button className="small-outline-button" style={{ display: 'inline-flex', alignItems: 'center', gap: '5px', borderColor: '#25D366', color: '#128C7E' }} onClick={() => openWhatsAppDialog(customer)}><MessageCircle size={14} /> WhatsApp</button></td></tr>)}</tbody></table></div>{!filtered.length && <div className="empty-state"><Search size={22} /><strong>No customers found</strong><span>Try another search.</span></div>}</section>
    {selectedCustomer && (
      <Modal title={`Send WhatsApp to ${selectedCustomer.name}`} onClose={() => setSelectedCustomer(null)}>
        <form className="modal-form" onSubmit={handleSend}>
          <p className="modal-copy">Recipient: <strong>{selectedCustomer.name}</strong> ({selectedCustomer.phone})</p>
          <label>Message text
            <textarea
              required
              rows={4}
              value={customMsg}
              onChange={(e) => setCustomMsg(e.target.value)}
              style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '13px' }}
            />
          </label>
          <div className="modal-actions">
            <button type="button" className="secondary-button" onClick={() => setSelectedCustomer(null)}>Cancel</button>
            <button type="submit" className="primary-button" style={{ backgroundColor: '#25D366', borderColor: '#25D366' }}>
              <Send size={15} /> Open in WhatsApp
            </button>
          </div>
        </form>
      </Modal>
    )}
  </div>
}

function AnalyticsPage({ range, setRange, products, salesTrend }) {
  const rows = salesTrend ?? getChartData(range)
  const grossSales = rows.reduce((total, row) => total + row.sales, 0)
  const orderCount = rows.reduce((total, row) => total + row.orders, 0)
  const averageOrderValue = orderCount ? Math.round(grossSales / orderCount) : 0
  const peakSalesDay = rows.reduce((peak, row) => row.sales > peak.sales ? row : peak)
  return <div className="page-stack">
    <div className="page-title-row"><div><div className="eyebrow">YOUR BUSINESS AT A GLANCE</div><h1>Sales analytics</h1><p>Understand what&apos;s working and spot your next opportunity.</p></div><button className="secondary-button" onClick={() => downloadCsv('shopmate-sales.csv', ['Day,Sales (PKR),Orders', ...rows.map((r) => `${r.day},${r.sales},${r.orders}`)].join('\n'))}><ArrowDownToLine size={16} /> Export report</button></div>
    <div className="mini-metrics"><MiniMetric icon={Wallet} label="Gross sales" value={money(grossSales)} /><MiniMetric icon={ShoppingBag} label="Total orders" value={orderCount} tone="violet" /><MiniMetric icon={CreditCard} label="Average order value" value={money(averageOrderValue)} tone="orange" /></div>
    <section className="panel full-panel analytics-chart-panel"><div className="panel-heading"><div><span className="panel-kicker">PERFORMANCE</span><h2>Sales over time</h2><p className="panel-subtitle">Revenue from your store</p></div><label className="select-wrap"><select value={range} onChange={(event) => setRange(event.target.value)}><option>7 days</option><option>30 days</option></select><ChevronDown size={14} /></label></div><div className="chart-summary"><strong>{money(grossSales)}</strong><span className="summary-change"><ArrowUpRight size={14} /> 12.8%</span><span className="summary-caption">compared to last period</span></div><SalesChart data={rows} tall /></section>
    <section className="panel category-panel"><SectionHeading title="Store snapshot" subtitle="A quick look at your catalogue" /><div className="snapshot-grid"><div><span>Active products</span><strong>{products.length}</strong><small>Across {new Set(products.map((p) => p.category)).size} categories</small></div><div><span>Stock to replenish</span><strong>{products.filter((p) => p.stock < 10).length}</strong><small>Products below 10 units</small></div><div><span>Top selling day</span><strong>{peakSalesDay.day}</strong><small>{money(peakSalesDay.sales)} in sales</small></div></div></section>
  </div>
}

function MiniMetric({ icon: Icon, label, value, tone = 'blue' }) {
  return <div className="mini-metric"><span className={`metric-icon metric-${tone}`}><Icon size={18} /></span><div><span>{label}</span><strong>{value}</strong></div></div>
}

const suggestedPrompts = ['How can I improve sales this week?', 'Which products should I restock?', 'Summarize my store performance']

function AssistantPage({ products, orders, customers = [], backendConnected, salesTrend }) {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [thinking, setThinking] = useState(false)

  const ask = async (text) => {
    const trimmed = text.trim()
    if (!trimmed || thinking) return
    setMessage('')
    setThinking(true)

    // Optimistically add user question with thinking placeholder
    const question = trimmed
    setMessages((current) => [...current, { question, answer: '✦ ShopMate AI is analyzing your store...', isThinking: true }])

    try {
      // Call backend AI agent endpoint
      const response = await api.chatWithAgent(trimmed)
      if (response && response.reply) {
        setMessages((current) =>
          current.map((item, idx) =>
            idx === current.length - 1 ? { question, answer: response.reply, isThinking: false } : item
          )
        )
      } else {
        throw new Error('No reply from agent')
      }
    } catch {
      // Graceful local fallback using actual store data if backend is offline or errors
      let response = 'A good next step is to review your best-selling products, reach out to returning customers, and keep an eye on your weekly sales trend.'
      if (/stock|restock|inventory|shortage/i.test(trimmed)) {
        const low = products.filter((product) => product.stock < 10).map((product) => `${product.name} (${product.stock} left)`)
        response = low.length ? `I found ${low.length} product${low.length === 1 ? '' : 's'} running low on stock: ${low.join(', ')}. Consider restocking these soon to avoid missing sales.` : 'Your current products are looking well stocked above 10 units. Keep checking inventory as new orders come in.'
      } else if (/sales|revenue|performance|week|growth|earning|money/i.test(trimmed)) {
        const rows = salesTrend ?? initialSalesData
        const totalSales = rows.reduce((total, row) => total + row.sales, 0)
        const peakDay = rows.reduce((peak, row) => row.sales > peak.sales ? row : peak)
        response = `Your store recorded ${money(totalSales)} in sales this period. ${peakDay.day} was your strongest day at ${money(peakDay.sales)}. You have ${orders.filter((order) => order.status === 'Processing').length} orders currently being processed.`
      } else if (/order|fulfillment|processing|shipped|deliver/i.test(trimmed)) {
        const proc = orders.filter((o) => o.status === 'Processing').length
        const deliv = orders.filter((o) => o.status === 'Delivered').length
        response = `You have ${orders.length} total orders: ${deliv} delivered and ${proc} currently processing. Fulfilling pending orders quickly boosts repeat business.`
      } else if (/customer|buyer|shopper|loyalty|client/i.test(trimmed)) {
        const topCust = [...customers].sort((a, b) => (b.spent || 0) - (a.spent || 0))[0]
        response = `You have ${customers.length} registered customers. ${topCust ? `Your top customer is ${topCust.name} (${money(topCust.spent)} spent, ${topCust.orders} orders). ` : ''}Repeat customers account for approximately 68% of your store visits. Consider a friendly WhatsApp follow-up.`
      } else if (/product|catalog|item|sku|best seller|top/i.test(trimmed)) {
        const best = [...products].sort((a, b) => (b.sold || 0) - (a.sold || 0))[0]
        response = `Your store catalogue has ${products.length} products. ${best ? `Your top-selling product is ${best.name} with ${best.sold} units sold.` : ''} Keep high-demand SKUs well-stocked.`
      }
      setMessages((current) =>
        current.map((item, idx) =>
          idx === current.length - 1 ? { question, answer: response, isThinking: false } : item
        )
      )
    } finally {
      setThinking(false)
    }
  }

  return <div className="page-stack assistant-page">
    <div className="page-title-row"><div><div className="eyebrow"><span className="live-dot" /> YOUR BUSINESS PARTNER</div><h1>AI Assistant</h1><p>Ask a question about your store and get real-time recommendations.</p></div><span className="ai-ready"><span className="live-dot" /> {backendConnected ? 'Connected to Backend Agent' : 'Local demo assistant'}</span></div>
    <section className="panel chat-panel">
      <div className="chat-welcome"><div className="chat-bot-icon"><Sparkles size={22} /></div><div><h2>Hi Muhammad, how can I help?</h2><p>I analyze your live inventory, order fulfillment, and sales metrics to give you actionable advice.</p></div></div>
      <div className="prompt-grid">{suggestedPrompts.map((prompt) => <button key={prompt} onClick={() => ask(prompt)} disabled={thinking}>{prompt}<ArrowUpRight size={15} /></button>)}</div>
      <div className="chat-messages">{messages.map((item, index) => <div className="chat-pair" key={`${index}-${item.question}`}><div className="user-message">{item.question}</div><div className={`ai-message ${item.isThinking ? 'ai-thinking' : ''}`}><span className="chat-mini-icon"><Sparkles size={14} /></span><p>{item.answer}</p></div></div>)}</div>
      <form className="chat-input-row" onSubmit={(event) => { event.preventDefault(); ask(message) }}><input value={message} onChange={(event) => setMessage(event.target.value)} placeholder={thinking ? "ShopMate AI is thinking..." : "Ask anything about your business..."} aria-label="Message your AI assistant" disabled={thinking} /><button className="send-button" type="submit" disabled={!message.trim() || thinking} aria-label="Send message">{thinking ? <Sparkles size={16} /> : <Send size={17} />}</button></form>
      <p className="chat-disclaimer"><Sparkles size={12} /> {backendConnected ? 'Powered by Google Gemini AI & ShopMate live backend intelligence.' : 'Using sample data; start the backend for live store insights.'}</p>
    </section>
  </div>
}

function GenericPage({ page, onNavigate }) {
  return <div className="page-stack"><div className="page-title-row"><div><div className="eyebrow">SHOPMATE AI</div><h1>{page}</h1><p>Manage your ShopMate AI workspace.</p></div></div><section className="panel generic-panel"><div className="chat-bot-icon"><MessageCircle size={21} /></div><h2>{page === 'Settings' ? 'Your store settings' : 'How can we help?'}</h2><p>{page === 'Settings' ? 'Store profile: Khan’s General Store · Currency: PKR · Time zone: Pakistan Standard Time.' : 'For this demo, connect your store owner account with your usual support channel.'}</p><button className="secondary-button" onClick={() => onNavigate('Overview')}>Back to overview <ArrowRight size={15} /></button></section></div>
}

function Modal({ title, onClose, children }) {
  return <div className="modal-overlay" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose() }}><section className="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-title"><div className="modal-heading"><h2 id="modal-title">{title}</h2><button className="icon-button" onClick={onClose} aria-label="Close dialog"><X size={18} /></button></div>{children}</section></div>
}

function ProductModal({ onClose, onSave }) {
  const [name, setName] = useState('')
  const [category, setCategory] = useState('Grocery')
  const [price, setPrice] = useState('')
  const [stock, setStock] = useState('')
  const submit = async (event) => { event.preventDefault(); if (await onSave({ name: name.trim(), category, price: Number(price), stock: Number(stock) })) onClose() }
  return <Modal title="Add a product" onClose={onClose}><form className="modal-form" onSubmit={submit}><label>Product name<input required value={name} onChange={(event) => setName(event.target.value)} placeholder="e.g. Lahore Chana Masala" /></label><div className="form-two-col"><label>Category<select value={category} onChange={(event) => setCategory(event.target.value)}><option>Grocery</option><option>Clothing</option><option>Beverages</option><option>Footwear</option><option>Home goods</option></select></label><label>Price (PKR)<input required type="number" min="1" value={price} onChange={(event) => setPrice(event.target.value)} placeholder="1250" /></label></div><label>Starting stock<input required type="number" min="0" value={stock} onChange={(event) => setStock(event.target.value)} placeholder="20" /></label><div className="modal-actions"><button type="button" className="secondary-button" onClick={onClose}>Cancel</button><button type="submit" className="primary-button"><Plus size={15} /> Save product</button></div></form></Modal>
}

function CreateOrderModal({ onClose, onSave, products }) {
  const [customer, setCustomer] = useState('')
  const availableProducts = products.filter((entry) => entry.stock > 0)
  const [productSku, setProductSku] = useState(availableProducts[0]?.sku ?? '')
  const [quantity, setQuantity] = useState(1)
  const product = availableProducts.find((entry) => entry.sku === productSku)
  return <Modal title="Create an order" onClose={onClose}><form className="modal-form" onSubmit={async (event) => { event.preventDefault(); if (await onSave(customer.trim(), product, Number(quantity))) onClose() }}><label>Customer name<input required value={customer} onChange={(event) => setCustomer(event.target.value)} placeholder="e.g. Sana Iqbal" /></label><label>Product<select required value={productSku} onChange={(event) => setProductSku(event.target.value)} disabled={!availableProducts.length}>{availableProducts.map((entry) => <option key={entry.sku} value={entry.sku}>{entry.name} — {money(entry.price)} ({entry.stock} in stock)</option>)}</select></label>{!availableProducts.length && <p className="modal-copy">No products are currently in stock. Restock a product before creating an order.</p>}<label>Quantity<input required type="number" min="1" max={product?.stock ?? 1} value={quantity} onChange={(event) => setQuantity(event.target.value)} disabled={!product} /></label><div className="modal-actions"><button type="button" className="secondary-button" onClick={onClose}>Cancel</button><button type="submit" className="primary-button" disabled={!product}><CirclePlus size={15} /> Create order</button></div></form></Modal>
}

function downloadCsv(filename, contents) {
  const blob = new Blob([contents], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

export default function App() {
  const [activePage, setActivePage] = useState('Overview')
  const [menuOpen, setMenuOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [range, setRange] = useState('7 days')
  const [products, setProducts] = useState(initialProducts)
  const [orders, setOrders] = useState(initialOrders)
  const [customers, setCustomers] = useState(initialCustomers)
  const [salesTrend, setSalesTrend] = useState(null)
  const [modal, setModal] = useState('')
  const [backendConnected, setBackendConnected] = useState(false)
  const [actionError, setActionError] = useState('')

  // Load initial state from FastAPI Backend
  useEffect(() => {
    let isMounted = true

    async function loadBackendData() {
      const [isHealthy, backendProducts, backendOrders, backendCustomers] = await Promise.all([
        api.checkHealth(),
        api.getProducts().catch(() => null),
        api.getOrders().catch(() => null),
        api.getCustomers().catch(() => null),
      ])

      if (!isMounted) return
      setBackendConnected(isHealthy)
      if (Array.isArray(backendProducts)) setProducts(backendProducts)
      if (Array.isArray(backendOrders)) setOrders(backendOrders)
      if (Array.isArray(backendCustomers)) setCustomers(backendCustomers)
    }

    loadBackendData()
    return () => { isMounted = false }
  }, [])

  useEffect(() => {
    let isMounted = true
    setSalesTrend(null)
    api.getSalesTrend(range)
      .then((rows) => {
        if (isMounted && Array.isArray(rows)) {
          setSalesTrend(rows)
          setBackendConnected(true)
        }
      })
      .catch(() => {
        if (isMounted) setSalesTrend(null)
      })
    return () => { isMounted = false }
  }, [range])

  const addProduct = async (product) => {
    const sku = `SM-${crypto.randomUUID().replace(/-/g, '').slice(0, 8).toUpperCase()}`
    const productPayload = {
      ...product,
      sku,
      sold: 0,
      emoji: '🛍️',
      color: 'mint',
    }

    try {
      const created = await api.createProduct(productPayload)
      setProducts((current) => [...current, created])
      setBackendConnected(true)
      return true
    } catch {
      if (backendConnected) {
        setActionError('Could not save the product to the database. Please try again.')
        return false
      }
      setProducts((current) => [...current, productPayload])
      return true
    }
  }

  const handleRestock = async (sku) => {
    try {
      const result = await api.restockProduct(sku, 20)
      setProducts((current) =>
        current.map((p) => (p.sku === sku ? { ...p, stock: result.stock } : p))
      )
      setBackendConnected(true)
    } catch {
      if (backendConnected) {
        setActionError('Could not update stock in the database. Please try again.')
        return
      }
      setProducts((current) =>
        current.map((p) => (p.sku === sku ? { ...p, stock: p.stock + 20 } : p))
      )
    }
  }

  const createOrder = async (customer, product, quantity) => {
    if (!product) return
    const initials = customer.split(/\s+/).slice(0, 2).map((part) => part[0]?.toUpperCase()).join('')
    const orderPayload = {
      customer,
      initials: initials || 'CU',
      item: product.name,
      amount: product.price * quantity,
      product_sku: product.sku,
      quantity,
      status: 'Processing',
      color: 'blue',
    }

    try {
      const created = await api.createOrder(orderPayload)
      setOrders((current) => [created, ...current])
      setProducts((current) =>
        current.map((entry) =>
          entry.sku === product.sku ? { ...entry, stock: Math.max(0, entry.stock - quantity) } : entry
        )
      )
      setBackendConnected(true)
      return true
    } catch {
      if (backendConnected) {
        setActionError('Could not create the order. Check available stock and try again.')
        return false
      }
      const newOrder = {
        ...orderPayload,
        id: `#SM-${2085 + orders.length - initialOrders.length}`,
        date: 'Just now',
      }
      setOrders((current) => [newOrder, ...current])
      setProducts((current) =>
        current.map((entry) =>
          entry.sku === product.sku ? { ...entry, stock: Math.max(0, entry.stock - quantity) } : entry
        )
      )
      return true
    }
  }

  const handleStatusChange = async (id) => {
    const order = orders.find((o) => o.id === id)
    if (!order) return
    const nextStatus =
      order.status === 'Processing'
        ? 'Shipped'
        : order.status === 'Shipped'
        ? 'Delivered'
        : 'Processing'

    try {
      const updated = await api.updateOrderStatus(id, nextStatus)
      setOrders((current) =>
        current.map((o) => (o.id === id ? { ...o, status: updated.status } : o))
      )
      setBackendConnected(true)
    } catch {
      if (backendConnected) {
        setActionError('Could not update the order status in the database. Please try again.')
        return
      }
      setOrders((current) =>
        current.map((o) => (o.id === id ? { ...o, status: nextStatus } : o))
      )
    }
  }

  const page = activePage
  const content = useMemo(() => {
    if (page === 'Overview') return <Dashboard onNavigate={setActivePage} onAddProduct={() => setModal('product')} range={range} setRange={setRange} query={search} orders={orders} products={products} backendConnected={backendConnected} salesTrend={salesTrend} />
    if (page === 'Products') return <ProductsPage products={products} query={search} onAddProduct={() => setModal('product')} onRestock={handleRestock} />
    if (page === 'Orders') return <OrdersPage orders={orders} query={search} onCreateOrder={() => setModal('order')} onStatusChange={handleStatusChange} />
    if (page === 'Inventory') return <InventoryPage products={products} onRestock={handleRestock} />
    if (page === 'Customers') return <CustomersPage query={search} customers={customers} />
    if (page === 'Analytics') return <AnalyticsPage range={range} setRange={setRange} products={products} salesTrend={salesTrend} />
    if (page === 'AI Assistant') return <AssistantPage products={products} orders={orders} customers={customers} backendConnected={backendConnected} salesTrend={salesTrend} />
    return <GenericPage page={page} onNavigate={setActivePage} />
  }, [page, search, range, orders, products, customers, backendConnected, salesTrend])

  return <div className="app-shell">
    <Sidebar activePage={activePage} onNavigate={(nextPage) => { setActivePage(nextPage); setSearch('') }} open={menuOpen} onClose={() => setMenuOpen(false)} productsCount={products.length} ordersCount={orders.length} />
    <main className="main-shell">
      <Topbar onMenu={() => setMenuOpen(true)} onSearch={setSearch} onNavigate={setActivePage} activePage={activePage} />
      <div className="main-content" key={activePage}>
        {actionError && <div className="action-error" role="alert">{actionError}<button onClick={() => setActionError('')} aria-label="Dismiss error"><X size={16} /></button></div>}
        {content}
      </div>
      <footer className="app-footer">
        <span>© {new Date().getFullYear()} ShopMate AI</span>
        <span>
          {backendConnected ? (
            <span style={{ color: '#16a34a', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <span className="live-dot" /> Backend API Connected (http://127.0.0.1:8000)
            </span>
          ) : (
            <span>Made for Pakistani businesses <span className="footer-heart">♥</span></span>
          )}
        </span>
        <span>PKR · PKT</span>
      </footer>
    </main>
    {modal === 'product' && <ProductModal onClose={() => setModal('')} onSave={addProduct} />}
    {modal === 'order' && <CreateOrderModal onClose={() => setModal('')} onSave={createOrder} products={products} />}
    <GuideChatbot onNavigate={setActivePage} activePage={activePage} />
  </div>
}
