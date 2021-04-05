import React, { Fragment } from 'react';
import './scss/App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// redux
import { Provider } from 'react-redux';
import store from './store';

// components
import Landing from './components/layout/Landing';
import Register from './components/auth/Register';
import Login from './components/auth/Login';
import Dashboard from './components/dashboard/Dashboard';
import Navbar from './components/layout/Navbar';
import Settings from './components/profile/Settings';

const App = () => {
  return (
    <Provider store={store}>
      <Router>
        <Fragment>
          <Navbar />
          <Route exact path='/' component={Landing} />
          <Switch>
            <Route exact path='/register' component={Register} />
            <Route exact path='/login' component={Login} />
            <Route exact path='/dashboard' component={Dashboard} />
            <Route exact path='/settings' component={Settings} />
          </Switch>
        </Fragment>
      </Router>
    </Provider>
  );
};
export default App;
