// Same origin: the Vite dev server proxies /api to the api service (research R5).
const BASE_URL = '/api/v1'

/** The API error shape (Constitution VIII): {code, message, details}. */
export class ApiError extends Error {
  readonly status: number
  readonly code: string
  readonly details: Record<string, unknown>

  constructor(status: number, code: string, message: string, details: Record<string, unknown> = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }

  /** Field errors from a 422 DADOS_INVALIDOS response. */
  get campos(): Record<string, string> {
    const campos = this.details.campos
    return campos && typeof campos === 'object' ? (campos as Record<string, string>) : {}
  }
}

let authToken: string | null = null
let onUnauthorized: (() => void) | null = null

export function setAuthToken(token: string | null) {
  authToken = token
}

/** Called when an authenticated request gets a 401 (expired or revoked session). */
export function setUnauthorizedHandler(handler: (() => void) | null) {
  onUnauthorized = handler
}

type RequestOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  body?: unknown
}

export async function api<T>(path: string, { method = 'GET', body }: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = { Accept: 'application/json' }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (authToken) headers.Authorization = `Bearer ${authToken}`

  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new ApiError(0, 'ERRO_DE_REDE', 'Não foi possível conectar ao servidor. Tente novamente.')
  }

  if (response.status === 204) return undefined as T
  const data: unknown = await response.json().catch(() => null)

  if (!response.ok) {
    if (response.status === 401 && authToken) onUnauthorized?.()
    throw toApiError(response.status, data)
  }
  return data as T
}

function toApiError(status: number, data: unknown): ApiError {
  if (data && typeof data === 'object' && 'code' in data && 'message' in data) {
    const { code, message, details } = data as { code: string; message: string; details?: Record<string, unknown> }
    return new ApiError(status, code, message, details ?? {})
  }
  return new ApiError(status, 'ERRO_INESPERADO', 'Algo deu errado. Tente novamente.')
}
