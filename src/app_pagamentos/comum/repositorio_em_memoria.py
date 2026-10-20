from threading import RLock
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class RepositorioEmMemoria(Generic[T, ID]):
    """Armazenamento temporário para desenvolvimento; não persiste entre execuções."""

    def __init__(self) -> None:
        self._dados: dict[ID, T] = {}
        self._lock = RLock()

    def obter(self, identificador: ID) -> T | None:
        with self._lock:
            return self._dados.get(identificador)

    def salvar(self, entidade: T) -> T:
        identificador = getattr(entidade, "id", None)
        if identificador is None:
            raise ValueError("A entidade precisa ter um atributo 'id'.")
        with self._lock:
            self._dados[identificador] = entidade
        return entidade

    def remover(self, identificador: ID) -> bool:
        with self._lock:
            return self._dados.pop(identificador, None) is not None

    def listar(self) -> list[T]:
        with self._lock:
            return list(self._dados.values())


