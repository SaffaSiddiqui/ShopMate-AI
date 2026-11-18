import { ArrowDownRight, ArrowUpRight } from 'lucide-react'

export default function MetricCard({ title, label, value, change, note, helper, icon: Icon, tone }) {
  const cardTitle = title || label || ''
  const cardNote = note || helper || ''
  const positive = change ? !change.startsWith('-') : true
  return (
    <article className="metric-card">
      <div className="metric-top">
        <span className={`metric-icon metric-${tone}`}>
          {Icon && <Icon size={19} strokeWidth={1.8} />}
        </span>
        <span className="metric-more" aria-hidden="true">•••</span>
      </div>
      <p className="metric-title">{cardTitle}</p>
      <div className="metric-bottom">
        <strong className="metric-value">{value}</strong>
        {change && (
          <span className={`metric-change ${positive ? 'change-up' : 'change-down'}`}>
            {positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}{change}
          </span>
        )}
      </div>
      {cardNote && <p className="metric-note">{cardNote}</p>}
    </article>
  )
}

