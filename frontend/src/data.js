export const salesData = [
  { day: 'Mon', sales: 4800, orders: 6 },
  { day: 'Tue', sales: 6200, orders: 8 },
  { day: 'Wed', sales: 5500, orders: 7 },
  { day: 'Thu', sales: 7100, orders: 9 },
  { day: 'Fri', sales: 6800, orders: 8 },
  { day: 'Sat', sales: 9100, orders: 12 },
  { day: 'Sun', sales: 8300, orders: 10 },
]

export const products = [
  { name: 'Premium Basmati Rice', category: 'Grocery', sku: 'GR-1024', price: 1850, stock: 48, sold: 142, emoji: '🍚', color: 'sand' },
  { name: 'Sufi Cooking Oil 5L', category: 'Grocery', sku: 'GR-1031', price: 2750, stock: 9, sold: 98, emoji: '🫒', color: 'mint' },
  { name: 'Everyday Cotton Kurta', category: 'Clothing', sku: 'CL-2042', price: 3200, stock: 26, sold: 86, emoji: '👕', color: 'lilac' },
  { name: 'Royal Chai Blend', category: 'Beverages', sku: 'BV-3018', price: 980, stock: 6, sold: 74, emoji: '🍵', color: 'peach' },
  { name: 'Handwoven Khussa', category: 'Footwear', sku: 'FW-4056', price: 4500, stock: 18, sold: 63, emoji: '🥿', color: 'pink' },
  { name: 'Ajwa Dates (500g)', category: 'Grocery', sku: 'GR-1067', price: 2250, stock: 34, sold: 51, emoji: '🌴', color: 'sand' },
]

export const orders = [
  { id: '#SM-2084', customer: 'Ayesha Khan', initials: 'AK', item: 'Premium Basmati Rice', date: 'Today, 10:42 AM', amount: 4650, status: 'Processing', color: 'blue' },
  { id: '#SM-2083', customer: 'Usman Ali', initials: 'UA', item: 'Everyday Cotton Kurta', date: 'Today, 10:18 AM', amount: 3200, status: 'Shipped', color: 'purple' },
  { id: '#SM-2082', customer: 'Fatima Sheikh', initials: 'FS', item: 'Sufi Cooking Oil 5L', date: 'Today, 9:56 AM', amount: 5500, status: 'Delivered', color: 'green' },
  { id: '#SM-2081', customer: 'Bilal Ahmed', initials: 'BA', item: 'Royal Chai Blend', date: 'Today, 9:30 AM', amount: 1960, status: 'Processing', color: 'orange' },
  { id: '#SM-2080', customer: 'Maham Raza', initials: 'MR', item: 'Handwoven Khussa', date: 'Yesterday, 6:12 PM', amount: 4500, status: 'Delivered', color: 'pink' },
]

export const customers = [
  { name: 'Ayesha Khan', phone: '+92 300 1234567', city: 'Lahore', orders: 12, spent: 38400, initials: 'AK', color: 'blue' },
  { name: 'Usman Ali', phone: '+92 321 7654321', city: 'Karachi', orders: 8, spent: 26750, initials: 'UA', color: 'purple' },
  { name: 'Fatima Sheikh', phone: '+92 333 9876543', city: 'Islamabad', orders: 7, spent: 22100, initials: 'FS', color: 'green' },
  { name: 'Bilal Ahmed', phone: '+92 312 4567890', city: 'Faisalabad', orders: 5, spent: 15800, initials: 'BA', color: 'orange' },
  { name: 'Maham Raza', phone: '+92 301 8765432', city: 'Rawalpindi', orders: 4, spent: 12400, initials: 'MR', color: 'pink' },
]

export const navigation = [
  {
    title: 'Workspace',
    items: [
      { label: 'Overview', icon: 'LayoutDashboard' },
      { label: 'AI Assistant', icon: 'Sparkles', badge: 'AI' },
    ],
  },
  {
    title: 'Manage',
    items: [
      { label: 'Products', icon: 'Package', count: '48' },
      { label: 'Orders', icon: 'ShoppingBag', count: '12' },
      { label: 'Inventory', icon: 'Boxes', dot: true },
      { label: 'Customers', icon: 'UsersRound' },
    ],
  },
  {
    title: 'Insights',
    items: [{ label: 'Analytics', icon: 'ChartNoAxesCombined' }],
  },
]
