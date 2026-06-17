a {
    text-decoration: none;
    color: #464feb;
}
tr th, tr td {
    border: 1px solid #e6e6e6;
}
tr th {
    background-color: #f5f5f5;
}
Boa — agora você já está **na fase de usar de verdade**, não mais na fase de instalar. Pelo que você mostrou, o chat do Copilot já respondeu e está funcionando no VS Code. O próximo passo é aprender **como pedir**, **como configurar** e **como deixar o assistente “entender” seu projeto melhor**. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices)

---

# 1) Boas práticas para usar o chat no VS Code

## A. Escolha a superfície certa para a tarefa

O VS Code hoje separa a IA em modos diferentes, e usar o modo certo economiza tempo:

- **Chat view**: para perguntas, brainstorming, análise do projeto e tarefas de código no workspace. Atalho no Windows/Linux: **Ctrl+Alt+I**. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)
- **Inline chat**: para editar algo pontual **dentro do arquivo**, como refatorar uma função ou adicionar tratamento de erro. Atalho no Windows/Linux: **Ctrl+I**. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)
- **Quick Chat**: para uma consulta rápida sem “abrir uma sessão grande”. Atalho no Windows/Linux: **Ctrl+Shift+Alt+L**. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)
- **Agents / Plan**: para mudanças maiores, multi-arquivo ou quando você quer que a IA pense em um plano antes de alterar o projeto. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices)

### Regra simples

- **Perguntar/entender** → Chat
- **Alterar um trecho específico** → Inline chat
- **Fazer feature/refactor grande** → Agent / Plan

---

## B. Faça prompts com contexto e formato de saída

A documentação do VS Code recomenda ser **específico**, fornecer **contexto relevante** e escrever **instruções claras**. Você também pode adicionar contexto com**`#`-mentions** para arquivos, símbolos e outras referências do projeto. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)

### Estrutura de prompt que funciona muito bem

Use esse molde:

Objetivo:
Contexto:
Restrições:
Formato da resposta:

### Exemplo bom para o seu caso

Objetivo: melhorar a organização do backend Flask.
Contexto: projeto de controle/logística com frontend estático e SQLite.
Restrições: não quebrar as rotas existentes, manter nomes em português.
Formato da resposta: primeiro explique o problema, depois proponha a estrutura de pastas, e por fim gere os arquivos.

### Exemplo fraco

melhora isso

### Exemplo forte

analise o server.py e proponha uma refatoração para separar rotas, acesso ao banco e regras de negócio. 
Não altere os endpoints existentes. 
Me devolva:
1. diagnóstico,
2. estrutura de pastas,
3. código dos arquivos novos,
4. passos para testar.

---

## C. Peça “plano primeiro, código depois”

Para tarefa maior, uma prática excelente é pedir primeiro:

antes de escrever código, faça um plano em etapas e aponte riscos

Isso combina bem com a ideia de **Plan** e com agentes para tarefas multi-arquivo. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices), [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)

---

## D. Trabalhe por iteração curta

Em vez de pedir uma mega mudança de uma vez, divida assim:

1. **Explique** o projeto
2. **Planeje** a mudança
3. **Implemente** uma parte
4. **Revise**
5. **Teste**

O VS Code também permite manter **múltiplas sessões** de chat em paralelo, o que ajuda a separar assuntos sem perder contexto. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)

---

# 2) Configurações que mais valem a pena

## A. Crie instruções do projeto

O VS Code tem suporte oficial para **custom instructions**, que aplicam regras automaticamente às conversas do chat. O melhor ponto de partida é um arquivo **`.github/copilot-instructions.md`**, que vale para todo o workspace. Para regras por linguagem/pasta, use arquivos **`.instructions.md`**. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/custom-instructions), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices)

### Comandos úteis para começar

- **`/init`** → gera uma configuração inicial de instruções do projeto. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/overview)
- **`/instructions`** → ajuda a criar instruções mais específicas. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices)
- **`Chat: Open Customizations`** → abre o editor de customizações do agente no VS Code. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

