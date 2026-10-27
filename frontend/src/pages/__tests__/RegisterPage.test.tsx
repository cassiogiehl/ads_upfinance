import { fireEvent, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { mockFetch, renderRoute, TOKEN_RESPONSE } from '../../test/utils'
import RegisterPage from '../RegisterPage'

function preencher(nome: string, email: string, senha: string) {
  fireEvent.change(screen.getByLabelText('Nome'), { target: { value: nome } })
  fireEvent.change(screen.getByLabelText('E-mail'), { target: { value: email } })
  fireEvent.change(screen.getByLabelText('Senha'), { target: { value: senha } })
  fireEvent.click(screen.getByRole('button', { name: 'Criar conta' }))
}

afterEach(() => {
  vi.unstubAllGlobals()
  sessionStorage.clear()
})

describe('RegisterPage', () => {
  it('creates the account and signs in (US1-1)', async () => {
    const fetchMock = mockFetch(201, TOKEN_RESPONSE)
    renderRoute('/cadastro', <RegisterPage />)

    preencher('Rafael', 'rafael@example.com', 'senha1234')

    expect(await screen.findByTestId('destino')).toHaveTextContent('/')
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/auth/register',
      expect.objectContaining({ method: 'POST' }),
    )
  })

  it('shows the duplicate-email message on the email field (US1-2)', async () => {
    mockFetch(409, { code: 'EMAIL_JA_CADASTRADO', message: 'Este e-mail já está cadastrado', details: {} })
    renderRoute('/cadastro', <RegisterPage />)

    preencher('Rafael', 'rafael@example.com', 'senha1234')

    expect(await screen.findByText('Este e-mail já está cadastrado')).toBeInTheDocument()
    expect(screen.getByLabelText('E-mail')).toHaveAttribute('aria-invalid', 'true')
  })

  it('identifies every invalid field before calling the API (US1-3)', () => {
    const fetchMock = mockFetch(201, TOKEN_RESPONSE)
    renderRoute('/cadastro', <RegisterPage />)

    preencher('   ', 'nao-e-email', 'curta')

    expect(screen.getByText('Informe seu nome.')).toBeInTheDocument()
    expect(screen.getByText('Informe um e-mail válido.')).toBeInTheDocument()
    expect(screen.getByText('A senha deve ter pelo menos 8 caracteres.')).toBeInTheDocument()
    for (const label of ['Nome', 'E-mail', 'Senha']) {
      expect(screen.getByLabelText(label)).toHaveAttribute('aria-invalid', 'true')
    }
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('maps field errors returned by the API (US1-3)', async () => {
    mockFetch(422, {
      code: 'DADOS_INVALIDOS',
      message: 'Dados inválidos.',
      details: { campos: { email: 'value is not a valid email address' } },
    })
    renderRoute('/cadastro', <RegisterPage />)

    preencher('Rafael', 'rafael@exemplo.c0m', 'senha1234')

    expect(await screen.findByText('Informe um e-mail válido.')).toBeInTheDocument()
    expect(screen.queryByText('value is not a valid email address')).not.toBeInTheDocument()
  })
})
