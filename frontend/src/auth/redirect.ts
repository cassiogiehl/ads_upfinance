import type { Location } from 'react-router-dom'

/** Where to go after signing in: the screen RequireAuth interrupted, or home. */
export function destinoAposLogin(state: unknown): string {
  const from = (state as { from?: Location } | null)?.from
  if (!from || from.pathname === '/login' || from.pathname === '/cadastro') return '/'
  return `${from.pathname}${from.search}${from.hash}`
}
