"""Representa uma cobrança e controla as mudanças permitidas no seu estado."""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app_pagamentos.financeiro.meio_pagamento import MeioPagamento
from app_pagamentos.financeiro.status_cobranca import StatusCobranca


@dataclass(slots=True)
class Cobranca:
    """Registra quanto um aluno deve, quando vence e se já foi pago."""

    aluno_id: UUID
    professor_id: UUID
    plano_id: UUID
    valor: Decimal
    vencimento: date
    competencia: date
    id: UUID = field(default_factory=uuid4)
    status: StatusCobranca = StatusCobranca.PENDENTE
    meio_pagamento: MeioPagamento | None = None
    paga_em: datetime | None = None

    def __post_init__(self) -> None:
        """Confere regras essenciais para que a cobrança faça sentido."""
        if self.valor <= 0:
            raise ValueError("O valor da cobrança deve ser maior que zero.")
        if self.competencia.day != 1:
            raise ValueError("A competência deve ser informada no primeiro dia do mês.")

    @property
    def em_atraso(self) -> bool:
        """Informa se a cobrança continua pendente depois do vencimento."""
        return self.status == StatusCobranca.PENDENTE and self.vencimento < date.today()

    def registrar_pagamento(self, meio: MeioPagamento) -> None:
        """Marca a cobrança como paga e registra o meio e o horário do pagamento."""
        if self.status != StatusCobranca.PENDENTE:
            raise ValueError("Somente cobranças pendentes podem ser pagas.")
        self.status = StatusCobranca.PAGA
        self.meio_pagamento = meio
        # UTC guarda o horário sem depender do fuso configurado no computador.
        self.paga_em = datetime.now(timezone.utc)

    def cancelar(self) -> None:
        """Cancela uma cobrança pendente; cobranças pagas não podem ser canceladas."""
        if self.status != StatusCobranca.PENDENTE:
            raise ValueError("Somente cobranças pendentes podem ser canceladas.")
        self.status = StatusCobranca.CANCELADA


