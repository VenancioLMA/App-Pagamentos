"""Apresenta o menu do professor e mantém seu perfil em um arquivo JSON."""

from pathlib import Path
from uuid import UUID

from app_pagamentos.comum.arquivo_json import gravar_lista_json, ler_lista_json
from app_pagamentos.professores.professor import Professor

ARQUIVO_PROFESSOR = Path(__file__).resolve().parents[3] / "data" / "professor.json"


def carregar_professor() -> Professor | None:
    """Lê o perfil salvo; retorna None quando ainda não existe professor."""
    registros = ler_lista_json(ARQUIVO_PROFESSOR)
    if not registros:
        return None
    if len(registros) != 1:
        raise RuntimeError("O cadastro precisa conter somente um professor.")

    registro = registros[0]
    try:
        return Professor(
            id=UUID(registro["id"]),
            nome=registro["nome"],
            email=registro["email"],
        )
    except (KeyError, TypeError, ValueError) as erro:
        raise RuntimeError(f"O cadastro do professor está inválido: {erro}") from erro


def salvar_professor(professor: Professor) -> None:
    """Grava o perfil em uma lista com um único registro no arquivo JSON."""
    gravar_lista_json(
        ARQUIVO_PROFESSOR,
        [{"id": str(professor.id), "nome": professor.nome, "email": professor.email}],
    )


def mostrar_professor(professor: Professor | None) -> None:
    """Exibe os dados do perfil ou informa que ainda não há cadastro."""
    print("\n--- Perfil do professor ---")
    if professor is None:
        print("Ainda não há professor cadastrado.")
        return
    print(f"Nome: {professor.nome}")
    print(f"E-mail: {professor.email}")


def cadastrar_ou_atualizar(professor: Professor | None) -> Professor:
    """Pede os dados e cria um perfil ou atualiza o que já existe."""
    nome = input("Nome do professor: ").strip()
    email = input("E-mail do professor: ").strip()
    try:
        if professor is None:
            professor = Professor(nome=nome, email=email)
        else:
            professor = Professor(id=professor.id, nome=nome, email=email)
    except ValueError as erro:
        print(f"Não foi possível salvar o perfil: {erro}")
        return professor

    salvar_professor(professor)
    print("Perfil salvo.")
    return professor


def executar() -> None:
    """Carrega o perfil e mantém o menu disponível até a opção de saída."""
    try:
        professor = carregar_professor()
        while True:
            print(
                "\n=== Sistema do Professor ==="
                "\n1. Ver perfil"
                "\n2. Cadastrar ou atualizar perfil"
                "\n0. Sair"
            )
            opcao = input("Escolha uma opção: ").strip()

            # A opção escolhida chama a ação correspondente do perfil.
            if opcao == "1":
                mostrar_professor(professor)
            elif opcao == "2":
                professor = cadastrar_ou_atualizar(professor)
            elif opcao == "0":
                print("Até logo!")
                return
            else:
                print("Opção inválida. Escolha 0, 1 ou 2.")
    except RuntimeError as erro:
        print(f"\nErro nos dados do professor: {erro}")
        input("Pressione Enter para fechar.")


if __name__ == "__main__":
    # Evita que o menu seja aberto ao importar este módulo em outro código.
    executar()
