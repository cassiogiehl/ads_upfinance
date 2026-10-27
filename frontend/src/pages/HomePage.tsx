import { Link } from 'react-router-dom'

import { useAuth } from '../auth/context'
import { SECOES } from '../components/nav'

export default function HomePage() {
  const { usuario } = useAuth()
  const primeiroNome = usuario?.nome.split(' ')[0]

  return (
    <>
      <h1>Olá, {primeiroNome}</h1>
      <p className="muted">O que você quer fazer hoje?</p>
      <ul className="cards">
        {SECOES.map((secao) => (
          <li key={secao.path}>
            <Link to={secao.path} className="card">
              {secao.label}
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}
