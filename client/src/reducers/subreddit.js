/* eslint-disable import/no-anonymous-default-export */
import {
  SUBMIT_SUBREDDIT_INFO,
  SUBMIT_SUBREDDIT_INFO_FAIL,
  FETCH_SUBREDDITS,
  FETCH_SUBREDDITS_FAIL,
} from '../actions/types';

const initialState = {
  // subreddit: null,
  subreddits: [],
  loading: false,
  error: {},
};

export default function (state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case SUBMIT_SUBREDDIT_INFO:
      return {
        ...state,
        // subreddit: {
        //   name: payload.name,
        //   keywords: payload.keywords,
        // },
        subreddits: [
          ...state.subreddits,
          {
            name: payload.name,
            keywords: payload.keywords,
          },
        ],
      };
    case SUBMIT_SUBREDDIT_INFO_FAIL:
      return {
        ...state,
        error: payload,
      };
    case FETCH_SUBREDDITS:
      return {
        ...state,
        subreddits: payload.subreddits,
      };
    case FETCH_SUBREDDITS_FAIL:
      return {
        ...state,
        error: payload,
      };
    default:
      return state;
  }
}
