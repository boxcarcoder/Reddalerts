import React, { Fragment } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// component
import Landing from './components/layout/Landing';
import Register from './components/auth/Register';
import Login from './components/auth/Login';

const App = () => {
  return (
    <Router>
      <Fragment>
        <Route exact path='/' component={Landing} />
        <Switch>
          <Route exact path='/register' component={Register} />
          <Route exact path='/login' component={Login} />
        </Switch>
      </Fragment>
    </Router>
  );
};
export default App;
