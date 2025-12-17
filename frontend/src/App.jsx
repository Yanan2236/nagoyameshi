import { Routes, Route } from 'react-router-dom'

import { Navbar} from './components/Navbar'
import { Home } from './components/Home.jsx'
import { Restaurants } from './components/Restaurants'
import { Users } from './components/Users.jsx'
import { Login } from './components/Login.jsx'
import { Logout } from './components/Logout.jsx'

import './App.css'

export const App = () => {
  return (
    <>
    <Navbar />
    <Routes>
      <Route path="/" element={<Home />}></Route>
      <Route path="/restaurants" element={<Restaurants />}></Route>
      <Route path="/users" element={<Users />}></Route>
      <Route path="/login" element={<Login />}></Route>
      <Route path="/logout" element={<Logout />}></Route>
    </Routes>
    <header>
    </header>
    </>
  )
}