### O que colocar nesse arquivo

A documentação recomenda manter as instruções **curtas**, focadas no que a IA **não consegue inferir só lendo o código**, como padrões não óbvios, decisões arquiteturais e setup do ambiente. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

### Exemplo pronto para o seu projeto

Você pode criar o arquivo:

**`.github/copilot-instructions.md`**

com algo assim:

# Instruções do projeto

## Contexto
Este projeto é um sistema de controle/logística com backend Flask, frontend estático e banco SQLite.

## Regras gerais
- Responder e gerar código em português-BR quando fizer sentido.
- Preservar rotas já existentes no backend.
- Preferir funções curtas e separação de responsabilidades.
- Sempre que sugerir refatoração, explicar impacto antes de alterar.
- Não duplicar lógica de acesso ao banco.
- Manter nomes claros para operações logísticas, expedição, conferência e relatórios.

## Backend
- Usar Flask de forma simples e legível.
- Separar rotas, serviços e acesso ao banco quando possível.
- Validar dados de entrada.
- Tratar erros com mensagens claras.

## Frontend
- Manter HTML legível e organizado.
- Evitar JS desnecessariamente complexo.
- Preservar compatibilidade com telas operacionais simples.

## Banco
- Preservar compatibilidade com SQLite existente.
- Sempre explicar migrações antes de alterar estrutura.

Se você quiser, eu posso transformar isso num arquivo **mais profissional e ajustado ao seu projeto atual**.

---

## B. Use prompt files para tarefas repetidas

O GitHub Copilot também suporta **prompt files** (`*.prompt.md`) no VS Code para fluxos reutilizáveis, como gerar README, fazer code review, documentar API e criar testes. A própria documentação lista esses exemplos e informa que o recurso está em **preview**. [[docs.github.com]](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files), [[docs.github.com]](https://docs.github.com/en/copilot/concepts/prompting/response-customization?tool=visualstudio)

### Exemplo de prompt reutilizável

Arquivo: `.github/prompts/revisar-backend.prompt.md`

Revise o backend Flask atual considerando:
- organização de rotas
- segurança básica
- validação de dados
- separação entre regra de negócio e acesso ao banco
- clareza para manutenção

Devolva:
1. problemas encontrados
2. prioridade
3. correções sugeridas
4. exemplos de código

Depois você usa isso como um prompt padrão em vez de reescrever tudo toda vez. [[docs.github.com]](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files), [[docs.github.com]](https://docs.github.com/en/copilot/concepts/prompting/response-customization?tool=visualstudio)

---

# 3) Comandos e recursos mais úteis do chat

## Comandos “slash” e contexto

No chat do VS Code, digitar **`/`** mostra os slash commands disponíveis. Já o **`#`** serve para adicionar contexto como arquivos, símbolos e outras referências do projeto. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview)

## Comandos/configurações que valem decorar

- **`/init`** → gera instruções iniciais do projeto. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/overview)
- **`/instructions`** → ajuda a criar instruções específicas. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices)
- **`/create-agent <descrição>`** → cria um agente customizado para um papel específico, como “revisor de segurança” ou “especialista em testes”. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/overview)
- **`/create-skill <descrição>`** → cria uma skill reutilizável para um fluxo específico. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/overview)
- **`/create-instruction`**, **`/create-prompt`**, **`/create-hook`** → ajudam a gerar arquivos de personalização com IA. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/overview)

---

# 4) Prompts prontos que funcionam muito bem

## Para entender o projeto

explique a arquitetura atual do projeto e identifique os pontos de acoplamento entre frontend, backend e banco

## Para refatorar com cuidado

faça um plano de refatoração do server.py em módulos menores sem quebrar as rotas existentes

## Para testes

gere testes para as rotas principais do Flask e explique como rodar

## Para banco

analise o uso do SQLite neste projeto e proponha melhorias sem alterar o schema atual

## Para documentação

gere um README técnico com instalação, estrutura de pastas, fluxo da aplicação e endpoints

