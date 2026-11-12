"""Define as situações possíveis para uma cobrança."""

from enum import Enum


class StatusCobranca(str, Enum):
    """Uma cobrança começa pendente e pode ser paga ou cancelada."""

    PENDENTE = "pendente"
    PAGA = "paga"
    CANCELADA = "cancelada"


