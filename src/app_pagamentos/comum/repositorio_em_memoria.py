"""Armazenamento temporário reutilizável para diferentes tipos de cadastro."""

from threading import RLock
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class RepositorioEmMemoria(Generic[T, ID]):
    """Guarda objetos durante a execução, mas não os salva em disco.

    T e ID são espaços reservados de tipos: assim, o mesmo repositório pode
    guardar alunos, planos ou cobranças sem perder as verificações de tipos.
    """

    def __init__(self) -> None:
        """Prepara o dicionário de dados e a trava para acesso seguro."""
        self._dados: dict[ID, T] = {}
        self._lock = RLock()

    def obter(self, identificador: ID) -> T | None:
        """Procura um item pelo identificador; retorna None se não existir."""
        with self._lock:
            return self._dados.get(identificador)

    def salvar(self, entidade: T) -> T:
        """Guarda ou substitui um item, usando seu atributo id como chave."""
        identificador = getattr(entidade, "id", None)
        if identificador is None:
            raise ValueError("A entidade precisa ter um atributo 'id'.")
        with self._lock:
            self._dados[identificador] = entidade
        return entidade

    def remover(self, identificador: ID) -> bool:
        """Remove um item e informa se ele realmente estava armazenado."""
        with self._lock:
            return self._dados.pop(identificador, None) is not None

    def listar(self) -> list[T]:
        """Retorna uma lista com os itens guardados até o momento."""
        with self._lock:
            return list(self._dados.values())