## Para revisão

revise este arquivo e destaque bugs, riscos de manutenção e melhorias rápidas

---

# 5) Como usar o Gemini no VS Code

Agora indo para sua outra pergunta.

## A. Como abrir o Gemini

A documentação oficial da Google informa que, depois de instalada a extensão oficial **Gemini Code Assist**, o Gemini aparece na **activity bar** do VS Code com o ícone do Gemini; depois, é só clicar nele e fazer login com a conta Google no painel **Gemini Code Assist: Chat**. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/use-gemini-code-assist-chat)

### Passo a passo

1. Abra **Extensions** e confirme que a extensão é a oficial da Google: **Gemini Code Assist** / publisher **Google**. [[marketplac...studio.com]](https://marketplace.visualstudio.com/items?itemName=Google.geminicodeassist), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini)
2. Na activity bar, clique no ícone do **Gemini Code Assist**. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/use-gemini-code-assist-chat)
3. No painel do Gemini, clique em **Login to Google** e conclua o login no navegador. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini)
4. Depois disso, você pode digitar prompts diretamente no chat. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/use-gemini-code-assist-chat), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini)

Se o ícone não estiver visível, normalmente vale procurar por**“Gemini Code Assist”** nas extensões e garantir que está instalado/habilitado. A fonte oficial diz que, após instalar, o Gemini deve aparecer na activity bar. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini)

---

## B. O que o Gemini faz no VS Code

Segundo a documentação oficial, o Gemini Code Assist ajuda com:

- **chat sobre código**, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/use-gemini-code-assist-chat)
- **geração de código**, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/write-code-gemini)
- **compleções inline enquanto você digita**, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/write-code-gemini)
- **transformação de código e smart actions**, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/write-code-gemini)
- e a extensão do marketplace destaca que ele também fornece **citações de documentação e samples** nas respostas. [[marketplac...studio.com]](https://marketplace.visualstudio.com/items?itemName=Google.geminicodeassist)

---

## C. Como usar o chat do Gemini

Você pode usar o Gemini para:

- explicar o arquivo atual, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini)
- explicar só um trecho selecionado, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini)
- criar múltiplos chats separados por contexto, com limite de 20 conversas antes de apagar a mais antiga, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini)
- ver histórico de consultas pelo **Query History**, [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/use-gemini-code-assist-chat)
- e limpar conversas antigas quando o contexto já não fizer mais sentido. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/use-gemini-code-assist-chat), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini)

### Prompts bons para o Gemini

explique este arquivo

gere uma função para validar dados de entrada desta rota Flask

refatore este trecho mantendo o mesmo comportamento

crie testes unitários para este módulo

---

## D. Atalhos úteis do Gemini

A documentação oficial da Google lista estes atalhos no VS Code:

