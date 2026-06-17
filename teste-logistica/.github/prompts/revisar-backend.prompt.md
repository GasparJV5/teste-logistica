# Revisar Backend

Use este prompt para revisar o backend Python/Flask do projeto de logística.

- Analise `mdr/backend/server.py` e verifique a lógica de rotas, persistência SQLite e backups JSON.
- Identifique problemas de segurança, desempenho ou organização do código.
- Sugira melhorias claras sem alterar a arquitetura básica.
- Priorize correções de bugs e pequenas refatorações.

## Tarefas esperadas
- Verificar se há tratamento adequado de erros e dados inválidos.
- Confirmar que o banco SQLite é inicializado corretamente e que a função de backup grava os dados.
- Revisar as rotas REST (`/save`, `/load`, `/backup`, etc.) e validar retornos JSON.
- Sugerir melhorias se houver redundância, código duplicado ou validações faltando.

## Contexto do projeto
- Backend serve frontend estático em `mdr/frontend`.
- Usa SQLite local com backup em `backup_mdr_v2.json`.
- O app foi projetado para ser leve e simples, então não adicione frameworks extras.
