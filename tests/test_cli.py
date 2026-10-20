import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app_pagamentos.alunos import cli as alunos_cli
from app_pagamentos.professores import cli as professores_cli


class CliTests(unittest.TestCase):
    def test_cadastro_de_aluno_fica_salvo_apos_reabrir(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "alunos.json"
            with patch.object(alunos_cli, "ARQUIVO_ALUNOS", arquivo):
                repositorio = alunos_cli.carregar_alunos()
                with patch("builtins.input", side_effect=["Joana Lima", "joana@example.com", ""]):
                    alunos_cli.cadastrar_aluno(repositorio)

                recarregado = alunos_cli.carregar_alunos()

            self.assertEqual(len(recarregado.listar()), 1)
            self.assertEqual(recarregado.listar()[0].nome, "Joana Lima")

    def test_perfil_de_professor_fica_salvo_apos_reabrir(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "professor.json"
            with patch.object(professores_cli, "ARQUIVO_PROFESSOR", arquivo):
                with patch(
                    "builtins.input",
                    side_effect=["Carlos Souza", "carlos@example.com"],
                ):
                    professor = professores_cli.cadastrar_ou_atualizar(None)

                recarregado = professores_cli.carregar_professor()

            self.assertIsNotNone(recarregado)
            self.assertEqual(recarregado.id, professor.id)
            self.assertEqual(recarregado.nome, "Carlos Souza")

    def test_indice_zero_nao_altera_o_ultimo_aluno(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "alunos.json"
            with patch.object(alunos_cli, "ARQUIVO_ALUNOS", arquivo):
                repositorio = alunos_cli.carregar_alunos()
                with patch(
                    "builtins.input",
                    side_effect=["Joana Lima", "joana@example.com", ""],
                ):
                    alunos_cli.cadastrar_aluno(repositorio)

                with patch("builtins.input", return_value="0"):
                    alunos_cli.alterar_situacao(repositorio)

            self.assertTrue(repositorio.listar()[0].ativo)


if __name__ == "__main__":
    unittest.main()
