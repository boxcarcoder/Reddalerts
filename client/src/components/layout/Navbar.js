import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

const Navbar = ({ authState: { isAuthenticated } }) => {
  return (
    <Fragment>
      {isAuthenticated ? (
        <Fragment>
          <Link to='/Dashboard'>Dashboard</Link>
          <Link to='/settings'>Settings</Link>
          <Link to='/landing'>Log Out</Link>
        </Fragment>
      ) : null}
    </Fragment>
  );
};

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps)(Navbar);
