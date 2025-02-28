import axios from "axios";

// Upewnij się, że baseURL odpowiada Twojej konfiguracji serwera.
// W środowisku deweloperskim możesz mieć niezaufany certyfikat SSL – pamiętaj, żeby zaakceptować go w przeglądarce.
const api = axios.create({
  baseURL: "https://127.0.0.1:8000", // Zamień na właściwy adres
  headers: {
    "Content-Type": "application/json",
  },
});

// Jeśli token istnieje, ustaw go domyślnie dla wszystkich zapytań
const token = localStorage.getItem("authToken");
if (token) {
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export default api;
