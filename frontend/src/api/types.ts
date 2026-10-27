// Mirrors specs/000-foundation/contracts/openapi.yaml

export type Usuario = {
  id: number
  nome: string
  email: string
}

export type TokenResponse = {
  access_token: string
  token_type: 'bearer'
  usuario: Usuario
}
