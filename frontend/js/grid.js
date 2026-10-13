const mesmaCelula = (a, b) => a.x === b.x && a.y === b.y;

export function renderizarGrid(container, fase, posicao) {
  container.replaceChildren();
  container.style.gridTemplateColumns = `repeat(${fase.largura}, 1fr)`;

  for (let y = 0; y < fase.altura; y++) {
    for (let x = 0; x < fase.largura; x++) {
      const celula = { x, y };
      const ehPersonagem = mesmaCelula(celula, posicao);
      const ehDestino = mesmaCelula(celula, fase.destino);
      const ehObstaculo = fase.obstaculos.some((o) => mesmaCelula(o, celula));

      const div = document.createElement("div");
      div.className = "celula";
      div.dataset.testid = ehPersonagem ? "personagem" : `celula-${x}-${y}`;

      if (ehObstaculo) { div.classList.add("obstaculo"); div.textContent = "🪨"; }
      if (ehDestino) { div.classList.add("destino"); div.textContent = "🏁"; }
      if (ehPersonagem) { div.classList.add("personagem"); div.textContent = "🤖"; }

      container.appendChild(div);
    }
  }
}