- **Alt+G** → navegar para a interface de chat do Gemini, [[docs.cloud...google.com]](https://docs.cloud.google.com/gemini/docs/codeassist/keyboard-shortcuts), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/keyboard-shortcuts?hl=pt-br)
- **Ctrl+Alt+X** → adicionar o trecho de código selecionado ao contexto do chat, [[docs.cloud...google.com]](https://docs.cloud.google.com/gemini/docs/codeassist/keyboard-shortcuts), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/keyboard-shortcuts?hl=pt-br)
- **Alt+F** → concluir as mudanças de código em um arquivo, [[docs.cloud...google.com]](https://docs.cloud.google.com/gemini/docs/codeassist/keyboard-shortcuts), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/keyboard-shortcuts?hl=pt-br)
- **Alt+O** → gerar um outline/contorno. [[docs.cloud...google.com]](https://docs.cloud.google.com/gemini/docs/codeassist/keyboard-shortcuts), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/keyboard-shortcuts?hl=pt-br)

Se você quiser mudar esses atalhos, a própria Google orienta: **Settings > Keyboard Shortcuts** e editar a keybinding do comando desejado. [[docs.cloud...google.com]](https://docs.cloud.google.com/gemini/docs/codeassist/keyboard-shortcuts), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/keyboard-shortcuts?hl=pt-br)

---

## E. Importante: Copilot e Gemini juntos podem conflitar

A documentação do Gemini alerta que o comportamento de geração, compleções e transformações pode ser **não determinístico** quando ele é usado ao mesmo tempo com outros plugins que usam os **mesmos atalhos** ou a **mesma API da plataforma** para esse tipo de ação. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/write-code-gemini), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/chat-gemini)

### Minha recomendação prática

Para evitar confusão:

- deixe **um assistente como principal para sugestões inline**,
- e use o outro mais para **chat/análise/refatoração guiada**.

Exemplo de divisão boa:

- **Copilot** → entender projeto, refatorar com contexto do workspace, tarefas multi-arquivo
- **Gemini** → explicações rápidas, código assistido, segunda opinião, outline e chat alternativo

Se quiser, eu também posso te sugerir uma configuração “sem conflito” de atalhos.

---

# 6) Atenção importante sobre o Gemini hoje

Há um aviso oficial da Google dizendo que **Gemini Code Assist IDE Extensions e Gemini CLI para os tiers “individuals”, “Google AI Pro” e “Google AI Ultra” deixam de servir requisições a partir de 18 de junho de 2026**, com recomendação de migração para **Antigravity / Antigravity CLI**. Como hoje é **17 de junho de 2026**, isso é algo para você verificar **agora**, principalmente se você estiver usando a versão individual/grátis. [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/write-code-gemini), [[developers...google.com]](https://developers.google.com/gemini-code-assist/resources/release-notes)

Em paralelo, as notas de release da Google indicam que o Gemini Code Assist no VS Code estava na versão **2.86.0** com correções em **15 de junho de 2026**, e que o **Gemini 3.5 Flash** ficou disponível para agent mode, chat e code generation em **8 de junho de 2026**. [[developers...google.com]](https://developers.google.com/gemini-code-assist/resources/release-notes)

---

# 7) Meu conselho final para você

Se eu estivesse configurando seu VS Code hoje, faria assim:

## Configuração simples e forte

1. **Usar o Copilot Chat como chat principal do projeto**. [[code.visua...studio.com]](https://code.visualstudio.com/docs/chat/chat-overview), [[code.visua...studio.com]](https://code.visualstudio.com/docs/agents/best-practices)
2. Criar um **`.github/copilot-instructions.md`** com as regras do seu sistema. [[code.visua...studio.com]](https://code.visualstudio.com/docs/agent-customization/custom-instructions), [[code.visua...studio.com]](https://code.visualstudio.com/blogs/2025/03/26/custom-instructions)
3. Criar 2 ou 3 **prompt files** para tarefas repetidas. [[docs.github.com]](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files)
4. Instalar o **Gemini Code Assist** e usar como alternativa/segunda opinião. [[marketplac...studio.com]](https://marketplace.visualstudio.com/items?itemName=Google.geminicodeassist), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/set-up-gemini)
5. Remapear atalhos se houver conflito. [[docs.cloud...google.com]](https://docs.cloud.google.com/gemini/docs/codeassist/keyboard-shortcuts), [[developers...google.com]](https://developers.google.com/gemini-code-assist/docs/write-code-gemini)

---

Se você quiser, eu posso fazer o próximo passo por você aqui mesmo:

### Opção A — eu monto seu arquivo de instruções

Eu posso te entregar agora um **`.github/copilot-instructions.md` pronto** para esse projeto Flask + frontend + SQLite.

### Opção B — eu monto seus prompts reutilizáveis

Posso criar:

- um prompt para **revisar backend**,
- um para **gerar testes**,
- um para **documentar rotas**,
- e um para **analisar banco SQLite**.

### Opção C — eu te organizo Copilot + Gemini sem conflito

Posso te passar uma configuração prática de:

- **quem usa qual atalho**,
- **quem fica para inline**,
- **quem fica para chat**.
