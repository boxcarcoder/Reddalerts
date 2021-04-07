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
        <div className='readMe'>
          <p>Register to start monitoring Subreddits.</p>
          <div className='line' />
          <p>
            Specify a subreddit you wish to monitor, and keyword(s) of interest
            for that Subreddit.
          </p>
          <div className='line' />
          <p>
            Receive text messages of rising posts in each monitored Subreddit
            that contains your keywords.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Landing;
