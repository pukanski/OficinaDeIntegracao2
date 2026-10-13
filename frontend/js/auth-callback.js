import { getToken, setToken } from "./api.js";

const token = new URLSearchParams(window.location.hash.slice(1)).get("token");

if (token) {
  setToken(token);
  window.history.replaceState(null, "", window.location.pathname); // tira o token da URL
}

window.location.replace(token || getToken() ? "index.html" : "login.html?erro=google");