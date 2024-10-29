import React from 'react';
import logo from './logo.svg';
import { Counter } from './features/counter/Counter';
import  Register  from './features/register/Register'
import './App.css';
import { Outlet, Link } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        {/* <Counter />  */}
        <Register />
      </header>
      <Outlet/>
    </div>
  );
}

export default App;
