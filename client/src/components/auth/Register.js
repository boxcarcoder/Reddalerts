import React, { useState } from 'react';
import { register } from '../../actions/auth';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import authPic from '../../img/top-design-subreddits.jpeg';

const Register = ({ register, authState: { isAuthenticated } }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const { username, email, password } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();

    // Send the form data to Redux action.
    register({ username, email, password });
  };

  const handleUsername = (e) => {
    setFormData({
      ...formData,
      username: e.target.value,
    });
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
    return <Redirect to='/settings' />;
  }

  return (
    <section>
      <div className='authBox'>
        <h1>Sign Up</h1>
        <div className='line'></div>

        <form onSubmit={handleSubmit}>
          <p>Username</p>
          <input
            type='text'
            placeholder='John Doe'
            onChange={handleUsername}
            value={username}
          />
          <p>Email</p>
          <input
            type='email'
            placeholder='jdoe@gmail.com'
            onChange={handleEmail}
            value={email}
          />
          <p>Password</p>
          <input
            type='password'
            placeholder='********'
            onChange={handlePassword}
            value={password}
          />
          <input type='submit' value='Register' />
        </form>
      </div>

      <img src={authPic} alt='register' width='569' className='authPic' />
      <div>
        Already have an account? <a href='/login'>Login</a>
      </div>
    </section>
  );
};

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps, { register })(Register);
