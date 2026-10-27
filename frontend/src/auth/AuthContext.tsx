import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'

import { api, setAuthToken, setUnauthorizedHandler } from '../api/client'
import type { TokenResponse, Usuario } from '../api/types'
import { AuthContext, type AuthState } from './context'

// Token lives in memory and in sessionStorage: it survives a reload, not a closed tab (research R1).
const STORAGE_KEY = 'upfinance.sessao'

type Sessao = { token: string; usuario: Usuario }

function lerSessao(): Sessao | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as Sessao) : null
  } catch {
    return null
  }
}

function gravarSessao(sessao: Sessao | null) {
  try {
    if (sessao) sessionStorage.setItem(STORAGE_KEY, JSON.stringify(sessao))
    else sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    // storage unavailable (private mode): the session stays in memory only
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [sessao, setSessao] = useState<Sessao | null>(() => {
    const inicial = lerSessao()
    setAuthToken(inicial?.token ?? null)
    return inicial
  })

  const iniciar = useCallback((resp: TokenResponse) => {
    const nova = { token: resp.access_token, usuario: resp.usuario }
    setAuthToken(nova.token)
    gravarSessao(nova)
    setSessao(nova)
  }, [])

  const logout = useCallback(() => {
    setAuthToken(null)
    gravarSessao(null)
    setSessao(null)
  }, [])

  // An expired token ends the session; RequireAuth then sends the user to
  // /login and keeps the screen they were on (spec edge case).
  useEffect(() => {
    setUnauthorizedHandler(logout)
    return () => setUnauthorizedHandler(null)
  }, [logout])

  const login = useCallback(
    async (email: string, senha: string) => {
      iniciar(await api<TokenResponse>('/auth/login', { method: 'POST', body: { email, senha } }))
    },
    [iniciar],
  )

  const register = useCallback(
    async (nome: string, email: string, senha: string) => {
      iniciar(await api<TokenResponse>('/auth/register', { method: 'POST', body: { nome, email, senha } }))
    },
    [iniciar],
  )

  const value = useMemo<AuthState>(
    () => ({ usuario: sessao?.usuario ?? null, isAuthenticated: sessao !== null, login, register, logout }),
    [sessao, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
