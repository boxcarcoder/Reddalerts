/* eslint-disable import/no-anonymous-default-export */
import {
  SUBMIT_SUBREDDIT_INFO,
  SUBMIT_SUBREDDIT_INFO_FAIL,
  FETCH_SUBREDDITS,
  FETCH_SUBREDDITS_FAIL,
  DELETE_SUBREDDIT,
  DELETE_SUBREDDIT_FAIL,
  UPDATE_SUBREDDIT_KEYWORDS,
} from '../actions/types';

const initialState = {
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
        subreddits: [...state.subreddits, payload.subreddit],
      };
    case SUBMIT_SUBREDDIT_INFO_FAIL:
      return {
        ...state,
        error: payload,
      };
    case UPDATE_SUBREDDIT_KEYWORDS:
      return {
        ...state,
        subreddits: state.subreddits.map((subreddit) =>
          subreddit.subreddit_name === payload.subreddit.subreddit_name
            ? {
                ...subreddit,
                keywords: payload.subreddit.keywords,
              }
            : subreddit
        ),
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
    case DELETE_SUBREDDIT:
      return {
        ...state,
        subreddits: payload.subreddits,
      };
    case DELETE_SUBREDDIT_FAIL:
      return {
        ...state,
        error: payload,
      };
    default:
      return state;
  }
}
