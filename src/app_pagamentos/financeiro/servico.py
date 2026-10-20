from datetime import date
from decimal import Decimal
from uuid import UUID

from app_pagamentos.alunos.repositorio import RepositorioAlunos
from app_pagamentos.financeiro.cobranca import Cobranca
from app_pagamentos.financeiro.meio_pagamento import MeioPagamento
from app_pagamentos.financeiro.repositorio import RepositorioCobrancas
from app_pagamentos.planos.repositorio import RepositorioPlanos
from app_pagamentos.professores.professor import Professor


class ServicoFinanceiro:
    def __init__(
        self,
        professor: Professor,
        alunos: RepositorioAlunos,
        planos: RepositorioPlanos,
        cobrancas: RepositorioCobrancas,
    ) -> None:
        self._professor = professor
        self._alunos = alunos
        self._planos = planos
        self._cobrancas = cobrancas

    def gerar_cobranca(
        self,
        aluno_id: UUID,
        plano_id: UUID,
        vencimento: date,
        competencia: date,
        valor: Decimal | None = None,
    ) -> Cobranca:
        aluno = self._alunos.obter(aluno_id)
        if aluno is None or not aluno.ativo:
            raise LookupError("Aluno não encontrado ou inativo.")
        plano = self._planos.obter(plano_id)
        if plano is None or not plano.ativo:
            raise LookupError("Plano não encontrado ou inativo.")
        if valor is not None and valor <= 0:
            raise ValueError("O valor da cobrança deve ser maior que zero.")
        cobranca = Cobranca(
            aluno_id=aluno.id,
            professor_id=self._professor.id,
            plano_id=plano.id,
            valor=valor if valor is not None else plano.valor_mensal,
            vencimento=vencimento,
            competencia=competencia,
        )
        return self._cobrancas.salvar(cobranca)

    def confirmar_pagamento(
        self, cobranca_id: UUID, meio: MeioPagamento
    ) -> Cobranca:
        cobranca = self._cobrancas.obter(cobranca_id)
        if cobranca is None:
            raise LookupError("Cobrança não encontrada.")
        cobranca.registrar_pagamento(meio)
        return self._cobrancas.salvar(cobranca)

    def cancelar_cobranca(self, cobranca_id: UUID) -> Cobranca:
        cobranca = self._cobrancas.obter(cobranca_id)
        if cobranca is None:
            raise LookupError("Cobrança não encontrada.")
        cobranca.cancelar()
        return self._cobrancas.salvar(cobranca)
