from uuid import UUID

from app_pagamentos.comum.repositorio_em_memoria import RepositorioEmMemoria
from app_pagamentos.financeiro.cobranca import Cobranca
from app_pagamentos.financeiro.status_cobranca import StatusCobranca


class RepositorioCobrancas(RepositorioEmMemoria[Cobranca, UUID]):
    def listar_por_aluno(self, aluno_id: UUID) -> list[Cobranca]:
        return [
            cobranca
            for cobranca in self.listar()
            if cobranca.aluno_id == aluno_id
        ]

    def listar_pendentes(self) -> list[Cobranca]:
        return [
            cobranca
            for cobranca in self.listar()
            if cobranca.status == StatusCobranca.PENDENTE
        ]


