# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 22:33:40 2026

@author: carlo
"""
from instalar_pacotes import instalar_pacotes

pacotes = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "openpyxl"
]

nomes_import = {
    "scikit-learn": "sklearn"
}

instalar_pacotes(pacotes, nomes_import)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import os


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 1. Carregar o dataset gerado
df = pd.read_excel(BASE_DIR / "triagem_em_ubs.xlsx")


# 2. Separar variáveis preditoras (X) e alvo (y)
X = df[['febre', 'tosse', 'dor_corpo', 'fadiga']]
y = df['gripe_resfriado']

# 3. Codificar atributos categóricos em valores inteiros para o CategoricalNB
# Ordinal Encoder: Converte categorias textuais em números inteiros sequenciais (ex: de 0 a n-1).

encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)

# 4. Divisão em dados de treino (75%) e teste (25%) com estratificação
# 42 é o Seed
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.25, random_state=42, stratify=y
)

# 5. Treinio do modelo Instanciar e treinar o classificador Naïve Bayes Categórico 
model = CategoricalNB()
model.fit(X_train, y_train)

# 6. Predição nos dados de teste
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1] # Probabilidade da classe positiva (Gripe)

# 7. Exibir relatório de classificação no console
print("--- RELATÓRIO DE CLASSIFICAÇÃO ---")
print(classification_report(y_test, y_pred, target_names=['Resfriado/Outro (0)', 'Gripe (1)']))

# 8. Visualização dos Resultados (Matriz de Confusão + Curva ROC)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Matriz de Confusão
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Resfriado/Outro (0)', 'Gripe (1)'],
            yticklabels=['Resfriado/Outro (0)', 'Gripe (1)'])
axes[0].set_title('Matriz de Confusão — Naïve Bayes', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Classe Predita')
axes[0].set_ylabel('Classe Real')

# Plot 2: Curva ROC
fpr, tpr, _ = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)

axes[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'Curva ROC (AUC = {roc_auc:.2f})')
axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
axes[1].set_xlim([0.0, 1.0])
axes[1].set_ylim([0.0, 1.05])
axes[1].set_xlabel('Taxa de Falsos Positivos (FPR)')
axes[1].set_ylabel('Taxa de Verdadeiros Positivos (TPR)')
axes[1].set_title('Curva ROC — Diagnóstico de Gripe', fontsize=12, fontweight='bold')
axes[1].legend(loc="lower right")
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()

# usar o modelo
df2 = pd.read_excel(BASE_DIR / "novos_pacientes_para_predicao.xlsx")
x2 = df2[['febre', 'tosse', 'dor_corpo', 'fadiga']]
x2_encoded = encoder.transform(x2)
y2_pred = model.predict(x2_encoded)
