from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(slots=True)
class Plano:
    nome: str
    valor_mensal: Decimal
    descricao: str = ""
    ativo: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.nome = self.nome.strip()
        self.descricao = self.descricao.strip()
        if not self.nome:
            raise ValueError("O nome do plano é obrigatório.")
        if self.valor_mensal <= 0:
            raise ValueError("O valor mensal deve ser maior que zero.")


