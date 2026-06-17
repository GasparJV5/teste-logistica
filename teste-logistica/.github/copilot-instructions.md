# GitHub Copilot Instructions

## Sobre este repositório
Este projeto é uma aplicação web de controle logístico com backend Python/Flask e frontend estático em HTML/JavaScript.

## Como ajudar
- Foque em manter o backend leve, com rotas REST claras para salvar, carregar e fazer backup de dados.
- No frontend, preserve a lógica de blocos operacionais, cadastro de processos e filtros de consulta.
- Evite alterações grandes de arquitetura sem necessidade; priorize correções e melhorias incrementais.

## Padrões esperados
- Código Python simples e funcional no backend.
- UI estática com JavaScript vanilla no frontend.
- Dados persistidos em SQLite e em arquivo JSON de backup.
- Mensagens e labels em português.

## Quando gerar código novo
- Se for necessária uma nova rota ou recurso, adicione documentação clara no backend (`server.py`) e mantenha o frontend compatível.
- Se for necessário adicionar um novo arquivo, prefira colocá-lo em `mdr/backend` ou `mdr/frontend`.

## Uso de agentes e prompts
- O workspace inclui agentes em `agentes/` para análise de requisitos, governança de dados, LGPD e melhoria contínua.
- Use os prompt files em `.github/prompts/` para acionar cada agente com instruções claras e reutilizáveis.
- Cada agente deve focar na sua área: requisitos e backlog, qualidade de dados, privacidade ou plano de ação.

## Não alterar sem validação
- Não remova o suporte de backup JSON em `mdr/backend/backup_mdr_v2.json`.
- Não substitua o frontend atual por frameworks como React ou Vue sem autorização.
