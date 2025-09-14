import React from 'react';
import logo from './logo.svg';
import './App.css';
import DateTimeRangeSearch from './Components/DateTimeRangeSearch';
import LoginForm from './Components/LoginForm'

function App() {
  return (
    <div className="App">
      <DateTimeRangeSearch />
      <LoginForm />
    </div>
  );
}

export default App;
