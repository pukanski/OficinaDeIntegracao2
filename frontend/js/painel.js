import { exigirUsuario, limparToken, obterHistorico, obterStats } from "./api.js";

const LIMITE_HISTORICO = 50;

const usuario = await exigirUsuario();

const definir = (id, texto) => { document.getElementById(id).textContent = texto; };
const elErro = document.getElementById("erro");
const avisar = (msg) => { elErro.textContent = msg; elErro.hidden = false; };

function formatarTempo(segundos) {
  const m = Math.floor(segundos / 60);
  const s = segundos % 60;
  return m > 0 ? `${m}min ${s}s` : `${s}s`;
}

function formatarData(iso) {
  const data = new Date(iso);
  return iso && !Number.isNaN(data.getTime())
    ? data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })
    : "—";
}

function criarSelo(texto, tipo) {
  const selo = document.createElement("span");
  selo.className = `selo selo-${tipo}`;
  selo.textContent = texto;
  return selo;
}

function criarCelula(conteudo, classe = "") {
  const td = document.createElement("td");
  if (classe) td.className = classe;
  if (conteudo instanceof Node) td.appendChild(conteudo);
  else td.textContent = conteudo;
  return td;
}

function mostrarResumo(stats) {
  definir("fases-concluidas", `${stats.fases_concluidas} / ${stats.total_fases}`);
  definir("total-tentativas", String(stats.total_tentativas));
  definir("tempo-total", formatarTempo(stats.tempo_total_segundos));

  const barra = document.getElementById("barra-progresso");
  barra.setAttribute("aria-valuemax", String(stats.total_fases));
  barra.setAttribute("aria-valuenow", String(stats.fases_concluidas));
  const percentual = stats.total_fases ? (stats.fases_concluidas / stats.total_fases) * 100 : 0;
  barra.firstElementChild.style.width = `${percentual}%`;

  const corpo = document.getElementById("tabela-fases");
  corpo.replaceChildren();
  for (const f of stats.por_fase) {
    const linha = document.createElement("tr");
    linha.dataset.testid = `linha-fase-${f.fase_id}`;
    linha.append(
      criarCelula(`${f.fase_id}. ${f.titulo}`),
      criarCelula(f.concluida ? criarSelo("Concluída", "ok") : criarSelo("Pendente", "pendente")),
      criarCelula(String(f.tentativas), "num"),
      criarCelula(formatarTempo(f.tempo_segundos), "num"),
    );
    corpo.appendChild(linha);
  }
}

function mostrarHistorico(tentativas) {
  document.getElementById("historico-vazio").hidden = tentativas.length > 0;
  document.getElementById("historico-tabela").hidden = tentativas.length === 0;

  const nota = document.getElementById("historico-nota");
  nota.hidden = tentativas.length < LIMITE_HISTORICO;
  nota.textContent = `Mostrando as ${LIMITE_HISTORICO} tentativas mais recentes.`;

  const corpo = document.getElementById("tabela-historico");
  corpo.replaceChildren();
  for (const t of tentativas) {
    const linha = document.createElement("tr");
    linha.dataset.testid = `tentativa-${t.id}`;
    linha.append(
      criarCelula(formatarData(t.criado_em)),
      criarCelula(`${t.fase_id}. ${t.fase_titulo}`),
      criarCelula(t.concluida ? criarSelo("Concluída", "ok") : criarSelo("Não concluída", "parcial")),
      criarCelula(String(t.movimentos), "num"),
      criarCelula(formatarTempo(t.tempo_segundos), "num"),
    );
    corpo.appendChild(linha);
  }
}

try {
  mostrarResumo(await obterStats());
} catch (erro) {
  avisar(`Não foi possível carregar o resumo: ${erro.message}`);
}

try {
  mostrarHistorico(await obterHistorico(LIMITE_HISTORICO));
} catch (erro) {
  avisar(`Não foi possível carregar o histórico: ${erro.message}`);
}

definir("nome-usuario", `Olá, ${usuario.nome}`);

document.getElementById("btn-sair").addEventListener("click", () => {
  limparToken();
  window.location.replace("login.html");
});

document.getElementById("carregando").hidden = true;
document.getElementById("conteudo").hidden = false;
