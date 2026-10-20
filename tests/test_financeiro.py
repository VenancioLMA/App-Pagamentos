import unittest
from datetime import date
from decimal import Decimal

from app_pagamentos.alunos.aluno import Aluno
from app_pagamentos.alunos.repositorio import RepositorioAlunos
from app_pagamentos.financeiro.meio_pagamento import MeioPagamento
from app_pagamentos.financeiro.repositorio import RepositorioCobrancas
from app_pagamentos.financeiro.servico import ServicoFinanceiro
from app_pagamentos.financeiro.status_cobranca import StatusCobranca
from app_pagamentos.planos.plano import Plano
from app_pagamentos.planos.repositorio import RepositorioPlanos
from app_pagamentos.professores.professor import Professor


class ServicoFinanceiroTests(unittest.TestCase):
    def setUp(self) -> None:
        self.alunos = RepositorioAlunos()
        self.planos = RepositorioPlanos()
        self.cobrancas = RepositorioCobrancas()
        self.professor = Professor("Professora Ana", "ana@example.com")
        self.aluno = self.alunos.salvar(Aluno("João Silva", "joao@example.com"))
        self.plano = self.planos.salvar(
            Plano("Mensal", Decimal("150.00"))
        )
        self.servico = ServicoFinanceiro(
            self.professor, self.alunos, self.planos, self.cobrancas
        )

    def test_gera_cobranca_com_valor_do_plano_e_registra_pagamento(self) -> None:
        cobranca = self.servico.gerar_cobranca(
            self.aluno.id,
            self.plano.id,
            date(2026, 11, 10),
            date(2026, 11, 1),
        )

        self.assertEqual(cobranca.valor, Decimal("150.00"))
        self.assertEqual(cobranca.status, StatusCobranca.PENDENTE)

        paga = self.servico.confirmar_pagamento(cobranca.id, MeioPagamento.PIX)

        self.assertEqual(paga.status, StatusCobranca.PAGA)
        self.assertEqual(paga.meio_pagamento, MeioPagamento.PIX)
        self.assertIsNotNone(paga.paga_em)

    def test_nao_gera_cobranca_para_aluno_inativo(self) -> None:
        self.aluno.ativo = False

        with self.assertRaises(LookupError):
            self.servico.gerar_cobranca(
                self.aluno.id,
                self.plano.id,
                date(2026, 11, 10),
                date(2026, 11, 1),
            )

    def test_nao_permite_confirmar_pagamento_mais_de_uma_vez(self) -> None:
        cobranca = self.servico.gerar_cobranca(
            self.aluno.id,
            self.plano.id,
            date(2026, 11, 10),
            date(2026, 11, 1),
        )
        self.servico.confirmar_pagamento(cobranca.id, MeioPagamento.PIX)

        with self.assertRaises(ValueError):
            self.servico.confirmar_pagamento(cobranca.id, MeioPagamento.CARTAO)


if __name__ == "__main__":
    unittest.main()
