import { fireEvent, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { mockFetch, renderRoute, TOKEN_RESPONSE } from '../../test/utils'
import LoginPage, { MENSAGEM_CREDENCIAIS } from '../LoginPage'

function preencher(email: string, senha: string) {
  fireEvent.change(screen.getByLabelText('E-mail'), { target: { value: email } })
  fireEvent.change(screen.getByLabelText('Senha'), { target: { value: senha } })
  fireEvent.click(screen.getByRole('button', { name: 'Entrar' }))
}

afterEach(() => {
  vi.unstubAllGlobals()
  sessionStorage.clear()
})

describe('LoginPage', () => {
  it('signs in and goes home (US2-1)', async () => {
    const fetchMock = mockFetch(200, TOKEN_RESPONSE)
    renderRoute('/login', <LoginPage />)

    preencher('rafael@example.com', 'senha1234')

    expect(await screen.findByTestId('destino')).toHaveTextContent('/')
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/auth/login',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'rafael@example.com', senha: 'senha1234' }),
      }),
    )
    expect(sessionStorage.getItem('upfinance.sessao')).toContain('token-de-teste')
  })

  it('returns to the screen the user was trying to open (US2-4)', async () => {
    mockFetch(200, TOKEN_RESPONSE)
    renderRoute('/login', <LoginPage />, { from: { pathname: '/movimentacoes', search: '', hash: '' } })

    preencher('rafael@example.com', 'senha1234')

    expect(await screen.findByTestId('destino')).toHaveTextContent('/movimentacoes')
  })

  it('shows a generic message on wrong credentials (US2-2)', async () => {
    mockFetch(401, { code: 'CREDENCIAIS_INVALIDAS', message: 'qualquer coisa', details: {} })
    renderRoute('/login', <LoginPage />)

    preencher('rafael@example.com', 'errada123')

    expect(await screen.findByRole('alert')).toHaveTextContent(MENSAGEM_CREDENCIAIS)
    expect(screen.queryByTestId('destino')).not.toBeInTheDocument()
  })

  it('asks for both fields before calling the API', () => {
    const fetchMock = mockFetch(200, TOKEN_RESPONSE)
    renderRoute('/login', <LoginPage />)

    preencher('', '')

    expect(screen.getByRole('alert')).toHaveTextContent('Informe e-mail e senha.')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('shows a connection error when the API is unreachable', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    renderRoute('/login', <LoginPage />)

    preencher('rafael@example.com', 'senha1234')

    expect(await screen.findByRole('alert')).toHaveTextContent('Não foi possível conectar ao servidor')
  })
})
