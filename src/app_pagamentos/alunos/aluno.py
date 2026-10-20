from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class Aluno:
    nome: str
    email: str
    telefone: str = ""
    ativo: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.nome = self.nome.strip()
        self.email = self.email.strip().lower()
        self.telefone = self.telefone.strip()
        if not self.nome:
            raise ValueError("O nome do aluno é obrigatório.")
        if "@" not in self.email or self.email.startswith("@"):
            raise ValueError("Informe um e-mail válido.")


