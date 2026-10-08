# Planejamento do Projeto

**Proposta escolhida:** Ferramenta visual para programação de um pequeno personagem que permita andar pela tela usando comandos básicos (frente, trás, direita, esquerda). O controle pode ser feito com botões na tela ou setas do teclado

**Stack proposta:** Back-end em Python + Front-end em HTML/JavaScript, com login/cadastro próprio e login com Google.

---

## 1. Requisitos Funcionais (RF)

| Código | Requisito |
|--------|-----------|
| RF01 | O sistema deve permitir cadastro de usuário com nome, e-mail e senha |
| RF02 | O sistema deve permitir login com e-mail e senha |
| RF03 | O sistema deve permitir login via conta Google (OAuth 2.0) |
| RF04 | O sistema deve exibir uma tela com um cenário/grid e um personagem posicionado nele |
| RF05 | O usuário deve poder mover o personagem (frente, trás, esquerda, direita) usando botões na tela |
| RF06 | O usuário deve poder mover o personagem usando as setas do teclado |
| RF07 | O sistema deve validar movimentos inválidos (ex: personagem não pode sair do grid ou atravessar obstáculos) |
| RF08 | O sistema deve apresentar desafios/fases simples (ex: levar o personagem até um destino, desviando de obstáculos) — dá caráter pedagógico à ferramenta, alinhado ao ELLP |
| RF09 | O sistema deve salvar o progresso do usuário (fases concluídas, tentativas) |
| RF10 | O sistema deve permitir logout |
| RF11 | O sistema deve exibir um histórico/painel simples com o desempenho do usuário |

## 2. Arquitetura em Alto Nível

**Arquiteura:** Arquitetura em camadas, cliente-servidor:

**Decisões de arquitetura:**
- Separação clara entre front-end e back-end, comunicando via API REST.
- Camada de serviço isolada dos controllers, para poder ser testada isoladamente.
- Autenticação google isolada em um módulo de infraestrutura.

## 3. Tecnologias

| Camada | Tecnologia sugerida |
|--------|----------------------|
| Linguagem back-end | Python |
| Framework web | FastAPI |
| ORM / Banco | SQLAlchemy + PostgreSQL |
| Migrações de banco | Alembic |
| Autenticação própria | OAuth2PasswordBearer + JWT + hashing de senha |
| Autenticação Google | Authlib |
| Front-end | HTML5 + CSS + JavaScript |
| Comunicação Front↔Back | Fetch API consumindo endpoints REST em JSON |
| Testes back-end | pytest + httpx |
| Cobertura de testes | pytest-cov |
| Testes end-to-end | Selenium |
| Versionamento | Git + GitHub |
| Gestão de tarefas | GitHub Issues + GitHub Projects |
| Integração contínua | GitHub Actions |

## 4. Estratégia de Automação de Testes

- **Testes unitários (Python/pytest):** cobrir a camada de serviço — validação de movimento, lógica de fases, cálculo de progresso.
- **Testes de integração:** testar os endpoints da API (cadastro, login, login Google simulado, movimentação, persistência de progresso) usando o testClient do fastAPI, contra um banco postgreSQL de teste.
- **Testes end-to-end:** simular o fluxo completo no navegador (cadastro → login → mover personagem → completar fase) com selenium, rodando contra a aplicação completa (front-end + fastAPI + postgreSQL) em ambiente de teste.
- **Cobertura:** medir com pytest-cov e reportar no README/CI;.
- **Execução:** todos os testes rodando automaticamente via gitHub Actions a cada push e pull request.

## 5. Cronograma

| Semana | Datas | Fase | Atividades planejadas |
|--------|-------|------|------------------------|
| Semana 6 | 21/09 – 27/09/2026 | Sprint 1 | Setup do projeto; definição final do modelo de dados |
| Semana 7 | 28/09 – 04/10/2026 | Sprint 1 | Implementação de cadastro e login próprio; início da integração do login com Google |
| Semana 8 | 05/10 – 11/10/2026 | Sprint 1 | Renderização do grid e do personagem; movimentação via botões na tela e via teclado |
| Semana 9 | 12/10 – 18/10/2026 | Sprint 1 | Testes automatizados da sprint 1; gravação do vídeo de sprint review |
| Semana 10 | 19/10 – 25/10/2026 | Revisão sprint 1 | Recuperação da sprint 1 |
| Semana 11 | 26/10 – 01/11/2026 | Sprint 2 | Planejamento e implementação do sistema de fases/desafios |
| Semana 12 | 02/11 – 08/11/2026 | Sprint 2 | Validação de obstáculos/limites do grid; persistência de progresso do usuário |
| Semana 13 | 09/11 – 15/11/2026 | Sprint 2 | Implementação de logout; Testes automatizados da sprint 2 |
| Semana 14 | 16/11 – 22/11/2026 | Sprint 2 | Testes automatizados da sprint 2 |
| Semana 15 | 23/11 – 29/11/2026 | Sprint 2 | Ajustes finais, gravação do vídeo de sprint review, preparação da documentação |
| Semana 16 | 30/11 – 06/12/2026 | Segunda chamada | -- |
| Semana 17 | — | Encerramento | Recuperação da sprint 2 e fechamento da entrega do projeto |

## 6. Backlog Inicial

**Sprint 1:**
- [ ] Setup do repositório e ambiente
- [ ] Cadastro de usuário
- [ ] Login com e-mail/senha
- [ ] Login com google
- [ ] Renderização do grid e personagem
- [ ] Movimentação via botões na tela
- [ ] Movimentação via teclado
- [ ] Testes unitários e de integração da sprint 1
- [ ] Vídeo de sprint review

**Sprint 2:**
- [ ] Sistema de fases/desafios
- [ ] Validação de obstáculos/limites do grid
- [ ] Persistência de progresso do usuário
- [ ] Logout
- [ ] Testes unitários e de integração da sprint 2
- [ ] Vídeo de sprint review
