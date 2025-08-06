#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar questões semelhantes no arquivo Prova_Completa2023.json
e adicionar os tópicos do arquivo questoes_extraidas_completas.json
"""

import json
import re
from difflib import SequenceMatcher
from typing import Dict, List, Any, Tuple

def clean_text(text: str) -> str:
    """
    Limpa o texto removendo caracteres especiais e normalizando espaços
    """
    if not text:
        return ""
    
    # Remove caracteres especiais e normaliza espaços
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calcula a similaridade entre dois textos usando SequenceMatcher
    """
    if not text1 or not text2:
        return 0.0
    
    clean_text1 = clean_text(text1)
    clean_text2 = clean_text(text2)
    
    if not clean_text1 or not clean_text2:
        return 0.0
    
    return SequenceMatcher(None, clean_text1, clean_text2).ratio()

def find_similar_questions(questoes_com_topicos: List[Dict], prova_completa: List[Dict], 
                          similarity_threshold: float = 0.7) -> List[Dict]:
    """
    Encontra questões semelhantes baseado no número e enunciado
    """
    resultado = []
    
    for questao_prova in prova_completa:
        questao_encontrada = None
        melhor_similaridade = 0.0
        
        # Extrai o número da questão da prova
        numero_prova = questao_prova.get('index', 0)
        
        # Extrai o enunciado da questão da prova
        enunciado_prova = ""
        if 'alternativesIntroduction' in questao_prova:
            enunciado_prova = questao_prova['alternativesIntroduction']
        elif 'context' in questao_prova:
            # Se não há alternativesIntroduction, usa o context
            context = questao_prova['context']
            # Remove markdown e imagens
            context = re.sub(r'!\[.*?\]\(.*?\)', '', context)
            context = re.sub(r'\*\*.*?\*\*', '', context)
            context = re.sub(r'\\\[.*?\\\]', '', context)
            enunciado_prova = context.strip()
        
        # Procura por questões semelhantes
        for questao_topicos in questoes_com_topicos:
            numero_topicos = int(questao_topicos.get('numero', 0))
            
            # Primeiro tenta fazer match pelo número
            if numero_prova == numero_topicos:
                questao_encontrada = questao_topicos
                melhor_similaridade = 1.0
                break
            
            # Se não encontrou pelo número, tenta pelo enunciado
            enunciado_topicos = questao_topicos.get('enunciado', '')
            
            # Calcula similaridade entre os enunciados
            similaridade = calculate_similarity(enunciado_prova, enunciado_topicos)
            
            if similaridade > melhor_similaridade and similaridade >= similarity_threshold:
                melhor_similaridade = similaridade
                questao_encontrada = questao_topicos
        
        # Cria a questão resultante
        questao_resultado = questao_prova.copy()
        
        if questao_encontrada:
            questao_resultado['topicos'] = questao_encontrada.get('topicos', [])
            questao_resultado['similarity_score'] = melhor_similaridade
            questao_resultado['matched_question_number'] = questao_encontrada.get('numero')
        else:
            questao_resultado['topicos'] = []
            questao_resultado['similarity_score'] = 0.0
            questao_resultado['matched_question_number'] = None
        
        resultado.append(questao_resultado)
    
    return resultado

def main():
    """
    Função principal do script
    """
    try:
        # Carrega o arquivo com questões e tópicos
        print("Carregando arquivo com questões e tópicos...")
        with open('questoes_extraidas_completas.json', 'r', encoding='utf-8') as f:
            questoes_com_topicos = json.load(f)
        
        # Carrega o arquivo da prova completa
        print("Carregando arquivo da prova completa...")
        with open('Prova_Completa2023.json', 'r', encoding='utf-8') as f:
            prova_completa_data = json.load(f)
        
        # Extrai as questões da prova completa
        questoes_prova = prova_completa_data.get('questions', [])
        
        print(f"Encontradas {len(questoes_com_topicos)} questões com tópicos")
        print(f"Encontradas {len(questoes_prova)} questões na prova completa")
        
        # Encontra questões semelhantes
        print("Procurando questões semelhantes...")
        questoes_com_topicos_merged = find_similar_questions(
            questoes_com_topicos, 
            questoes_prova,
            similarity_threshold=0.6
        )
        
        # Conta quantas questões foram encontradas
        questoes_encontradas = sum(1 for q in questoes_com_topicos_merged if q['topicos'])
        print(f"Encontradas {questoes_encontradas} questões semelhantes")
        
        # Salva o resultado
        output_data = {
            "metadata": {
                "total_questions": len(questoes_com_topicos_merged),
                "questions_with_topics": questoes_encontradas,
                "source_files": [
                    "questoes_extraidas_completas.json",
                    "Prova_Completa2023.json"
                ]
            },
            "questions": questoes_com_topicos_merged
        }
        
        output_filename = 'prova_2023_com_topicos.json'
        print(f"Salvando resultado em {output_filename}...")
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Arquivo {output_filename} criado com sucesso!")
        
        # Mostra algumas estatísticas
        print("\nEstatísticas:")
        print(f"- Total de questões: {len(questoes_com_topicos_merged)}")
        print(f"- Questões com tópicos encontrados: {questoes_encontradas}")
        print(f"- Taxa de sucesso: {(questoes_encontradas/len(questoes_com_topicos_merged)*100):.1f}%")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except json.JSONDecodeError as e:
        print(f"Erro: JSON inválido - {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main() 