import { SUBMIT_SUBREDDIT_INFO } from './types';
import axios from 'axios';

export const submitSubredditInfo = ({
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
    const body = JSON.stringify({ subredditName, subredditKeywords });
    const res = await axios.post('/api/submitSubredditInfo', body, config);

    dispatch({
      type: SUBMIT_SUBREDDIT_INFO,
      payload: res.data,
    });
  } catch (err) {}
};
