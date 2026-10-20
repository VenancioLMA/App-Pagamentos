from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app_pagamentos.financeiro.meio_pagamento import MeioPagamento
from app_pagamentos.financeiro.status_cobranca import StatusCobranca


@dataclass(slots=True)
class Cobranca:
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
        if self.valor <= 0:
            raise ValueError("O valor da cobrança deve ser maior que zero.")
        if self.competencia.day != 1:
            raise ValueError("A competência deve ser informada no primeiro dia do mês.")

    @property
    def em_atraso(self) -> bool:
        return self.status == StatusCobranca.PENDENTE and self.vencimento < date.today()

    def registrar_pagamento(self, meio: MeioPagamento) -> None:
        if self.status != StatusCobranca.PENDENTE:
            raise ValueError("Somente cobranças pendentes podem ser pagas.")
        self.status = StatusCobranca.PAGA
        self.meio_pagamento = meio
        self.paga_em = datetime.now(timezone.utc)

    def cancelar(self) -> None:
        if self.status != StatusCobranca.PENDENTE:
            raise ValueError("Somente cobranças pendentes podem ser canceladas.")
        self.status = StatusCobranca.CANCELADA


