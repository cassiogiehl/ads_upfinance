// Sections of the app. Each one is filled in by its feature (001–004).
export const SECOES = [
  { path: '/movimentacoes', label: 'Movimentações', feature: '001' },
  { path: '/analise', label: 'Análise', feature: '002' },
  { path: '/faturas', label: 'Faturas', feature: '003' },
  { path: '/recorrencias', label: 'Recorrências', feature: '004' },
  { path: '/alertas', label: 'Alertas', feature: '002' },
] as const

// Opt in to React Router v7 behavior now, so the upgrade changes nothing.
export const ROUTER_FUTURE = { v7_startTransition: true, v7_relativeSplatPath: true } as const
