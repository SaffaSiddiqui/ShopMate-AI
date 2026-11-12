import {
  Boxes,
  ChartNoAxesCombined,
  ChevronDown,
  CircleHelp,
  LayoutDashboard,
  LifeBuoy,
  Package,
  Settings2,
  ShoppingBag,
  Sparkles,
  UsersRound,
  X,
} from 'lucide-react'
import { navigation } from '../data.js'

const iconMap = {
  LayoutDashboard,
  Sparkles,
  Package,
  ShoppingBag,
  Boxes,
  UsersRound,
  ChartNoAxesCombined,
}
export default function Sidebar({ activePage, onNavigate, open, onClose, productsCount, ordersCount }) {
  return (
    <>
      {open && <button className="sidebar-backdrop" onClick={onClose} aria-label="Close navigation" />}
      <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}>
        <div className="brand-row">
          <div className="brand-mark"><span className="brand-mark-inner">s</span></div>
          <span className="brand-name">shopmate<span className="brand-ai">.ai</span></span>
          <button className="icon-button mobile-close" onClick={onClose} aria-label="Close menu"><X size={18} /></button>
        </div>

        <button className="store-switcher" onClick={() => onNavigate('Settings')}>
          <div className="store-avatar">K</div>
          <span className="store-copy"><strong>Khan's General Store</strong><small>Free plan</small></span>
          <ChevronDown size={16} className="muted-icon" />
        </button>

        <nav className="side-nav" aria-label="Main navigation">
          {navigation.map((group) => (
            <div className="nav-group" key={group.title}>
              <p className="nav-heading">{group.title}</p>
              {group.items.map(({ label, icon, badge, count, dot }) => {
                const Icon = iconMap[icon]
                const itemCount = label === 'Products' ? productsCount : label === 'Orders' ? ordersCount : count
                return (
                <button
                  key={label}
                  className={`nav-item ${activePage === label ? 'nav-item-active' : ''}`}
                  onClick={() => { onNavigate(label); onClose() }}
                >
                  <Icon size={18} strokeWidth={1.8} />
                  <span>{label}</span>
                  {badge && <span className="nav-ai-badge">{badge}</span>}
                  {itemCount != null && <span className="nav-count">{itemCount}</span>}
                  {dot && <span className="nav-alert-dot" />}
                </button>
                )
              })}
            </div>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon"><Sparkles size={16} /></div>
            <strong>Work smarter with AI</strong>
            <p>Let your AI assistant handle the busywork.</p>
            <button onClick={() => onNavigate('AI Assistant')}>Explore assistant <span>→</span></button>
          </div>
          <button className="utility-link" onClick={() => onNavigate('Help & support')}><CircleHelp size={17} /> Help & support</button>
          <button className="utility-link" onClick={() => onNavigate('Settings')}><Settings2 size={17} /> Settings</button>
          <div className="profile-row">
            <div className="profile-avatar">MK</div>
            <div className="profile-copy"><strong>Muhammad Khan</strong><small>Store owner</small></div>
            <button className="icon-button" aria-label="Open account menu" onClick={() => onNavigate('Settings')}><LifeBuoy size={17} /></button>
          </div>
        </div>
      </aside>
    </>
  )
}
