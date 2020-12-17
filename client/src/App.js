import React, { Fragment } from 'react';
import './scss/App.scss';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// redux
import { Provider } from 'react-redux';
import store from './store';

// components
import Landing from './components/layout/Landing';
import Register from './components/auth/Register';
import Login from './components/auth/Login';

const App = () => {
  return (
    <Provider store={store}>
      <Router>
        <Fragment>
          <Route exact path='/' component={Landing} />
          <Switch>
            <Route exact path='/register' component={Register} />
            <Route exact path='/login' component={Login} />
          </Switch>
        </Fragment>
      </Router>
    </Provider>
  );
};
export default App;
