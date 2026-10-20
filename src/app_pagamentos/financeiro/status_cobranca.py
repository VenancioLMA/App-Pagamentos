from enum import Enum


class StatusCobranca(str, Enum):
    PENDENTE = "pendente"
    PAGA = "paga"
    CANCELADA = "cancelada"


