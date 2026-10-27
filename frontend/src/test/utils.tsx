import { render } from '@testing-library/react'
import type { ReactElement } from 'react'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import { vi } from 'vitest'

import { AuthProvider } from '../auth/AuthContext'
import { ROUTER_FUTURE } from '../components/nav'

/** Shows the current path so tests can assert navigation. */
function Destino() {
  const location = useLocation()
  return <p data-testid="destino">{location.pathname}</p>
}

export function renderRoute(path: string, element: ReactElement, state?: unknown) {
  return render(
    <MemoryRouter initialEntries={[{ pathname: path, state }]} future={ROUTER_FUTURE}>
      <AuthProvider>
        <Routes>
          <Route path={path} element={element} />
          <Route path="*" element={<Destino />} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  )
}

export function mockFetch(status: number, body: unknown) {
  const fetchMock = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } }),
  )
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

export const TOKEN_RESPONSE = {
  access_token: 'token-de-teste',
  token_type: 'bearer',
  usuario: { id: 1, nome: 'Rafael', email: 'rafael@example.com' },
}
