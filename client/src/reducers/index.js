import { combineReducers } from 'redux';
import auth from './auth';
import subreddit from './subreddit';

export default combineReducers({
  auth,
  subreddit,
});
