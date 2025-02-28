import { createStore, applyMiddleware, combineReducers } from "redux";
import { thunk } from "redux-thunk";
import authReducer from "./reducers";

const rootReducer = combineReducers({
  auth: authReducer,
  // Dodaj inne reducery, jeśli zajdzie potrzeba
});

const store = createStore(rootReducer, applyMiddleware(thunk));

export default store;
