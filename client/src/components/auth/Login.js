import React, { useState } from 'react';
import { login } from '../../actions/auth';
import { connect } from 'react-redux';

const Login = ({ login }) => {
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

  return (
    <section>
      <h1>Login</h1>
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
    </section>
  );
};

export default connect(null, { login })(Login);
