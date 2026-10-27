import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { ApiError } from '../api/client'
import { useAuth } from '../auth/context'
import { AuthCard } from '../components/AuthCard'
import { Field } from '../components/Field'

type Campo = 'nome' | 'email' | 'senha'
type Erros = Partial<Record<Campo, string>>

// Same rules as the API (FR-001, FR-008); messages in pt-BR for every field the API may reject.
const MENSAGENS: Record<Campo, string> = {
  nome: 'Informe seu nome.',
  email: 'Informe um e-mail válido.',
  senha: 'A senha deve ter pelo menos 8 caracteres.',
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validar(nome: string, email: string, senha: string): Erros {
  const erros: Erros = {}
  if (!nome.trim()) erros.nome = MENSAGENS.nome
  if (!EMAIL_RE.test(email.trim())) erros.email = MENSAGENS.email
  if (senha.length < 8) erros.senha = MENSAGENS.senha
  return erros
}

export default function RegisterPage() {
  const { register, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erros, setErros] = useState<Erros>({})
  const [erroGeral, setErroGeral] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  if (isAuthenticated && !enviando) return <Navigate to="/" replace />

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setErroGeral(null)
    const locais = validar(nome, email, senha)
    setErros(locais)
    if (Object.keys(locais).length > 0) return

    setEnviando(true)
    try {
      await register(nome, email, senha)
      navigate('/', { replace: true })
    } catch (e) {
      setEnviando(false)
      if (!(e instanceof ApiError)) {
        setErroGeral((e as Error).message)
      } else if (e.code === 'EMAIL_JA_CADASTRADO') {
        setErros({ email: e.message })
      } else if (e.code === 'DADOS_INVALIDOS') {
        const doServidor: Erros = {}
        for (const campo of Object.keys(e.campos)) {
          if (campo in MENSAGENS) doServidor[campo as Campo] = MENSAGENS[campo as Campo]
        }
        setErros(doServidor)
        if (Object.keys(doServidor).length === 0) setErroGeral(e.message)
      } else {
        setErroGeral(e.message)
      }
    }
  }

  return (
    <AuthCard title="Criar conta" subtitle="Seus dados financeiros ficam visíveis só para você.">
      <form onSubmit={onSubmit} noValidate>
        <Field
          label="Nome"
          autoComplete="name"
          value={nome}
          error={erros.nome}
          onChange={(e) => setNome(e.target.value)}
        />
        <Field
          label="E-mail"
          type="email"
          autoComplete="email"
          value={email}
          error={erros.email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Field
          label="Senha"
          type="password"
          autoComplete="new-password"
          value={senha}
          error={erros.senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        {erroGeral && (
          <p role="alert" className="form-error">
            {erroGeral}
          </p>
        )}
        <button type="submit" className="button-primary" disabled={enviando}>
          {enviando ? 'Criando conta…' : 'Criar conta'}
        </button>
      </form>
      <p className="auth-switch">
        Já tem conta? <Link to="/login">Entrar</Link>
      </p>
    </AuthCard>
  )
}
