import React from 'react';
import { deleteMonitoredSubreddit } from '../../actions/subreddit';
import { connect } from 'react-redux';

const DashboardTable = ({
  subreddit: { subreddit_name, keywords },
  deleteMonitoredSubreddit,
  authState: {
    loggedInUser: { id },
  },
}) => {
  const handleClick = (e) => {
    e.preventDefault();
    deleteMonitoredSubreddit(id, subreddit_name);
  };

  const displayKeywords = (keywords) => {
    return keywords.map((keywordObj) => (
      <tr>
        <td>{keywordObj.keyword}</td>
      </tr>
    ));
  };

  return (
    <table>
      <thead>
        <tr>
          <th colspan='2'>{subreddit_name}</th>
          <td>
            <button onClick={(e) => handleClick(e)}>delete</button>
          </td>
        </tr>
      </thead>
      <tbody>{displayKeywords(keywords)}</tbody>
    </table>
  );
};

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps, { deleteMonitoredSubreddit })(
  DashboardTable
);
