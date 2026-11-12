"""Oferece buscas úteis para os alunos armazenados em memória."""

from uuid import UUID

from app_pagamentos.alunos.aluno import Aluno
from app_pagamentos.comum.repositorio_em_memoria import RepositorioEmMemoria


class RepositorioAlunos(RepositorioEmMemoria[Aluno, UUID]):
    """Guarda alunos e acrescenta formas de busca específicas para eles."""

    def buscar_por_email(self, email: str) -> Aluno | None:
        """Encontra um aluno pelo e-mail, sem diferenciar maiúsculas de minúsculas."""
        email_normalizado = email.strip().lower()
        return next(
            (aluno for aluno in self.listar() if aluno.email == email_normalizado),
            None,
        )

    def listar_ativos(self) -> list[Aluno]:
        """Devolve somente os alunos marcados como ativos."""
        return [aluno for aluno in self.listar() if aluno.ativo]


