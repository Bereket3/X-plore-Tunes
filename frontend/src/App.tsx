import React from 'react';
import logo from './logo.svg';
import './App.css';

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login"
import Layout from './pages/Layout';
import Home from './pages/Home';
import NoPage from './pages/NoPage';
import SignUp from './pages/SignUp';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="login" element={<Login/>} />
          <Route path="signup" element={<SignUp/>}/>
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
