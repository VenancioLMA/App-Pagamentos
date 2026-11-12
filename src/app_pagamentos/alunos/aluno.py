"""Define os dados e as regras básicas de validação de um aluno."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class Aluno:
    """Representa uma pessoa cadastrada para acompanhar suas mensalidades."""

    nome: str
    email: str
    telefone: str = ""
    ativo: bool = True
    # O identificador é criado automaticamente e distingue alunos com o mesmo nome.
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """Padroniza os textos e impede que o cadastro fique sem dados essenciais."""
        self.nome = self.nome.strip()
        self.email = self.email.strip().lower()
        self.telefone = self.telefone.strip()
        if not self.nome:
            raise ValueError("O nome do aluno é obrigatório.")
        if "@" not in self.email or self.email.startswith("@"):
            raise ValueError("Informe um e-mail válido.")


