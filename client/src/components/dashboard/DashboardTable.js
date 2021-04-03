import React, { Fragment } from 'react';
import { deleteMonitoredSubreddit } from '../../actions/subreddit';
import { connect } from 'react-redux';

const DashboardTable = ({
  subreddit: { subreddit_name, keywords },
  deleteMonitoredSubreddit,
  authState: {
    loggedInUser: { id },
  },
}) => {
  const handleDelete = (e) => {
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
    <Fragment>
      <div className='subredditTableAndDeleteBtn'>
        <table className='subredditTable'>
          <thead>
            <tr>
              <th colspan='2'>{subreddit_name}</th>
            </tr>
            <tr>
              <div className='line' />
            </tr>
          </thead>
          <tbody>{displayKeywords(keywords)}</tbody>
        </table>
        <button className='deleteBtn' onClick={(e) => handleDelete(e)}>
          Delete
        </button>
      </div>
    </Fragment>
  );
};

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps, { deleteMonitoredSubreddit })(
  DashboardTable
);
