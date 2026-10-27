import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'

import { useAuth } from '../auth/context'
import { SECOES } from './nav'

/** Signed-in shell. Below 640 px the nav collapses behind a menu button (US4, RNF001). */
export default function Layout() {
  const { usuario, logout } = useAuth()
  const [menuAberto, setMenuAberto] = useState(false)
  const location = useLocation()

  useEffect(() => setMenuAberto(false), [location.pathname])

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand">
          UPFinance
        </Link>
        <button
          type="button"
          className="menu-toggle"
          aria-expanded={menuAberto}
          aria-controls="nav-principal"
          onClick={() => setMenuAberto((aberto) => !aberto)}
        >
          {menuAberto ? 'Fechar' : 'Menu'}
        </button>
        <nav id="nav-principal" className="nav" data-open={menuAberto} aria-label="Principal">
          <ul>
            {SECOES.map((secao) => (
              <li key={secao.path}>
                <NavLink to={secao.path}>{secao.label}</NavLink>
              </li>
            ))}
          </ul>
          <div className="nav-user">
            <span className="muted" title={usuario?.email}>
              {usuario?.nome}
            </span>
            <button type="button" className="button-link" onClick={logout}>
              Sair
            </button>
          </div>
        </nav>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
