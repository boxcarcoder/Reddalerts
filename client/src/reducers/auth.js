/* eslint-disable import/no-anonymous-default-export */
import {
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  REGISTER_SUCCESS,
  REGISTER_FAIL,
} from '../actions/types';

const initialState = {
  token: localStorage.getItem('token'),
  loggedInUser: null,
  loading: false,
  isAuthenticated: false,
};

export default function (state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case LOGIN_SUCCESS:
    case REGISTER_SUCCESS:
      localStorage.setItem('token', payload.token);
      return {
        ...state,
        isAuthenticated: true,
        loggedInUser: payload.user,
      };
    case LOGIN_FAIL:
    case REGISTER_FAIL:
      return {
        ...state,
        isAuthenticated: false,
      };
    default:
      return state;
  }
}
