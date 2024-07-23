# -------------------- Bibliotecas --------------------


import re
import os
import shutil
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Union


# -------------------- Constantes --------------------


# -------------------- Classes --------------------


class Atividade:
    
    def __init__(self, codigo: str):
        self._codigo = codigo.upper()
        self.criar_diretorios_base()
        self.mover_arquivos_de_exercicios()

    @property
    def atividade_dir(self):
        return f"atividade_{self._codigo.lower()}"
    
    @property
    def codigo(self):
        return self._codigo

    def criar_diretorios_base(self) -> None:
        if not os.path.exists(self.atividade_dir):
            self.to_do_dir = os.path.join(self.atividade_dir, "to_do")
            self.doing_dir = os.path.join(self.atividade_dir, "doing")
            self.done_dir = os.path.join(self.atividade_dir, "done")
            self.relatorio_dir = os.path.join(self.atividade_dir, "relatorio")
            os.mkdir(self.atividade_dir)
            os.mkdir(self.to_do_dir)
            os.mkdir(self.doing_dir)
            os.mkdir(self.done_dir)
            os.mkdir(self.relatorio_dir)

    def mover_arquivos_de_exercicios(self) -> None:
        # Aqui criaria instâncias da classe Exercicio e alimentaria uma lista com os exercícios
        arquivos = os.listdir()
        arquivos_da_atividade = [arquivo for arquivo in arquivos if arquivo.lower().startswith(self.codigo.lower())]
        for arquivo in arquivos_da_atividade:
            nome_arquivo, formato_aquivo = arquivo.split(".")
            exercicio_dir = os.path.join(self.to_do_dir, nome_arquivo.lower())
            if not os.path.exists(exercicio_dir):
                os.mkdir(exercicio_dir)
            # shutil.move(arquivo, os.path.join(exercicio_dir, arquivo.lower())) # Talvez passar no argparse a opção para copiar ou mover
            shutil.copy(arquivo, os.path.join(exercicio_dir, arquivo.lower()))


class Exercicio:
    pass


class Aluno:
    pass


# -------------------- Funções --------------------


def argumentos_do_terminal():
    parser = argparse.ArgumentParser(
        prog="Corretor EQ220",
        description="Script utilizado para corrigir as atividades desenvolvidas na disciplina EQ220 da Faculdade de Engenharia Química (FEQ) da Universidade Estadual de Campinas (UNICAMP).",
    )

    parser.add_argument("code")
    # parser.add_argument("-c", "--copy")

    args = parser.parse_args()

    return args


# -------------------- Função main() --------------------


def main() -> None:

    args = argumentos_do_terminal()

    codigo_atividade = args.code
    atividade_1 = Atividade(codigo_atividade)


if __name__ == "__main__":
    main()