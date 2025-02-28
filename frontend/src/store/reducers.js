import {
    LOGIN_SUCCESS,
    LOGIN_FAILURE,
    REGISTER_SUCCESS,
    REGISTER_FAILURE,
  } from "./actions";
  
  const initialState = {
    token: localStorage.getItem("authToken") || null,
    error: null,
  };
  
  const authReducer = (state = initialState, action) => {
    switch (action.type) {
      case LOGIN_SUCCESS:
        return { ...state, token: action.payload, error: null };
      case LOGIN_FAILURE:
        return { ...state, token: null, error: action.error };
      case REGISTER_SUCCESS:
        return { ...state, error: null };
      case REGISTER_FAILURE:
        return { ...state, error: action.error };
      default:
        return state;
    }
  };
  
  export default authReducer;
  