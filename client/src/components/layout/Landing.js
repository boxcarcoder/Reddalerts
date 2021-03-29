import React from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
  return (
    <section className='landing'>
      <div className='dark-overlay'>
        <div className='landingText'>
          <h1>ReddAlerts</h1>
          <Link to='/register'>Register</Link>
          <Link to='/login'>Log In</Link>
        </div>
      </div>
    </section>
  );
};

export default Landing;
