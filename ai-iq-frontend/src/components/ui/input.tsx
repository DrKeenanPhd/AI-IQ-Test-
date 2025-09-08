import * as React from 'react'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = React.forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  const { className = '', ...rest } = props
  const classes = `flex h-10 w-full rounded-md border px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 ${className}`
  return <input ref={ref} className={classes} {...rest} />
})
Input.displayName = 'Input'

export default Input
