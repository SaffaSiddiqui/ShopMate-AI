import { useEffect, useRef, useState } from 'react'
import { Bell, ChevronDown, Menu, Search } from 'lucide-react'

export default function Topbar({ onMenu, onSearch, onNavigate, activePage }) {
  const [searchOpen, setSearchOpen] = useState(false)
  const searchInput = useRef(null)

  useEffect(() => {
    const handleShortcut = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        setSearchOpen(true)
        searchInput.current?.focus()
      }
      if (event.key === 'Escape') {
        setSearchOpen(false)
        searchInput.current?.blur()
      }
    }
    window.addEventListener('keydown', handleShortcut)
    return () => window.removeEventListener('keydown', handleShortcut)
  }, [])

  return (
    <header className="topbar">
      <button className="icon-button menu-button" onClick={onMenu} aria-label="Open navigation"><Menu size={20} /></button>
      <div className="breadcrumb"><span>Workspace</span><span className="crumb-slash">/</span><strong>{activePage}</strong></div>
      <div className="topbar-actions">
        <label className={`global-search ${searchOpen ? 'search-open' : ''}`}>
          <Search size={16} />
          <input ref={searchInput} type="search" placeholder="Search anything..." onChange={(event) => onSearch(event.target.value)} />
          <kbd>⌘ K</kbd>
        </label>
        <button className="icon-button mobile-search-trigger" onClick={() => { setSearchOpen(true); searchInput.current?.focus() }} aria-label="Search"><Search size={18} /></button>
        <button className="icon-button notification-button" aria-label="Notifications" onClick={() => onNavigate('Orders')}>
          <Bell size={18} /><i />
        </button>
        <div className="topbar-divider" />
        <button className="topbar-user" onClick={() => onNavigate('Settings')}>
          <span className="profile-avatar small-avatar">MK</span><ChevronDown size={15} className="muted-icon" />
        </button>
      </div>
    </header>
  )
}
