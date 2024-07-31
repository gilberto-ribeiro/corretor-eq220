# -------------------- Bibliotecas --------------------


import re
import os
import shutil
import subprocess
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Union


# -------------------- Constantes --------------------


# -------------------- Classes --------------------


class Atividade:
    def __init__(self, codigo: str):
        self._codigo: str = codigo.upper()
        self._exercicios: List[Exercicio] = []
        self._alunos: List[Aluno] = []
        self.criar_diretorios_base()
        self.transferir_gabarito()
        self.transferir_exercicios_para_to_do()
        self.obter_resposta_dos_exercicios()

    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def exercicios(self):
        return self._exercicios
    
    @property
    def alunos(self):
        return self._alunos

    @property
    def atividade_dir(self) -> str:
        return f"atividade_{self._codigo.lower()}"

    def criar_diretorios_base(self) -> None:
        if not os.path.exists(self.atividade_dir):
            self._to_do_dir = os.path.join(self.atividade_dir, "to_do")
            self._doing_dir = os.path.join(self.atividade_dir, "doing")
            self._done_dir = os.path.join(self.atividade_dir, "done")
            self._relatorio_dir = os.path.join(self.atividade_dir, "relatorio")
            os.mkdir(self.atividade_dir)
            os.mkdir(self._to_do_dir)
            os.mkdir(self._doing_dir)
            os.mkdir(self._done_dir)
            os.mkdir(self._relatorio_dir)

    def transferir_exercicios_para_to_do(self) -> None:
        arquivos = os.listdir()
        arquivos_de_exercicios = [arquivo for arquivo in arquivos if arquivo.lower().startswith(self._codigo.lower())]
        for arquivo in arquivos_de_exercicios:
            nome_arquivo = arquivo.split(".")[0]
            exercicio_dir = os.path.join(self._to_do_dir, nome_arquivo.lower())
            if not os.path.exists(exercicio_dir):
                os.mkdir(exercicio_dir)
                exercicio = Exercicio(self, exercicio_dir)
                self._exercicios.append(exercicio)
            # shutil.move(arquivo, os.path.join(exercicio_dir, arquivo.lower())) # Talvez passar no argparse a opção para copiar ou mover
            shutil.copy(arquivo, os.path.join(exercicio_dir, arquivo.lower()))

    def transferir_gabarito(self):
        arquivo_gabarito = f"gabarito_{self._codigo.lower()}.py"
        self._gabarito_dir = os.path.join(self.atividade_dir, arquivo_gabarito)
        # shutil.move(arquivo_gabarito, self._gabarito_dir)
        shutil.copy(arquivo_gabarito, self._gabarito_dir)

    def obter_resposta_dos_exercicios(self):
        for exercicio in self._exercicios:
            print("---------------- TESTES -----------------")
            print(exercicio.status_resposta)
            print(exercicio.arquivo_py)
            print(exercicio._diretorio_atual)
            print(exercicio.resposta_str)
            exercicio.mover_exercicio("doing")
            print(exercicio.diretorio_atual)

        
class Exercicio:
    def __init__(self, atividade: Atividade, diretorio_atual: str):
        self._atividade = atividade
        self._diretorio_atual = diretorio_atual
        self._alunos = []
        self._nome = self._diretorio_atual.split("/")[-1]
        self.listar_alunos()

    @property
    def atividade(self) -> Atividade:
        return self._atividade

    @property
    def diretorio_atual(self) -> str:
        return self._diretorio_atual

    @property
    def alunos(self):
        return self._alunos
    
    @property
    def primeiro_ra(self) -> str:
        return self._primeiro_ra

    @property
    def arquivo_py(self) -> str:
        return f"{self._nome}.py"

    @property
    def gabarito_str(self) -> str:
        return subprocess.run(["python3", self._atividade._gabarito_dir, self.arquivo_py], capture_output=True, text=True).stdout.strip()

    @property
    def gabarito(self) -> List[float]:
        return self.converter_resposta(self.gabarito_str)
    
    @property
    def response(self):
        return subprocess.run(["python3", f"{self._diretorio_atual}/{self.arquivo_py}"], capture_output=True, text=True)
    
    @property
    def resposta_str(self) -> str:
        if self.status_resposta:
            return self.response.stdout.strip()
        else:
            return self.response.stderr
    
    @property
    def resposta(self) -> Union[List[float], None]:
        if self.status_resposta:
            return self.converter_resposta(self.resposta_str)
        else:
            return None
        
    @property
    def status_resposta(self) -> bool:
        return True if self.response.stdout.strip() != "" else False

    def listar_alunos(self) -> None:
        ras = [ra for ra in self._nome.split("_")[1:]]
        self._primeiro_ra = ras[0]
        for ra in ras:
            aluno = Aluno(self, ra)
            self._alunos.append(aluno)
        self.atividade._alunos.extend(self._alunos)

    def mover_exercicio(self, diretorio: str) -> None:
        match diretorio:
            case "to_do":
                destino_dir = self._atividade._to_do_dir
            case "doing":
                destino_dir = self._atividade._doing_dir
            case "done":
                destino_dir = self._atividade._done_dir
        shutil.move(self._diretorio_atual, destino_dir)
        self._diretorio_atual = os.path.join(destino_dir, self._nome)

    @staticmethod
    def converter_resposta(respostas: str) -> List[float]:
        return [float(resposta) for resposta in respostas.split("\n")]


class Aluno:
    def __init__(self, exercicio: Exercicio, ra: str):
        self._exercicio: Exercicio = exercicio
        self._ra: str = ra

    @property
    def exercicio(self) -> Exercicio:
        return self._exercicio
    
    @property
    def ra(self) -> str:
        return self._ra

    @property
    def primeiro_ra(self) -> bool:
        return self.ra == self.exercicio.primeiro_ra


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