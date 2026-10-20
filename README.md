# App-Pagamentos

Um projeto simples para um professor de educação física manter o cadastro dos
alunos e seu próprio perfil. É um começo didático: ainda não processa
pagamentos nem precisa de bibliotecas extras.

## Como abrir no Windows

1. Instale Python 3.10 ou superior em [python.org](https://www.python.org/downloads/).
   Durante a instalação, marque **Add Python to PATH**.
2. Extraia o ZIP do projeto para uma pasta.
3. Abra essa pasta e dê dois cliques em `executar_alunos.bat` ou
   `executar_professores.bat`.

Cada atalho abre um menu próprio no terminal. O de alunos permite cadastrar,
listar e ativar/inativar cadastros. O de professores permite ver, cadastrar e
atualizar o perfil.

Os atalhos procuram Python automaticamente, inclusive em alguns locais comuns
de instalação no Windows. Se aparecer uma mensagem dizendo que Python não foi
encontrado, instale-o pelo endereço acima e abra o atalho novamente.

## Rodar pelo terminal

Se preferir usar o PowerShell, abra a pasta do projeto e execute:

```bash
.\executar_alunos.bat
```

Para abrir o perfil do professor, use `.\executar_professores.bat`.

## Onde ficam os dados

Os cadastros são guardados em arquivos JSON na pasta `data`, criada na primeira
vez que salvar algo. Assim, eles continuam lá ao fechar e abrir o programa.
Esses arquivos ficam só neste computador; faça cópias de segurança e não
compartilhe dados pessoais dos alunos.

O código está em `src/app_pagamentos/`: `alunos/` cuida dos cadastros de alunos,
`professores/` do perfil do professor, `planos/` dos planos e `financeiro/` das
cobranças. Para manter os exemplos iniciais fáceis de entender, os atalhos
abrem apenas os menus de alunos ou professores.
