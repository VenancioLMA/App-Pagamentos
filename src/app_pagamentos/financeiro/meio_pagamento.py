from enum import Enum


class MeioPagamento(str, Enum):
    PIX = "pix"
    DINHEIRO = "dinheiro"
    CARTAO = "cartao"
    TRANSFERENCIA = "transferencia"
    OUTRO = "outro"


