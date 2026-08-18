# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:27:01 2026

@author: carlosnunes
"""
#%% Librarys necessárias 
import importlib.util # 
import subprocess     # serve para executar comandos do sistema operacional tipo CMD
import sys            # conversa diretamente com o interpretador 
#%%
def instalar_pacotes(pacotes, nomes_import=None):
    """
    Instala uma lista de pacotes via pip, pulando os que já estão instalados.

    Parâmetros:
        pacotes (list[str]): lista de nomes de pacotes (como usados no pip),
                              ex: ["pandas", "numpy", "scikit-learn"]
        nomes_import (dict[str, str], opcional): mapeamento pacote -> nome do
            módulo importável, para casos em que o nome do pip difere do nome
            usado no import (ex: {"scikit-learn": "sklearn"}).
    Retorna:
        dict: {"instalados": [...], "ja_existentes": [...], "falhas": [...]}

SINTAXE:
instalar_pacotes(pacotes, nomes_import=None)	

pacotes: lista de nomes de pacotes; nomes_import: dict opcional mapeando nome do pip → nome do módulo importável

    """
   
    nomes_import = nomes_import or {}
    resultado = {"instalados": [], "ja_existentes": [], "falhas": []}

    for pacote in pacotes:
        modulo = nomes_import.get(pacote, pacote.replace("-", "_"))

        if importlib.util.find_spec(modulo) is not None:
            print(f"[OK] '{pacote}' já está instalado.")
            resultado["ja_existentes"].append(pacote)
            continue

        print(f"[...] Instalando '{pacote}'...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pacote],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"[OK] '{pacote}' instalado com sucesso.")
            resultado["instalados"].append(pacote)
        except subprocess.CalledProcessError:
            print(f"[ERRO] Falha ao instalar '{pacote}'.")
            resultado["falhas"].append(pacote)

    return resultado


if __name__ == "__main__":
    pacotes_desejados = ["pandas", "numpy", "scikit-learn", "requests"]
    mapeamento = {"scikit-learn": "sklearn"}

    status = instalar_pacotes(pacotes_desejados, nomes_import=mapeamento)
    print("\nResumo:")
    print(status)