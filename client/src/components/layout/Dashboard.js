import React, { Fragment, useState, useEffect } from 'react';
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
    loggedInUser: { username },
  },
}) => {
  // need to populate the redux state using useEffect before rendering dashboard.
  useEffect(() => {
    fetchUserSubreddits(username);
  }, []);

  const [formData, setFormData] = useState({
    subredditName: '',
    subredditKeywords: '',
  });

  const { subredditName, subredditKeywords } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    submitSubredditInfo({ username, subredditName, subredditKeywords });
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

  return (
    <Fragment>
      <h1>Reddalerts</h1>
      <h3>Subreddits To Monitor</h3>
      <form onSubmit={handleSubmit}>
        <input
          type='text'
          placeholder='Subreddit'
          value={subredditName}
          onChange={handleSubredditName}
        />
        <input
          type='text'
          placeholder='Keywords'
          value={subredditKeywords}
          onChange={handleSubredditKeywords}
        />
        <input type='submit' value='Submit' />
        {displaySubredditTables()}
      </form>
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
