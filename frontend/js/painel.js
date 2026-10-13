import { exigirUsuario, limparToken, obterStats } from "./api.js";

await exigirUsuario();

function formatarTempo(segundos) {
  const m = Math.floor(segundos / 60);
  const s = segundos % 60;
  return m > 0 ? `${m}min ${s}s` : `${s}s`;
}

const definir = (id, texto) => { document.getElementById(id).textContent = texto; };

try {
  const stats = await obterStats();

  definir("fases-concluidas", `${stats.fases_concluidas} / ${stats.total_fases}`);
  definir("total-tentativas", String(stats.total_tentativas));
  definir("tempo-total", formatarTempo(stats.tempo_total_segundos));

  const corpo = document.getElementById("tabela-fases");
  corpo.replaceChildren();
  for (const f of stats.por_fase) {
    const linha = document.createElement("tr");
    linha.dataset.testid = `linha-fase-${f.fase_id}`;
    const celulas = [
      `${f.fase_id}. ${f.titulo}`,
      f.concluida ? "✔ Concluída" : "Pendente",
      String(f.tentativas),
      formatarTempo(f.tempo_segundos),
    ];
    for (const texto of celulas) {
      const td = document.createElement("td");
      td.textContent = texto;
      linha.appendChild(td);
    }
    corpo.appendChild(linha);
  }
} catch (erro) {
  const aviso = document.getElementById("erro");
  aviso.textContent = `Não foi possível carregar o painel: ${erro.message}`;
  aviso.hidden = false;
}

document.getElementById("btn-sair").addEventListener("click", () => {
  limparToken();
  window.location.replace("login.html");
});

document.getElementById("carregando").hidden = true;
document.getElementById("conteudo").hidden = false;