"""Define os dados de um plano mensal e verifica se estão corretos."""

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(slots=True)
class Plano:
    """Representa uma opção de serviço com nome, descrição e preço mensal."""

    nome: str
    valor_mensal: Decimal
    descricao: str = ""
    ativo: bool = True
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """Remove espaços extras e impede nome vazio ou preço não positivo."""
        self.nome = self.nome.strip()
        self.descricao = self.descricao.strip()
        if not self.nome:
            raise ValueError("O nome do plano é obrigatório.")
        if self.valor_mensal <= 0:
            raise ValueError("O valor mensal deve ser maior que zero.")


