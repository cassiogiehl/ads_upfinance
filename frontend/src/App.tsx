import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

const queryClient = new QueryClient()

// Pages, auth and layout arrive in 000 Phase 4 (T022–T027).
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="*" element={<main className="app">UPFinance</main>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
