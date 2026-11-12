"""Lista os meios de pagamento que podem ser associados a uma cobrança."""

from enum import Enum


class MeioPagamento(str, Enum):
    """Opções de pagamento aceitas pelo sistema."""

    PIX = "pix"
    DINHEIRO = "dinheiro"
    CARTAO = "cartao"
    TRANSFERENCIA = "transferencia"
    OUTRO = "outro"


