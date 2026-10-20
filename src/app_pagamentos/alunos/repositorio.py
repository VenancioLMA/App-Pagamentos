from uuid import UUID

from app_pagamentos.alunos.aluno import Aluno
from app_pagamentos.comum.repositorio_em_memoria import RepositorioEmMemoria


class RepositorioAlunos(RepositorioEmMemoria[Aluno, UUID]):
    def buscar_por_email(self, email: str) -> Aluno | None:
        email_normalizado = email.strip().lower()
        return next(
            (aluno for aluno in self.listar() if aluno.email == email_normalizado),
            None,
        )

    def listar_ativos(self) -> list[Aluno]:
        return [aluno for aluno in self.listar() if aluno.ativo]


