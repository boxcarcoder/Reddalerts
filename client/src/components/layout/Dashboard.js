import React, { Fragment, useState } from 'react';
import { connect } from 'react-redux';
import { submitSubredditInfo } from '../../actions/subreddit';

const Dashboard = ({
  submitSubredditInfo,
  subredditState: { subreddit, subreddits },
}) => {
  const [formData, setFormData] = useState({
    subredditName: '',
    subredditKeywords: '',
  });

  const { subredditName, subredditKeywords } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    submitSubredditInfo({ subredditName, subredditKeywords });
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
    if (subreddits.length > 0) {
      for (let i = 0; i < subreddits.length; i++) {
        displaySubredditTable(subreddits[i]);
      }
    }
  };

  const displaySubredditTable = (subreddit) => {
    return (
      <table>
        <thead>
          <th colspan='2'>{subreddit.name}</th>
        </thead>
        <tbody>{displayKeywords(subreddit)}</tbody>
      </table>
    );
  };

  const displayKeywords = (subreddit) => {
    for (let i = 0; i < subreddit.keywords.length; i++) {
      return <tr>{subreddit.keywords[i]}</tr>;
    }
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

const mapToStateToProps = (state) => ({
  subredditState: state.subreddit,
});

export default connect(mapToStateToProps, { submitSubredditInfo })(Dashboard);
