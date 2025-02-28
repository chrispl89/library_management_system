import api from "../services/api";

// Typy akcji
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_FAILURE = "LOGIN_FAILURE";
export const REGISTER_SUCCESS = "REGISTER_SUCCESS";
export const REGISTER_FAILURE = "REGISTER_FAILURE";

// Akcja logowania z wykorzystaniem JWT
export const login = (credentials) => async (dispatch) => {
    try {
      // Używamy endpointu JWT
      const response = await api.post("/api/token/", credentials);
      // W odpowiedzi otrzymujemy zwykle 'access' oraz opcjonalnie 'refresh'
      const { access } = response.data;
      localStorage.setItem("authToken", access);
      api.defaults.headers.common["Authorization"] = `Bearer ${access}`;
      dispatch({ type: LOGIN_SUCCESS, payload: access });
    } catch (error) {
      dispatch({ type: LOGIN_FAILURE, error: error.message });
    }
  };

// Akcja rejestracji
export const register = (data) => async (dispatch) => {
    try {
      // Endpoint rejestracji zgodnie z listą: /api/register/
      const response = await api.post("/api/register/", data);
      dispatch({ type: REGISTER_SUCCESS, payload: response.data });
    } catch (error) {
      dispatch({ type: REGISTER_FAILURE, error: error.message });
    }
  };
