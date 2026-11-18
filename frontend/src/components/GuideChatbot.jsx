import { useState, useRef, useEffect } from 'react'
import {
  Bot,
  Sparkles,
  X,
  Send,
  MessageSquare,
  HelpCircle,
  Compass,
  ArrowRight,
  ChevronDown,
  Minimize2
} from 'lucide-react'
import { api } from '../api.js'

// Comprehensive knowledge base explaining how to use every aspect of ShopMate AI
const GUIDE_TOPICS = [
  {
    id: 'overview',
    title: '🧭 App Navigation Tour',
    badge: 'Basics',
    reply: `ShopMate AI is your complete retail dashboard tailored for Pakistani SMEs! Here is how to navigate:
• 📊 **Overview**: Live KPIs (sales, orders, stock alerts), revenue graph, and top items.
• 📦 **Products**: View all catalogue items, manage prices, and restock.
• 🛍️ **Orders**: Track incoming orders, change statuses, and send WhatsApp receipts.
• 📋 **Inventory**: Monitor stock levels, low-stock warnings, and print inventory reports.
• 👥 **Customers**: View customer contacts, cities, and lifetime spend.
• 📈 **Analytics**: Explore 7-day and 30-day sales curves, revenue trends, and categories.
• ✦ **AI Assistant**: Live Gemini business advisor for custom queries.

💡 **Pro Tip**: Press **Ctrl + K** (or **⌘ + K**) anytime to instantly search products, orders, or customers.`,
    navTarget: null,
  },
  {
    id: 'add-product',
    title: '➕ How to add a product?',
    badge: 'Products',
    reply: `To add a new product to your catalogue:
1. Click the blue **"+ Add product"** button at the top-right of the Dashboard or Products page.
2. Enter the **Product Name** (e.g., "Shan Biryani Masala").
3. Choose the **Category** (Grocery, Clothing, Beverages, Footwear, Home goods).
4. Enter the **Price in PKR** and **Starting stock quantity**.
5. Click **"Save product"** — it instantly updates your inventory and live store value!`,
    navTarget: 'Products',
    navLabel: 'Go to Products page',
  },
  {
    id: 'whatsapp-receipt',
    title: '🧾 How do WhatsApp receipts work?',
    badge: 'Orders',
    reply: `Sending WhatsApp receipts to your customers is 1-click simple:
1. Go to the **Dashboard** (Recent orders) or the **Orders** page.
2. In the orders table, find the order you want to invoice.
3. Click the green **"Receipt"** button on that row.
4. It automatically opens WhatsApp (web or app) with a pre-filled, professional bilingual receipt containing the Customer Name, Order ID, Purchased Item, PKR Amount, and Order Status!`,
    navTarget: 'Orders',
    navLabel: 'Go to Orders page',
  },
  {
    id: 'restock',
    title: '📦 How to restock low items?',
    badge: 'Inventory',
    reply: `To keep your shelves healthy and avoid stockouts:
1. Check the **"Low stock alerts"** KPI on your dashboard (< 10 units).
2. Head to the **Inventory** or **Products** page.
3. Items running low will have an orange or red tag.
4. Click the **"Restock (+20)"** button on any product row.
5. The stock level increases immediately by 20 units and updates the live store balance!`,
    navTarget: 'Inventory',
    navLabel: 'Go to Inventory page',
  },
  {
    id: 'ai-assistant',
    title: '✦ How to use the AI Assistant?',
    badge: 'AI Advisor',
    reply: `Your ShopMate AI Assistant is powered by Google Gemini:
1. Click **"AI Assistant"** in the left sidebar (or the menu on mobile).
2. You can click any suggested prompt or type a question about:
   • *"Which products should I restock?"*
   • *"How were our sales this week?"*
   • *"Who are our top customers?"*
   • *"What is our best-selling item?"*
3. The AI reads your live SQLite store database and delivers concise business advice in Pakistani Rupees (PKR)!`,
    navTarget: 'AI Assistant',
    navLabel: 'Open AI Assistant',
  },
  {
    id: 'analytics-tips',
    title: '📈 Where can I view sales trends?',
    badge: 'Analytics',
    reply: `To analyze your store's financial performance:
1. Open the **Analytics** page from the sidebar.
2. Use the dropdown to toggle between **7 days** (daily PKR earnings) and **30 days** (weekly breakdown).
3. Review key metrics: **Average Order Value**, **Growth Rate**, **Top Selling Products**, and **Category Distribution**!`,
    navTarget: 'Analytics',
    navLabel: 'Go to Analytics page',
  },
]

