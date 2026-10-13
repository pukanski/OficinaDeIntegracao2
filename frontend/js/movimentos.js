// Mesmas regras do backend (app/services/fase_service.py). O servidor revalida tudo.
const DELTAS = {
  cima: [0, -1],
  baixo: [0, 1],
  esquerda: [-1, 0],
  direita: [1, 0],
};

// Retorna a nova posição, ou a mesma se o movimento for inválido (fora do grid ou obstáculo).
export function mover(fase, posicao, direcao) {
  const [dx, dy] = DELTAS[direcao];
  const x = posicao.x + dx;
  const y = posicao.y + dy;
  const dentro = x >= 0 && x < fase.largura && y >= 0 && y < fase.altura;
  const bloqueado = fase.obstaculos.some((o) => o.x === x && o.y === y);
  return dentro && !bloqueado ? { x, y } : posicao;
}

export const chegou = (fase, posicao) =>
  posicao.x === fase.destino.x && posicao.y === fase.destino.y;