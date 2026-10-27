import { useState, type FormEvent } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'

import { ApiError } from '../api/client'
import { useAuth } from '../auth/context'
import { destinoAposLogin } from '../auth/redirect'
import { AuthCard } from '../components/AuthCard'
import { Field } from '../components/Field'

// US2-2: never reveal whether the email exists.
export const MENSAGEM_CREDENCIAIS = 'E-mail ou senha inválidos.'

export default function LoginPage() {
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const destino = destinoAposLogin(location.state)

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  if (isAuthenticated && !enviando) return <Navigate to={destino} replace />

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    if (!email.trim() || !senha) {
      setErro('Informe e-mail e senha.')
      return
    }
    setErro(null)
    setEnviando(true)
    try {
      await login(email, senha)
      navigate(destino, { replace: true })
    } catch (e) {
      setErro(e instanceof ApiError && e.status === 401 ? MENSAGEM_CREDENCIAIS : (e as Error).message)
      setEnviando(false)
    }
  }

  return (
    <AuthCard title="Entrar" subtitle="Acesse suas finanças.">
      <form onSubmit={onSubmit} noValidate>
        <Field
          label="E-mail"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Field
          label="Senha"
          type="password"
          autoComplete="current-password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        {erro && (
          <p role="alert" className="form-error">
            {erro}
          </p>
        )}
        <button type="submit" className="button-primary" disabled={enviando}>
          {enviando ? 'Entrando…' : 'Entrar'}
        </button>
      </form>
      <p className="auth-switch">
        Ainda não tem conta? <Link to="/cadastro">Criar conta</Link>
      </p>
    </AuthCard>
  )
}
