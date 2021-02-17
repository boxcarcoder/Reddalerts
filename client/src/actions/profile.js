import { SUBMIT_PHONE_NUMBER } from './types';
import axios from 'axios';

const submitPhoneNumber = (phoneNumber) => async (dispatch) => {
  try {
    // configuration of the HTTP request to the backend
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    const body = JSON.stringify({
      phoneNumber,
    });

    const res = await axios.post('/api/submitPhoneNumber', body, config);
  } catch (err) {}
};
