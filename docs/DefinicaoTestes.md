# Definição dos Testes Automatizados — Projeto ELLP

## 1. Ferramentas

| Nível | Ferramenta | O que vai validar |
|-------|-----------|----------------|
| Unitário | pytest | Lógica de negócio isolada (services), sem tocar banco/rede |
| Integração | pytest + testClient (fastAPI) | Endpoints da API contra um postgreSQL de teste real |
| End-to-end | selenium | Fluxo completo no navegador (front-end + back-end + banco) |
| Cobertura | pytest-cov | Percentual de cobertura da camada de serviço (meta esperada: 70–80%) |

## 2. Mapeamento de requisitos para casos de teste

**As rotas são apenas exemplos, podendo ser alteradas**

| ID | RF relacionado | Nível | Descrição do caso de teste | Resultado esperado |
|----|-----------------|-------|------------------------------|----------------------|
| CT01 | RF01 | Unitário | Validar regras de cadastro (e-mail em formato válido, senha com tamanho mínimo) | Erro de validação quando dados inválidos; sucesso quando válidos |
| CT02 | RF01 | Integração | POST /auth/register com dados válidos | Usuário criado no banco de teste, retorno 201 |
| CT03 | RF01 | Integração | POST /auth/register com e-mail já cadastrado | Retorno 400/409, usuário não duplicado |
| CT04 | RF02 | Unitário | Verificar hashing e comparação de senha | Senha correta autentica; senha incorreta falha |
| CT05 | RF02 | Integração | POST /auth/login com credenciais válidas | Retorno 200 com token JWT válido |
| CT06 | RF02 | Integração | POST /auth/login com credenciais inválidas | Retorno 401, nenhum token gerado |
| CT07 | RF03 | Integração | Fluxo de login com Google | Usuário autenticado/criado a partir dos dados do Google |
| CT08 | RF04 | E2E | Acessar a tela principal após login | Grid e personagem são renderizados |
| CT09 | RF05 | Unitário | Validar movimento do personagem (frente/trás/esquerda/direita) na lógica de posição | Posição atualizada corretamente |
| CT10 | RF05 | E2E | Clicar nos botões de movimento na tela | Personagem se move na direção esperada |
| CT11 | RF06 | E2E | Pressionar as setas do teclado | Personagem se move na direção correspondente |
| CT12 | RF07 | Unitário | Tentar mover o personagem para fora do grid ou sobre obstáculo | Movimento é bloqueado, posição não muda |
| CT13 | RF08 | Unitário | Validar lógica de conclusão de fase (chegada ao destino) | Fase marcada como concluída quando objetivo é atingido |
| CT14 | RF08 | Integração | GET /game/stages retorna fases disponíveis | Lista de fases correta, condizente com o progresso do usuário |
| CT15 | RF09 | Integração | POST /game/progress salva avanço do usuário | Progresso persistido no banco de teste |
| CT16 | RF09 | E2E | Completar uma fase e recarregar a página | Progresso salvo é mantido após recarregar a página |
| CT17 | RF10 | Integração | POST /auth/logout invalida a sessão/token | Requisições subsequentes com o token antigo retornam 401 |
| CT18 | RF11 | Integração | GET /users/me/stats retorna dados de desempenho | Dados batem com o progresso salvo no banco |

## 3. Critérios Gerais
- Todo endpoint novo deve ter pelo menos um teste de integração cobrindo o caso de sucesso e um cobrindo o principal caso de erro.
- Toda regra de negócio na camada de serviço deve ter teste unitário antes de ser integrada à API.
- Os fluxos críticos (cadastro, login, login Google, mover personagem, salvar progresso) devem ter pelo menos um teste end-to-end.
- Os testes de integração e2e devem rodar contra o banco de teste (dbTest, porta 5433) definido no docker, nunca contra o banco de desenvolvimento.
- A suíte de testes deve rodar automaticamente pelo GitHub Actions a cada push e pull request.
