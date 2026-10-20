from uuid import UUID

from app_pagamentos.comum.repositorio_em_memoria import RepositorioEmMemoria
from app_pagamentos.planos.plano import Plano


class RepositorioPlanos(RepositorioEmMemoria[Plano, UUID]):
    def listar_ativos(self) -> list[Plano]:
        return [plano for plano in self.listar() if plano.ativo]


