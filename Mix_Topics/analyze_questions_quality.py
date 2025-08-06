#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar a qualidade das questões, encontrar duplicatas
e questões que não se assemelham ao enunciado original
"""

import json
import re
from difflib import SequenceMatcher
from typing import Dict, List, Set, Any, Tuple

def load_json_file(filename: str) -> Any:
    """
    Carrega um arquivo JSON
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {filename} não encontrado")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro: JSON inválido em {filename} - {e}")
        return None

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

def find_duplicate_questions(questoes_prova: List[Dict]) -> List[Tuple[int, int]]:
    """
    Encontra questões duplicadas baseado no índice
    """
    indices = {}
    duplicatas = []
    
    for i, questao in enumerate(questoes_prova):
        index = questao.get('index', 0)
        if index in indices:
            duplicatas.append((indices[index], i))
        else:
            indices[index] = i
    
    return duplicatas

def find_low_similarity_questions(questoes_com_topicos: List[Dict], 
                                questoes_prova: List[Dict], 
                                similarity_threshold: float = 0.3) -> List[Dict]:
    """
    Encontra questões que têm baixa similaridade com o enunciado original
    """
    questoes_baixa_similaridade = []
    
    for questao_prova in questoes_prova:
        index_prova = questao_prova.get('index', 0)
        melhor_similaridade = 0.0
        questao_original = None
        
        # Extrai o enunciado da questão da prova
        enunciado_prova = ""
        if 'alternativesIntroduction' in questao_prova:
            enunciado_prova = questao_prova['alternativesIntroduction']
        elif 'context' in questao_prova:
            context = questao_prova['context']
            context = re.sub(r'!\[.*?\]\(.*?\)', '', context)
            context = re.sub(r'\*\*.*?\*\*', '', context)
            context = re.sub(r'\\\[.*?\\\]', '', context)
            enunciado_prova = context.strip()
        
        # Procura pela questão original correspondente
        for questao_original_data in questoes_com_topicos:
            numero_original = int(questao_original_data.get('numero', 0))
            
            # Primeiro tenta fazer match pelo número
            if index_prova == numero_original:
                questao_original = questao_original_data
                melhor_similaridade = 1.0
                break
            
            # Se não encontrou pelo número, tenta pelo enunciado
            enunciado_original = questao_original_data.get('enunciado', '')
            similaridade = calculate_similarity(enunciado_prova, enunciado_original)
            
            if similaridade > melhor_similaridade:
                melhor_similaridade = similaridade
                questao_original = questao_original_data
        
        # Se a similaridade é baixa, adiciona à lista
        if melhor_similaridade < similarity_threshold:
            questoes_baixa_similaridade.append({
                'questao_prova': questao_prova,
                'similarity_score': melhor_similaridade,
                'questao_original': questao_original
            })
    
    return questoes_baixa_similaridade

def analyze_questions_quality():
    """
    Analisa a qualidade das questões
    """
    print("🔍 Analisando qualidade das questões...")
    
    # Carrega os arquivos
    questoes_com_topicos = load_json_file('questoes_extraidas_completas.json')
    if not questoes_com_topicos:
        return
    
    prova_com_topicos_data = load_json_file('prova_2023_com_topicos.json')
    if not prova_com_topicos_data:
        return
    
    questoes_prova = prova_com_topicos_data.get('questions', [])
    
    print(f"\n📊 Estatísticas:")
    print(f"- Questões com tópicos: {len(questoes_com_topicos)}")
    print(f"- Questões na prova final: {len(questoes_prova)}")
    
    # Encontra duplicatas
    print(f"\n🔍 Procurando questões duplicadas...")
    duplicatas = find_duplicate_questions(questoes_prova)
    
    if duplicatas:
        print(f"❌ Encontradas {len(duplicatas)} questões duplicadas:")
        for i, (idx1, idx2) in enumerate(duplicatas, 1):
            questao1 = questoes_prova[idx1]
            questao2 = questoes_prova[idx2]
            print(f"{i}. Questão {questao1.get('index')} aparece nas posições {idx1} e {idx2}")
    else:
        print("✅ Nenhuma questão duplicada encontrada")
    
    # Encontra questões com baixa similaridade
    print(f"\n🔍 Procurando questões com baixa similaridade...")
    questoes_baixa_similaridade = find_low_similarity_questions(
        questoes_com_topicos, 
        questoes_prova,
        similarity_threshold=0.3
    )
    
    if questoes_baixa_similaridade:
        print(f"⚠️  Encontradas {len(questoes_baixa_similaridade)} questões com baixa similaridade:")
        for i, item in enumerate(questoes_baixa_similaridade, 1):
            questao_prova = item['questao_prova']
            similarity = item['similarity_score']
            questao_original = item['questao_original']
            
            print(f"\n{i}. Questão {questao_prova.get('index')} (similaridade: {similarity:.2f})")
            
            if questao_original:
                print(f"   Original: Questão {questao_original.get('numero')}")
                enunciado_original = questao_original.get('enunciado', '')[:100] + "..."
                print(f"   Enunciado original: {enunciado_original}")
            
            enunciado_prova = questao_prova.get('alternativesIntroduction', '')[:100] + "..."
            print(f"   Enunciado prova: {enunciado_prova}")
    else:
        print("✅ Todas as questões têm boa similaridade")
    
    # Verifica questões adicionadas manualmente
    questoes_manuais = [q for q in questoes_prova if q.get('is_manual_addition')]
    if questoes_manuais:
        print(f"\n📝 Questões adicionadas manualmente ({len(questoes_manuais)}):")
        for questao in questoes_manuais:
            print(f"   - Questão {questao.get('index')} ({questao.get('discipline')})")
    
    # Verifica se há questões sem tópicos
    questoes_sem_topicos = [q for q in questoes_prova if not q.get('topicos')]
    if questoes_sem_topicos:
        print(f"\n❌ Questões sem tópicos ({len(questoes_sem_topicos)}):")
        for questao in questoes_sem_topicos:
            print(f"   - Questão {questao.get('index')}")
    else:
        print(f"\n✅ Todas as questões têm tópicos")

if __name__ == "__main__":
    analyze_questions_quality() 