export default function GuideChatbot({ onNavigate, activePage }) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: `Assalam-o-Alaikum! 👋 I am your **ShopMate Web Guide**.

I can show you how to use every feature on this website, manage your products, fulfill orders, and track your revenue.

Choose a topic below or type any question!`,
      actions: null,
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const chatInputRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen, isTyping])

  const handleSelectTopic = (topic) => {
    setMessages((prev) => [
      ...prev,
      { sender: 'user', text: topic.title },
    ])
    setIsTyping(true)

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: topic.reply,
          navTarget: topic.navTarget,
          navLabel: topic.navLabel,
        },
      ])
      setIsTyping(false)
    }, 350)
  }

  const handleSendMessage = async (textToSend) => {
    const text = (textToSend || inputValue).trim()
    if (!text || isTyping) return

    setInputValue('')
    setMessages((prev) => [...prev, { sender: 'user', text }])
    setIsTyping(true)

    // Helper to resolve navigation button for relevant app sections
    const resolveNavTarget = (content) => {
      const lower = content.toLowerCase()
      if (/product|add item|catalogue|sku/i.test(lower)) return { target: 'Products', label: 'Go to Products' }
      if (/order|receipt|whatsapp|fulfill/i.test(lower)) return { target: 'Orders', label: 'Go to Orders' }
      if (/stock|inventory|shortage|restock/i.test(lower)) return { target: 'Inventory', label: 'Go to Inventory' }
      if (/customer|client|buyer/i.test(lower)) return { target: 'Customers', label: 'Go to Customers' }
      if (/analytic|revenue|sale|trend|chart/i.test(lower)) return { target: 'Analytics', label: 'Go to Analytics' }
      if (/ai assistant|gemini|advisor/i.test(lower)) return { target: 'AI Assistant', label: 'Open AI Assistant' }
      return { target: null, label: null }
    }

    try {
      // 1. Try backend live Web Guide AI (powered by Google Gemini)
      const res = await api.guideChat(text)
      if (res && res.reply) {
        const { target, label } = resolveNavTarget(text + ' ' + res.reply)
        setMessages((prev) => [
          ...prev,
          {
            sender: 'bot',
            text: res.reply,
            navTarget: target,
            navLabel: label,
          },
        ])
        setIsTyping(false)
        return
      }
    } catch {
      // Graceful local fallback if backend is offline
    }

    // 2. Client-side rule-based web guide fallback (Strictly about using this website)
    setTimeout(() => {
      const lower = text.toLowerCase()
      let reply = ''
      let navTarget = null
      let navLabel = null

      if (/product|add item|new item|catalogue|price|item/i.test(lower)) {
        reply = `To manage products, navigate to the **Products** page. Click the "+ Add product" button at the top-right to enter a name, category, PKR price, and stock. You can also click "Restock (+20)" on any product row to instantly replenish units.`
        navTarget = 'Products'
        navLabel = 'Go to Products'
      } else if (/order|receipt|whatsapp|fulfill|deliver|processing|invoice/i.test(lower)) {
        reply = `To view and manage orders, go to **Orders**. You can see all customer purchases, click an order status to advance it (Processing ➔ Shipped ➔ Delivered), or click the green "Receipt" button to send an instant WhatsApp bill!`
        navTarget = 'Orders'
        navLabel = 'Go to Orders'
      } else if (/stock|inventory|shortage|restock|low stock/i.test(lower)) {
        reply = `To track stock health, open the **Inventory** page. Any item with fewer than 10 units is flagged with a "Low stock" warning pill. Click "Restock (+20)" on any row to instantly replenish your shelves.`
        navTarget = 'Inventory'
        navLabel = 'Go to Inventory'
      } else if (/customer|buyer|client|phone|city|directory/i.test(lower)) {
        reply = `To see your customer directory, visit the **Customers** page. You'll see customer names, phone numbers, cities, total order counts, and total lifetime spend in PKR.`
        navTarget = 'Customers'
        navLabel = 'Go to Customers'
      } else if (/sale|revenue|growth|money|earning|chart|analytics|trend/i.test(lower)) {
        reply = `For financial charts and trends, visit the **Analytics** page. You can compare 7-day and 30-day performance, see peak revenue days, and analyze category breakdowns.`
        navTarget = 'Analytics'
        navLabel = 'Go to Analytics'
      } else if (/ai|bot|gemini|assistant|ask/i.test(lower)) {
        reply = `The **AI Assistant** is your smart retail business partner in the sidebar! You can ask it natural business questions about sales, stock, and customers and get recommendations powered by Google Gemini.`
        navTarget = 'AI Assistant'
        navLabel = 'Open AI Assistant'
      } else if (/search|shortcut|find|filter|kbd/i.test(lower)) {
        reply = `You can search anything across the app using the search bar in the top navigation, or by pressing **Ctrl + K** (or **⌘ + K**) on your keyboard!`
      } else if (/responsive|mobile|phone|tablet|menu/i.test(lower)) {
        reply = `ShopMate AI is 100% responsive! On mobile and tablet devices, tap the menu toggle button (☰) at the top-left to open the sidebar, and tables scroll smoothly with touch.`
      } else if (/print|export|report/i.test(lower)) {
        reply = `You can print your inventory report anytime by going to **Inventory** and clicking the "Print report" button!`
        navTarget = 'Inventory'
        navLabel = 'Go to Inventory'
      } else {
        reply = `I am specifically the **ShopMate Web Guide**. I'm here to help you navigate and use this web application.

Please ask me how to:
• Add products or restock inventory
• Send WhatsApp receipts to customers
• Advance order fulfillment status
• View sales charts and analytics
• Use the Google Gemini AI Assistant`
      }

      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: reply, navTarget, navLabel },
      ])
      setIsTyping(false)
    }, 350)
  }

  return (
    <aside className="guide-chatbot-wrapper" aria-label="Web Guide Chatbot">
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          className="guide-fab"
          onClick={() => setIsOpen(true)}
          aria-label="Open ShopMate Web Guide AI"
          title="Need help? Click to open Web Guide AI"
        >
          <div className="guide-fab-pulse" />
          <span className="guide-fab-icon">
            <Bot size={22} strokeWidth={2.2} />
          </span>
          <span className="guide-fab-label">
            <span className="guide-fab-title">Web Guide AI</span>
            <span className="guide-fab-subtitle">How to use this web</span>
          </span>
          <span className="guide-fab-sparkle">
            <Sparkles size={14} />
          </span>
        </button>
      )}

      {/* Floating Chat Modal Card */}
      {isOpen && (
        <section
          className="guide-chat-card"
          role="dialog"
          aria-modal="false"
          aria-label="ShopMate Web Guide Window"
        >
          {/* Card Header */}
          <header className="guide-chat-header">
            <div className="guide-header-info">
              <div className="guide-avatar-badge">
                <Bot size={19} />
                <span className="guide-online-dot" />
              </div>
              <div>
                <h3 className="guide-header-title">ShopMate Web Guide</h3>
                <p className="guide-header-status">
                  <span className="guide-live-status" /> Interactive App Guide · Ready
                </p>
              </div>
            </div>
            <div className="guide-header-actions">
              <button
                className="guide-icon-btn"
                onClick={() => setIsOpen(false)}
                title="Minimize guide"
                aria-label="Close web guide"
              >
                <X size={17} />
              </button>
            </div>
          </header>

          {/* Quick Guide Pills */}
          <div className="guide-quick-pills-bar">
            <span className="guide-pills-title">Quick Guides:</span>
            <div className="guide-pills-scroll">
              {GUIDE_TOPICS.map((topic) => (
                <button
                  key={topic.id}
                  className="guide-pill-btn"
                  onClick={() => handleSelectTopic(topic)}
                  disabled={isTyping}
                >
                  {topic.title}
                </button>
              ))}
            </div>
          </div>

          {/* Messages Stream */}
          <div className="guide-messages-stream">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`guide-bubble-row ${
                  msg.sender === 'user' ? 'guide-bubble-user' : 'guide-bubble-bot'
                }`}
              >
                {msg.sender === 'bot' && (
                  <div className="guide-msg-avatar" aria-hidden="true">
                    <Sparkles size={13} />
                  </div>
                )}
                <div className="guide-bubble-content">
                  <div className="guide-bubble-text" style={{ whiteSpace: 'pre-wrap' }}>
                    {msg.text}
                  </div>
                  {msg.navTarget && onNavigate && (
                    <button
                      className="guide-nav-btn"
                      onClick={() => {
                        onNavigate(msg.navTarget)
                        setIsOpen(false)
                      }}
                    >
                      <span>{msg.navLabel || `Go to ${msg.navTarget}`}</span>
                      <ArrowRight size={13} />
                    </button>
                  )}
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="guide-bubble-row guide-bubble-bot">
                <div className="guide-msg-avatar" aria-hidden="true">
                  <Sparkles size={13} />
                </div>
                <div className="guide-bubble-content">
                  <div className="guide-bubble-typing">
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Current Page Context Hint */}
          <div className="guide-context-bar">
            <span>You are currently viewing: <strong>{activePage || 'Dashboard'}</strong></span>
          </div>

          {/* Input Footer */}
          <form
            className="guide-input-form"
            onSubmit={(e) => {
              e.preventDefault()
              handleSendMessage()
            }}
          >
            <input
              ref={chatInputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask how to do anything in this web..."
              aria-label="Ask Web Guide AI"
              disabled={isTyping}
            />
            <button
              type="submit"
              className="guide-send-btn"
              disabled={!inputValue.trim() || isTyping}
              aria-label="Send question to guide"
            >
              <Send size={15} />
            </button>
          </form>
        </section>
      )}
    </aside>
  )
}

