import {
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  REGISTER_SUCCESS,
  REGISTER_FAIL,
} from './types';
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

    console.log('heard back from login api route.');
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

export const register = ({ username, email, password }) => async (dispatch) => {
  try {
    // configuration of the HTTP request to the backend
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    // Convert JS object into JSON to send to Flask.
    const body = JSON.stringify({ username, email, password });

    // Store the logged in user's token into a redux state for authentication purposes.
    const res = await axios.post('/api/register', body, config);

    dispatch({
      type: REGISTER_SUCCESS,
      payload: res.data,
    });
  } catch (err) {
    dispatch({
      type: REGISTER_FAIL,
    });
  }
};
