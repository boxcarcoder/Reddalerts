import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from '../../actions/auth';

const Navbar = ({ authState: { isAuthenticated }, logout }) => {
  const handleLogout = (e) => {
    logout();
  };

  return (
    <Fragment>
      {isAuthenticated ? (
        <Fragment>
          <Link to='/Dashboard'>Dashboard</Link>
          <Link to='/settings'>Settings</Link>
          <a onClick={(e) => handleLogout(e)} href='#!'>
            Logout
          </a>
        </Fragment>
      ) : null}
    </Fragment>
  );
};

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps, { logout })(Navbar);
