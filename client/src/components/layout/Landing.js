import React from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
  return (
    <section className='landing'>
      <h1>Reddalerts</h1>
      <Link to='/register'>Register</Link>
      <Link to='/login'>Log In</Link>
    </section>
  );
};

export default Landing;
