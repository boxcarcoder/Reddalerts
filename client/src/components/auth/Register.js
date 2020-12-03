import React, { useState } from 'react';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const { email, password } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();

    // Send formData to Redux action.
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
      </form>
    </section>
  );
};

export default Register;
