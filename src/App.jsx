import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import InputWithButton from './product'
import ResponsiveAppBar from './Navbar'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <ResponsiveAppBar></ResponsiveAppBar>
      <InputWithButton></InputWithButton  >
      
    </>
  )
}

export default App
