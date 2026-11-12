"""Armazenamento de cobranças com filtros próprios da área financeira."""

from uuid import UUID

from app_pagamentos.comum.repositorio_em_memoria import RepositorioEmMemoria
from app_pagamentos.financeiro.cobranca import Cobranca
from app_pagamentos.financeiro.status_cobranca import StatusCobranca


class RepositorioCobrancas(RepositorioEmMemoria[Cobranca, UUID]):
    """Guarda cobranças e permite consultá-las por aluno ou situação."""

    def listar_por_aluno(self, aluno_id: UUID) -> list[Cobranca]:
        """Retorna todas as cobranças ligadas ao identificador do aluno."""
        return [
            cobranca
            for cobranca in self.listar()
            if cobranca.aluno_id == aluno_id
        ]

    def listar_pendentes(self) -> list[Cobranca]:
        """Retorna cobranças que ainda aguardam pagamento."""
        return [
            cobranca
            for cobranca in self.listar()
            if cobranca.status == StatusCobranca.PENDENTE
        ]


