export const API_URL = "http://localhost:8000";
const CHAVE_TOKEN = "token";

export const getToken = () => localStorage.getItem(CHAVE_TOKEN);
export const setToken = (token) => localStorage.setItem(CHAVE_TOKEN, token);
export const limparToken = () => localStorage.removeItem(CHAVE_TOKEN);

export async function requisitar(caminho, opcoes = {}) {
  const token = getToken();
  return fetch(`${API_URL}${caminho}`, {
    ...opcoes,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...opcoes.headers,
    },
  });
}

export async function exigirUsuario() {
  try {
    const resp = await requisitar("/auth/me");
    if (resp.ok) return await resp.json();
  } catch {
    // API fora do ar: trata como não autenticado
  }
  limparToken();
  window.location.replace("login.html");
  return new Promise(() => {});
}

export async function requisitarJson(caminho, opcoes = {}) {
  const resp = await requisitar(caminho, opcoes);
  if (resp.status === 401) {
    limparToken();
    window.location.replace("login.html");
    return new Promise(() => {});
  }
  const corpo = await resp.json().catch(() => null);
  if (!resp.ok) {
    const detalhe = corpo?.detail;
    throw new Error(typeof detalhe === "string" ? detalhe : "Erro ao comunicar com o servidor");
  }
  return corpo;
}

export const listarFases = () => requisitarJson("/fases");
export const obterStats = () => requisitarJson("/stats");
export const obterHistorico = (limite = 50) => requisitarJson(`/historico?limite=${limite}`);
export const enviarProgresso = (dados) =>
  requisitarJson("/progresso", { method: "POST", body: JSON.stringify(dados) });