import { API_URL, requisitar, setToken } from "./api.js";

const elErro = document.getElementById("erro");
const botao = document.getElementById("btn-cadastrar");
const mostrarErro = (msg) => { elErro.textContent = msg; elErro.hidden = !msg; };

async function mensagemDeErro(resp) {
  const corpo = await resp.json().catch(() => null);
  if (typeof corpo?.detail === "string") return corpo.detail; // ex.: "E-mail já cadastrado"
  if (resp.status === 422) return "Confira os dados informados. O e-mail precisa ser válido.";
  return "Não foi possível criar a conta. Tente novamente.";
}

document.getElementById("form-cadastro").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mostrarErro("");

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value;
  const confirmacao = document.getElementById("confirmar-senha").value;

  // mesmas regras do backend (auth_service.validar_dados_cadastro); o servidor revalida
  if (!nome) return mostrarErro("Informe seu nome.");
  if (!email) return mostrarErro("Informe seu e-mail.");
  if (senha.length < 8) return mostrarErro("A senha deve ter pelo menos 8 caracteres.");
  if (senha !== confirmacao) return mostrarErro("As senhas não coincidem.");

  botao.disabled = true;
  botao.textContent = "Criando conta...";
  try {
    const resp = await requisitar("/auth/register", {
      method: "POST",
      body: JSON.stringify({ nome, email, senha }),
    });
    if (!resp.ok) {
      mostrarErro(await mensagemDeErro(resp));
      return;
    }

    // conta criada: já entra direto, sem pedir o login de novo
    const login = await requisitar("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, senha }),
    });
    if (!login.ok) {
      window.location.replace("login.html?cadastro=ok");
      return;
    }
    const { access_token } = await login.json();
    setToken(access_token);
    window.location.replace("index.html");
  } catch {
    mostrarErro("Não foi possível conectar ao servidor.");
  } finally {
    botao.disabled = false;
    botao.textContent = "Criar conta";
  }
});

document.getElementById("btn-google").addEventListener("click", () => {
  window.location.href = `${API_URL}/auth/google/login`; // cria a conta se for o primeiro acesso
});
