# Handoffs entre agentes

Este arquivo descreve como os agentes do projeto devem colaborar e passar trabalho entre si.

## Fluxo recomendável

1. `analista-desenvolvimento.agent.md`
   - inicia a captura de requisitos, identifica lacunas e mapeia o backlog técnico.
   - quando encontra riscos de dados ou ambiguidades de modelo, encaminha para `governanca-dados.agent.md` e/ou `lgpd.agent.md`.

2. `governanca-dados.agent.md`
   - analisa entidades, nomes e qualidade dos dados.
   - se detectar dados pessoais sensíveis ou problemas de retenção, faz handoff para `lgpd.agent.md`.
   - também pode sugerir melhorias estruturais ao `melhoria-continua.agent.md`.

3. `lgpd.agent.md`
   - foca em privacidade, minimização e retenção.
   - se identificar falhas de processo ou gargalos de tratamento de dados, encaminha para `melhoria-continua.agent.md`.

4. `melhoria-continua.agent.md`
   - recebe diagnósticos de riscos, qualidade e requisitos.
   - cria plano de ação com priorização e etapas de melhoria contínua.
   - pode devolver recomendações ao `analista-desenvolvimento.agent.md` para reorganização do backlog.

## Exemplo de uso conjunto

- Primeiro, use `analista-desenvolvimento.agent.md` para entender os requisitos e o escopo.
- Em seguida, execute `governanca-dados.agent.md` para validar entidades e qualidade dos dados.
- Depois, execute `lgpd.agent.md` se houver tratamento de dados pessoais ou retenção.
- Por fim, use `melhoria-continua.agent.md` para priorizar ações e gerar um plano de melhoria.

## Nota
Cada agente deve produzir recomendações claras e acionáveis, e os handoffs devem ser usados para dividir o trabalho sem duplicar análises.
