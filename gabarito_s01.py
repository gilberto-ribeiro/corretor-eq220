# -------------------- Bibliotecas --------------------


import os
import argparse
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -------------------- Funções --------------------


def extrair_primeiro_ra():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    nome_do_arquivo = args.filename
    exercicio, formato = nome_do_arquivo.split(".")
    primeiro_ra = exercicio.split("_")[1]
    digitos_ra = [float(digito) for digito in primeiro_ra]
    return digitos_ra


# -------------------- Função main() --------------------


def main() -> None:

    a, b, c = extrair_primeiro_ra()[3:6]

    # print(f"a = {a}")
    # print(f"b = {b}")
    # print(f"c = {c}")

    print(b**2)
    print(a*b)
    print(a+c-2)


if __name__ == "__main__":
    main()