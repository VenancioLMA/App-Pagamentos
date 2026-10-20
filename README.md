# App-Pagamentos

Aplicativo para um professor de educação física acompanhar alunos, planos e
mensalidades, inspirado no fluxo de gestão do MFIT Personal. O escopo inicial
é financeiro: não inclui loja, carrinho, estoque, treinos nem integração para
processar pagamentos.

## Estrutura

```text
src/app_pagamentos/
  alunos/          cadastro e consulta de alunos
  professores/     perfil do professor responsável
  planos/          planos e valores mensais
  financeiro/      cobranças, pagamentos e situação financeira
  comum/           repositório em memória para desenvolvimento
```

As cobranças podem ser geradas a partir do valor de um plano, consultadas por
aluno e marcadas como pagas após o recebimento. A confirmação registra o meio
de pagamento informado; ela não movimenta dinheiro nem chama um provedor
externo.

Os repositórios são temporários e mantêm os dados somente na memória do
processo. Persistência em banco de dados, autenticação, interface e integração
com Pix/cartão ficam para etapas posteriores.

## Instalação local

Requer Python 3.10 ou superior:

```bash
python -m pip install -e .
```

Os pacotes usam namespace packages e não precisam de arquivos `__init__.py`.
