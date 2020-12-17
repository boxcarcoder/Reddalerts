import React, { useState } from 'react';
import { register } from '../../actions/auth';
import { connect } from 'react-redux';

const Register = ({ register }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const { username, email, password } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();

    // Send the form data  to Redux action.
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

  return (
    <section>
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <input
          type='text'
          placeholder='Username'
          onChange={handleUsername}
          value={username}
        />
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
        <input type='submit' value='Register' />
      </form>
    </section>
  );
};

export default connect(null, { register })(Register);
