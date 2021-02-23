import {
  SUBMIT_SUBREDDIT_INFO,
  SUBMIT_SUBREDDIT_INFO_FAIL,
  FETCH_SUBREDDITS,
  FETCH_SUBREDDITS_FAIL,
  DELETE_SUBREDDIT,
  DELETE_SUBREDDIT_FAIL,
  UPDATE_SUBREDDIT_KEYWORDS,
} from './types';
import axios from 'axios';

export const submitSubredditInfo = ({
  id,
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
      id,
      subredditName,
      subredditKeywords,
    });

    const res = await axios.post('/api/submitSubredditInfo', body, config);

    if (res.data.update === 'true') {
      dispatch({
        type: UPDATE_SUBREDDIT_KEYWORDS,
        payload: res.data,
      });
    } else {
      dispatch({
        type: SUBMIT_SUBREDDIT_INFO,
        payload: res.data,
      });
    }
  } catch (err) {
    dispatch({
      type: SUBMIT_SUBREDDIT_INFO_FAIL,
      payload: { msg: err },
    });
  }
};

export const fetchUserSubreddits = (id) => async (dispatch) => {
  try {
    const res = await axios.get('/api/fetchSubredditsInfo', {
      params: {
        id,
      },
    });

    dispatch({
      type: FETCH_SUBREDDITS,
      payload: res.data,
    });
  } catch (err) {
    dispatch({
      type: FETCH_SUBREDDITS_FAIL,
      payload: { msg: err },
    });
  }
};

export const deleteMonitoredSubreddit = (id, subredditName) => async (
  dispatch
) => {
  try {
    const res = await axios.delete('/api/deleteMonitoredSubreddit', {
      params: {
        id,
        subredditName,
      },
    });

    dispatch({
      type: DELETE_SUBREDDIT,
      payload: res.data,
    });
  } catch (err) {
    console.log('shit: ', err);
  }
};
