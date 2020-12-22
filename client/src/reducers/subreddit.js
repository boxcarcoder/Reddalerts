/* eslint-disable import/no-anonymous-default-export */
import {
  SUBMIT_SUBREDDIT_INFO,
  SUBMIT_SUBREDDIT_INFO_FAIL,
} from '../actions/types';

const initialState = {
  subreddit: null,
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
        subreddit: {
          name: payload.name,
          keywords: payload.keywords,
        },
        subreddits: [
          {
            name: payload.name,
            keywords: payload.keywords,
          },
          ...state.subreddits,
        ],
      };
    case SUBMIT_SUBREDDIT_INFO_FAIL:
      return {
        ...state,
        error: payload,
      };
    default:
      return state;
  }
}
