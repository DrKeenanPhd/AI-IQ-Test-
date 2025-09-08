import * as React from 'react'

export type BadgeVariant =
  | 'default'
  | 'secondary'
  | 'outline'
  | 'success'
  | 'warning'
  | 'destructive'

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant
  key?: React.Key
}

const variantClasses: Record<BadgeVariant, string> = {
  default: 'bg-gray-800 text-white',
  secondary: 'bg-gray-200 text-gray-900',
  outline: 'border border-gray-400 text-gray-800',
  success: 'bg-emerald-600 text-white',
  warning: 'bg-amber-500 text-black',
  destructive: 'bg-red-600 text-white',
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className = '', variant = 'default', ...props }, ref) => {
    const base = 'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium'
    const classes = `${base} ${variantClasses[variant]} ${className}`
    return <span ref={ref} className={classes} {...props} />
  }
)
Badge.displayName = 'Badge'

export default Badge
