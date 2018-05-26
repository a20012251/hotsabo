import React, { Component } from 'react';
import { Header } from './components/layouts';
import News from './components/news';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header />
        <News />
      </div>
    );
  }
}

export default App;
