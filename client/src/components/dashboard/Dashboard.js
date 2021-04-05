import React, { Fragment, useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import {
  submitSubredditInfo,
  fetchUserSubreddits,
} from '../../actions/subreddit';
import DashboardTable from './DashboardTable';

const Dashboard = ({
  submitSubredditInfo,
  fetchUserSubreddits,
  subredditState: { subreddits },
  authState: {
    loggedInUser: { id },
    isAuthenticated,
  },
}) => {
  // need to populate the redux state using useEffect before rendering dashboard.
  useEffect(() => {
    fetchUserSubreddits(id);
  }, []);

  const [formData, setFormData] = useState({
    subredditName: '',
    subredditKeywords: '',
  });

  const { subredditName, subredditKeywords } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    submitSubredditInfo({ id, subredditName, subredditKeywords });
  };

  const handleSubredditName = (e) => {
    setFormData({
      ...formData,
      subredditName: e.target.value,
    });
  };

  const handleSubredditKeywords = (e) => {
    setFormData({
      ...formData,
      subredditKeywords: e.target.value,
    });
  };

  const displaySubredditTables = () => {
    return subreddits.map((subreddit) => (
      <DashboardTable subreddit={subreddit} />
    ));
  };

  if (!isAuthenticated) {
    return <Redirect to='/register' />;
  }

  return (
    <Fragment>
      <h1 className='defaultHeader'>ReddAlerts</h1>
      <div className='submissionBox'>
        <h2>Subreddits To Monitor</h2>
        <div className='line'></div>
        <form onSubmit={handleSubmit}>
          <p>Subreddit (/r/)</p>
          <input
            type='text'
            placeholder='technology'
            value={subredditName}
            onChange={handleSubredditName}
          />
          <p className='smallText'>One subreddit per submission.</p>
          <div className='line'></div>

          <p>Keywords</p>
          <input
            type='text'
            placeholder='javascript, reactjs'
            value={subredditKeywords}
            onChange={handleSubredditKeywords}
          />
          <p className='smallText'>Comma separated list.</p>

          <input type='submit' value='Submit' />
        </form>
      </div>

      {displaySubredditTables()}
    </Fragment>
  );
};

const mapStateToProps = (state) => ({
  subredditState: state.subreddit,
  authState: state.auth,
});

export default connect(mapStateToProps, {
  submitSubredditInfo,
  fetchUserSubreddits,
})(Dashboard);
