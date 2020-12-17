import { LOGIN_SUCCESS, LOGIN_FAIL } from './types';
import axios from 'axios';

export const login = ({ email, password }) => async (dispatch) => {
  try {
    // configuration of the HTTP request to the backend
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    // Convert JS object into JSON to send to Flask.
    const body = JSON.stringify({ email, password });

    // Store the logged in user's token into a redux state for authentication purposes.
    const res = await axios.post('/api/login', body, config);

    dispatch({
      type: LOGIN_SUCCESS,
      payload: res.data,
    });
  } catch (err) {
    dispatch({
      type: LOGIN_FAIL,
    });
  }
};
