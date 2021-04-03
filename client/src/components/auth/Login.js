import React, { useState } from 'react';
import { login } from '../../actions/auth';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import authPic from '../../img/top-design-subreddits.jpeg';

const Login = ({ login, authState: { isAuthenticated } }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const { email, password } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    // Send the form data to Redux action.
    login({ email, password });
  };

  const handleEmail = (e) => {
    setFormData({
      ...formData,
      email: e.target.value,
    });
  };

  const handlePassword = (e) => {
    setFormData({
      ...formData,
      password: e.target.value,
    });
  };

  if (isAuthenticated) {
    return <Redirect to='/dashboard' />;
  }

  return (
    <section>
      <div className='authBox'>
        <h1>Login</h1>
        <div className='line'></div>
        <form onSubmit={handleSubmit}>
          <input
            type='email'
            placeholder='Email'
            onChange={handleEmail}
            value={email}
          />
          <input
            type='password'
            placeholder='Password'
            onChange={handlePassword}
            value={password}
          />
          <input type='submit' value='Log In' />
        </form>
      </div>

      <img src={authPic} alt='login' width='569' className='authPic' />
      <div>
        Don't have an account? <a href='/register'>Register</a>
      </div>
    </section>
  );
};

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps, { login })(Login);
