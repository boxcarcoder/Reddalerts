import React from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
  return (
    <section className='landing'>
      <div className='dark-overlay'>
        <h1 className='landingHeader'>ReddAlerts</h1>
        <div className='landingLinks'>
          <Link to='/register' className='btn'>
            Register
          </Link>
          <Link to='/login' className='btn'>
            Login
          </Link>
        </div>
      </div>
    </section>
  );
};

export default Landing;
