import {
  SUBMIT_SUBREDDIT_INFO,
  SUBMIT_SUBREDDIT_INFO_FAIL,
  FETCH_SUBREDDITS,
  FETCH_SUBREDDITS_FAIL,
} from './types';
import axios from 'axios';

export const submitSubredditInfo = ({
  loggedInUser,
  subredditName,
  subredditKeywords,
}) => async (dispatch) => {
  try {
    // configuration of the HTTP request to the backend
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    const body = JSON.stringify({
      loggedInUser,
      subredditName,
      subredditKeywords,
    });
    const res = await axios.post('/api/submitSubredditInfo', body, config);

    dispatch({
      type: SUBMIT_SUBREDDIT_INFO,
      payload: res.data,
    });
  } catch (err) {
    dispatch({
      type: SUBMIT_SUBREDDIT_INFO_FAIL,
      payload: { msg: err },
    });
  }
};

export const fetchUserSubreddits = (loggedInUser) => async (dispatch) => {
  try {
    console.log('firing fetchUserSubreddits() action');
    const res = await axios.get('/api/fetchSubredditsInfo', {
      params: {
        loggedInUser,
      },
    });
    console.log(
      'res from successful firing of fetchUserSubreddits() action: ',
      res
    );

    dispatch({
      type: FETCH_SUBREDDITS,
      payload: res.data,
    });
  } catch (err) {
    console.log('failure in fetchUserSubreddits() action: ', err);
    dispatch({
      type: FETCH_SUBREDDITS_FAIL,
      payload: { msg: err },
    });
  }
};
