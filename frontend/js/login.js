import { API_URL, requisitar, setToken } from "./api.js";

const MENSAGENS = {
  google: "Não foi possível entrar com o Google. Tente novamente.",
  google_email: "Sua conta Google precisa ter um e-mail verificado.",
};

const elErro = document.getElementById("erro");
const mostrarErro = (msg) => { elErro.textContent = msg; elErro.hidden = !msg; };

mostrarErro(MENSAGENS[new URLSearchParams(window.location.search).get("erro")] ?? "");

document.getElementById("form-login").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mostrarErro("");

  let resp;
  try {
    resp = await requisitar("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value,
      }),
    });
  } catch {
    mostrarErro("Não foi possível conectar ao servidor.");
    return;
  }

  if (!resp.ok) {
    mostrarErro(resp.status === 401 ? "E-mail ou senha inválidos" : "Erro ao entrar. Tente novamente.");
    return;
  }
  const { access_token } = await resp.json();
  setToken(access_token);
  window.location.replace("index.html");
});

document.getElementById("btn-google").addEventListener("click", () => {
  window.location.href = `${API_URL}/auth/google/login`;
});