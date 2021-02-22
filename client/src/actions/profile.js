import { SUBMIT_PHONE_NUMBER, DELETE_PHONE_NUMBER } from './types';
import axios from 'axios';

export const submitPhoneNumber = ({ id, phoneNumber }) => async (dispatch) => {
  try {
    // configuration of the HTTP request to the backend
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    const body = JSON.stringify({
      id,
      phoneNumber,
    });

    const res = await axios.post('/api/submitPhoneNumber', body, config);

    // dispatch({
    //   type: SUBMIT_PHONE_NUMBER,
    //   payload:
    // })
  } catch (err) {}
};

export const deletePhoneNumber = (id) => async (dispatch) => {
  try {
    const res = await axios.delete('/api/deletePhoneNumber', {
      params: {
        id,
      },
    });

    dispatch({
      type: DELETE_PHONE_NUMBER,
    });
  } catch (err) {}
};
