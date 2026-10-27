import type { ReactNode } from 'react'

/** Shell for the signed-out screens (login, register). */
export function AuthCard({ title, subtitle, children }: { title: string; subtitle: string; children: ReactNode }) {
  return (
    <main className="auth">
      <div className="auth-card">
        <p className="brand">UPFinance</p>
        <h1>{title}</h1>
        <p className="muted">{subtitle}</p>
        {children}
      </div>
    </main>
  )
}
