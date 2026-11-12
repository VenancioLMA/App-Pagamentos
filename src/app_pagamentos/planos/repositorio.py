"""Armazenamento de planos e filtro para encontrar os planos disponíveis."""

from uuid import UUID

from app_pagamentos.comum.repositorio_em_memoria import RepositorioEmMemoria
from app_pagamentos.planos.plano import Plano


class RepositorioPlanos(RepositorioEmMemoria[Plano, UUID]):
    """Guarda planos e permite selecionar somente os que estão ativos."""

    def listar_ativos(self) -> list[Plano]:
        """Devolve os planos que podem ser usados para gerar cobranças."""
        return [plano for plano in self.listar() if plano.ativo]


