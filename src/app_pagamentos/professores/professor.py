"""Define os dados e validações do perfil do professor."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class Professor:
    """Representa o professor responsável pelos cadastros e cobranças."""

    nome: str
    email: str
    # O UUID é um código único criado automaticamente para este perfil.
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """Padroniza nome e e-mail e impede um perfil sem dados essenciais."""
        self.nome = self.nome.strip()
        self.email = self.email.strip().lower()
        if not self.nome:
            raise ValueError("O nome do professor é obrigatório.")
        if "@" not in self.email or self.email.startswith("@"):
            raise ValueError("Informe um e-mail válido.")


