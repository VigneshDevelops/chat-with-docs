import Container from './components/container'
import { AppProvider } from './context/AppContext'

function App() {
  return (
  <>
  <AppProvider>
  <Container />
  </AppProvider>
  </>
  )
}

export default App
