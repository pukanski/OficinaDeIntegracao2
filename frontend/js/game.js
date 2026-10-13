import { enviarProgresso, exigirUsuario, limparToken, listarFases } from "./api.js";
import { renderizarGrid } from "./grid.js";
import { chegou, mover } from "./movimentos.js";

const TECLAS = {
  ArrowUp: "cima",
  ArrowDown: "baixo",
  ArrowLeft: "esquerda",
  ArrowRight: "direita",
};

const usuario = await exigirUsuario();

const el = {
  titulo: document.getElementById("titulo-fase"),
  descricao: document.getElementById("descricao-fase"),
  nome: document.getElementById("nome-usuario"),
  lista: document.getElementById("lista-fases"),
  grid: document.getElementById("grid"),
  mensagem: document.getElementById("mensagem"),
  proxima: document.getElementById("btn-proxima"),
};

let fases = [];
let fase = null;
let posicao = null;
let movimentos = [];
let inicioTentativa = null; // o relógio começa no primeiro movimento
let finalizada = false;     // true depois de chegar ao destino: bloqueia novos movimentos
let enviando = false;

function mostrarMensagem(texto) {
  el.mensagem.textContent = texto;
}

function desenhar() {
  renderizarGrid(el.grid, fase, posicao);
}

function renderizarLista() {
  el.lista.replaceChildren();
  for (const f of fases) {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "btn-fase";
    botao.dataset.testid = `fase-${f.id}`;
    botao.disabled = !f.liberada;
    botao.classList.toggle("ativa", fase?.id === f.id);
    botao.textContent = `${f.concluida ? "✔" : f.liberada ? "▶" : "🔒"} ${f.id}. ${f.titulo}`;
    botao.addEventListener("click", () => iniciarFase(f));
    el.lista.appendChild(botao);
  }
}

function iniciarFase(f) {
  fase = f;
  posicao = { ...f.inicio };
  movimentos = [];
  inicioTentativa = null;
  finalizada = false;
  el.proxima.hidden = true;
  el.titulo.textContent = `Fase ${f.id}: ${f.titulo}`;
  el.descricao.textContent = f.descricao;
  mostrarMensagem("");
  desenhar();
  renderizarLista();
}

async function atualizarFases() {
  fases = await listarFases();
  renderizarLista();
}

function escolherFaseInicial() {
  return fases.find((f) => f.liberada && !f.concluida) ?? fases[fases.length - 1];
}

// Envia a tentativa atual. Quem decide se a fase foi concluída é o servidor.
async function registrarTentativa() {
  enviando = true;
  const tempo = inicioTentativa ? Math.round((Date.now() - inicioTentativa) / 1000) : 0;
  try {
    const resultado = await enviarProgresso({
      fase_id: fase.id,
      movimentos,
      tempo_segundos: tempo,
    });
    await atualizarFases();
    return resultado;
  } finally {
    enviando = false;
  }
}

async function aoChegar() {
  finalizada = true;
  try {
    const resultado = await registrarTentativa();
    if (!resultado.concluida) {
      mostrarMensagem("O servidor não validou a conclusão. Reinicie a fase.");
      return;
    }
    const proxima = fases.find((f) => f.id === fase.id + 1);
    mostrarMensagem(`Fase concluída em ${resultado.movimentos_validos} movimentos! 🎉`);
    el.proxima.hidden = !proxima;
  } catch (erro) {
    mostrarMensagem(`Não foi possível salvar o progresso: ${erro.message}`);
  }
}

function tentarMover(direcao) {
  if (!fase || finalizada || enviando) return;
  const nova = mover(fase, posicao, direcao);
  if (nova === posicao) {
    mostrarMensagem("Movimento inválido: parede ou limite do grid.");
    return;
  }
  mostrarMensagem("");
  inicioTentativa ??= Date.now();
  posicao = nova;
  movimentos.push(direcao);
  desenhar();
  if (chegou(fase, posicao)) aoChegar();
}

async function reiniciar() {
  if (enviando) return;
  // abandonar uma tentativa em andamento conta como tentativa não concluída
  if (movimentos.length > 0 && !finalizada) {
    try {
      await registrarTentativa();
    } catch (erro) {
      mostrarMensagem(`Não foi possível salvar a tentativa: ${erro.message}`);
    }
  }
  iniciarFase(fases.find((f) => f.id === fase.id));
}

document.querySelectorAll("[data-direcao]").forEach((botao) =>
  botao.addEventListener("click", () => tentarMover(botao.dataset.direcao))
);

document.addEventListener("keydown", (evento) => {
  const direcao = TECLAS[evento.key];
  if (!direcao) return;
  evento.preventDefault(); // evita rolar a página
  tentarMover(direcao);
});

document.getElementById("btn-reiniciar").addEventListener("click", reiniciar);
el.proxima.addEventListener("click", () => {
  const proxima = fases.find((f) => f.id === fase.id + 1);
  if (proxima) iniciarFase(proxima);
});
document.getElementById("btn-sair").addEventListener("click", () => {
  limparToken();
  window.location.replace("login.html");
});

el.nome.textContent = `Olá, ${usuario.nome}`;

try {
  await atualizarFases();
  iniciarFase(escolherFaseInicial());
} catch (erro) {
  mostrarMensagem(`Não foi possível carregar as fases: ${erro.message}`);
}

document.getElementById("carregando").hidden = true;
document.getElementById("conteudo").hidden = false;