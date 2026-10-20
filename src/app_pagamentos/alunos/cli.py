from pathlib import Path
from uuid import UUID

from app_pagamentos.alunos.aluno import Aluno
from app_pagamentos.alunos.repositorio import RepositorioAlunos
from app_pagamentos.comum.arquivo_json import gravar_lista_json, ler_lista_json

ARQUIVO_ALUNOS = Path(__file__).resolve().parents[3] / "data" / "alunos.json"


def carregar_alunos() -> RepositorioAlunos:
    repositorio = RepositorioAlunos()
    for registro in ler_lista_json(ARQUIVO_ALUNOS):
        try:
            aluno = Aluno(
                id=UUID(registro["id"]),
                nome=registro["nome"],
                email=registro["email"],
                telefone=registro.get("telefone", ""),
                ativo=registro.get("ativo", True),
            )
        except (KeyError, TypeError, ValueError) as erro:
            raise RuntimeError(f"Há um cadastro de aluno inválido: {erro}") from erro
        repositorio.salvar(aluno)
    return repositorio


def salvar_alunos(repositorio: RepositorioAlunos) -> None:
    registros = [
        {
            "id": str(aluno.id),
            "nome": aluno.nome,
            "email": aluno.email,
            "telefone": aluno.telefone,
            "ativo": aluno.ativo,
        }
        for aluno in repositorio.listar()
    ]
    gravar_lista_json(ARQUIVO_ALUNOS, registros)


def listar_alunos(repositorio: RepositorioAlunos) -> None:
    alunos = repositorio.listar()
    if not alunos:
        print("\nAinda não há alunos cadastrados.")
        return

    print("\n--- Alunos cadastrados ---")
    for indice, aluno in enumerate(alunos, start=1):
        situacao = "Ativo" if aluno.ativo else "Inativo"
        telefone = aluno.telefone or "não informado"
        print(f"{indice}. {aluno.nome} | {aluno.email} | {telefone} | {situacao}")


def cadastrar_aluno(repositorio: RepositorioAlunos) -> None:
    nome = input("Nome do aluno: ").strip()
    email = input("E-mail do aluno: ").strip()
    telefone = input("Telefone (opcional): ").strip()

    if repositorio.buscar_por_email(email):
        print("Já existe um aluno cadastrado com esse e-mail.")
        return

    try:
        aluno = repositorio.salvar(
            Aluno(nome=nome, email=email, telefone=telefone)
        )
    except ValueError as erro:
        print(f"Não foi possível cadastrar: {erro}")
        return
    salvar_alunos(repositorio)
    print(f"Aluno {aluno.nome} cadastrado e salvo.")


def alterar_situacao(repositorio: RepositorioAlunos) -> None:
    listar_alunos(repositorio)
    alunos = repositorio.listar()
    if not alunos:
        return

    try:
        indice = int(input("Número do aluno para ativar/inativar: ")) - 1
    except ValueError:
        print("Número inválido. Escolha um aluno da lista.")
        return

    if not 0 <= indice < len(alunos):
        print("Número inválido. Escolha um aluno da lista.")
        return

    aluno = alunos[indice]
    aluno.ativo = not aluno.ativo
    salvar_alunos(repositorio)
    situacao = "ativo" if aluno.ativo else "inativo"
    print(f"{aluno.nome} agora está {situacao}.")


def executar() -> None:
    try:
        repositorio = carregar_alunos()
        while True:
            print(
                "\n=== Sistema de Alunos ==="
                "\n1. Listar alunos"
                "\n2. Cadastrar aluno"
                "\n3. Ativar ou inativar aluno"
                "\n0. Sair"
            )
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                listar_alunos(repositorio)
            elif opcao == "2":
                cadastrar_aluno(repositorio)
            elif opcao == "3":
                alterar_situacao(repositorio)
            elif opcao == "0":
                print("Até logo!")
                return
            else:
                print("Opção inválida. Escolha 0, 1, 2 ou 3.")
    except RuntimeError as erro:
        print(f"\nErro nos dados dos alunos: {erro}")
        input("Pressione Enter para fechar.")


if __name__ == "__main__":
    executar()
