import React from 'react';
import { Button } from 'antd';
import './App.css';
import HomePage from './pages/HomePage';
const App = () => (
  <div className="App">
    <HomePage />
    <Button type="primary">Button</Button>
  </div>
);

export default App;