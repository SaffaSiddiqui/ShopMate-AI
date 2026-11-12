import { ArrowDownRight, ArrowUpRight } from 'lucide-react'

export default function MetricCard({ title, value, change, note, icon: Icon, tone }) {
  const positive = change ? !change.startsWith('-') : true
  return (
    <article className="metric-card">
      <div className="metric-top">
        <span className={`metric-icon metric-${tone}`}><Icon size={19} strokeWidth={1.8} /></span>
        <span className="metric-more" aria-hidden="true">•••</span>
      </div>
      <p className="metric-title">{title}</p>
      <div className="metric-bottom">
        <strong className="metric-value">{value}</strong>
        {change && <span className={`metric-change ${positive ? 'change-up' : 'change-down'}`}>
          {positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}{change}
        </span>}
      </div>
      <p className="metric-note">{note}</p>
    </article>
  )
}
