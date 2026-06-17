# Agentes do projeto

Este diretório reúne agentes de análise e revisão para o projeto.

## Agentes disponíveis

- `analista-desenvolvimento.agent.md`
  - Foco: requisitos, backlog técnico, arquitetura e documentação.

- `governanca-dados.agent.md`
  - Foco: mapeamento de entidades, nomenclatura, qualidade de dados e rastreabilidade.

- `lgpd.agent.md`
  - Foco: privacidade, dados pessoais, minimização e retenção.

- `melhoria-continua.agent.md`
  - Foco: identificação de gargalos, causa raiz, priorização e plano de ação.

## Como usar

1. Leia o agente mais adequado para a tarefa.
2. Use os prompt files correspondentes em `.github/prompts/` para acionar o agente.
3. Execute os prompts no chat do VS Code para iniciar o agente com instruções claras.
4. Use `agentes/handoffs.md` para entender como encadear análises entre os agentes.

## Exemplo de uso

- Abra o arquivo `agentes/analista-desenvolvimento.agent.md` para entender o papel do agente.
- Em seguida, use o prompt `.github/prompts/analista-desenvolvimento.prompt.md` no chat.
- Se o agente identificar problemas de dados, continue com `governanca-dados` ou `lgpd`.
- Por fim, aplique `melhoria-continua` para gerar um plano de ação.

## Handoffs

Veja `agentes/handoffs.md` para o fluxo recomendado de colaboração entre agentes.
