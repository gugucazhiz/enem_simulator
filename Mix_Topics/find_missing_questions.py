#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar questões que faltaram no arquivo prova_2023_com_topicos.json
e permitir que o usuário as adicione manualmente
"""

import json
import re
from typing import Dict, List, Set, Any

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

def find_missing_questions(questoes_com_topicos: List[Dict], prova_com_topicos: List[Dict]) -> List[Dict]:
    """
    Encontra questões que estão em questoes_com_topicos mas não em prova_com_topicos
    """
    # Extrai os números das questões que já estão no arquivo prova_com_topicos
    numeros_existentes = set()
    for questao in prova_com_topicos:
        index = questao.get('index', 0)
        numeros_existentes.add(index)
    
    # Encontra questões que faltam
    questoes_faltando = []
    for questao in questoes_com_topicos:
        numero = int(questao.get('numero', 0))
        if numero not in numeros_existentes:
            questoes_faltando.append(questao)
    
    return questoes_faltando

def display_question_info(questao: Dict) -> None:
    """
    Exibe informações de uma questão
    """
    print(f"\n{'='*80}")
    print(f"Questão {questao.get('numero', 'N/A')}")
    print(f"{'='*80}")
    
    enunciado = questao.get('enunciado', '')
    if len(enunciado) > 200:
        enunciado = enunciado[:200] + "..."
    
    print(f"Enunciado: {enunciado}")
    print(f"Tópicos: {', '.join(questao.get('topicos', []))}")
    print(f"{'='*80}")

def find_similar_question_in_prova(questao_faltando: Dict, prova_completa: List[Dict]) -> Dict:
    """
    Tenta encontrar uma questão semelhante na prova completa
    """
    numero_faltando = int(questao_faltando.get('numero', 0))
    enunciado_faltando = questao_faltando.get('enunciado', '')
    
    # Primeiro tenta encontrar pelo número
    for questao_prova in prova_completa:
        if questao_prova.get('index', 0) == numero_faltando:
            return questao_prova
    
    # Se não encontrou pelo número, tenta pelo enunciado
    melhor_match = None
    melhor_similaridade = 0.0
    
    for questao_prova in prova_completa:
        enunciado_prova = ""
        if 'alternativesIntroduction' in questao_prova:
            enunciado_prova = questao_prova['alternativesIntroduction']
        elif 'context' in questao_prova:
            context = questao_prova['context']
            context = re.sub(r'!\[.*?\]\(.*?\)', '', context)
            context = re.sub(r'\*\*.*?\*\*', '', context)
            context = re.sub(r'\\\[.*?\\\]', '', context)
            enunciado_prova = context.strip()
        
        # Calcula similaridade simples
        palavras_faltando = set(enunciado_faltando.lower().split())
        palavras_prova = set(enunciado_prova.lower().split())
        
        if palavras_faltando and palavras_prova:
            similaridade = len(palavras_faltando.intersection(palavras_prova)) / len(palavras_faltando.union(palavras_prova))
            if similaridade > melhor_similaridade:
                melhor_similaridade = similaridade
                melhor_match = questao_prova
    
    return melhor_match if melhor_similaridade > 0.3 else None

def add_question_to_prova(questao_faltando: Dict, questao_prova: Dict, prova_com_topicos: List[Dict]) -> List[Dict]:
    """
    Adiciona uma questão faltando ao arquivo prova_com_topicos
    """
    # Cria a questão resultante
    questao_resultado = questao_prova.copy()
    questao_resultado['topicos'] = questao_faltando.get('topicos', [])
    questao_resultado['similarity_score'] = 1.0
    questao_resultado['matched_question_number'] = questao_faltando.get('numero')
    
    # Adiciona a questão na posição correta (ordenada por índice)
    prova_com_topicos.append(questao_resultado)
    prova_com_topicos.sort(key=lambda x: x.get('index', 0))
    
    return prova_com_topicos

def main():
    """
    Função principal do script
    """
    print("🔍 Procurando questões que faltaram...")
    
    # Carrega os arquivos
    questoes_com_topicos = load_json_file('questoes_extraidas_completas.json')
    if not questoes_com_topicos:
        return
    
    prova_com_topicos_data = load_json_file('prova_2022_com_topicos.json')
    if not prova_com_topicos_data:
        return
    
    prova_completa_data = load_json_file('Prova_completa2022.json')
    if not prova_completa_data:
        return
    
    # Extrai as questões
    questoes_prova_topicos = prova_com_topicos_data.get('questions', [])
    questoes_prova_completa = prova_completa_data.get('questions', [])
    
    # Encontra questões que faltam
    questoes_faltando = find_missing_questions(questoes_com_topicos, questoes_prova_topicos)
    
    if not questoes_faltando:
        print("✅ Todas as questões já estão no arquivo prova_2023_com_topicos.json!")
        return
    
    print(f"\n❌ Encontradas {len(questoes_faltando)} questões que faltam:")
    
    for i, questao in enumerate(questoes_faltando, 1):
        print(f"{i}. Questão {questao.get('numero', 'N/A')}")
    
    print(f"\n{'='*80}")
    print("Deseja adicionar as questões que faltam?")
    print("1. Sim - Adicionar todas automaticamente")
    print("2. Sim - Revisar cada questão individualmente")
    print("3. Não - Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (1-3): ").strip()
            
            if opcao == "1":
                # Adiciona todas automaticamente
                print("\n🔄 Adicionando todas as questões automaticamente...")
                
                for questao_faltando in questoes_faltando:
                    questao_prova = find_similar_question_in_prova(questao_faltando, questoes_prova_completa)
                    
                    if questao_prova:
                        questoes_prova_topicos = add_question_to_prova(questao_faltando, questao_prova, questoes_prova_topicos)
                        print(f"✅ Questão {questao_faltando.get('numero')} adicionada automaticamente")
                    else:
                        print(f"⚠️  Questão {questao_faltando.get('numero')} não encontrada na prova completa")
                
                break
                
            elif opcao == "2":
                # Revisa cada questão individualmente
                print("\n🔍 Revisando questões individualmente...")
                
                for questao_faltando in questoes_faltando:
                    display_question_info(questao_faltando)
                    
                    questao_prova = find_similar_question_in_prova(questao_faltando, questoes_prova_completa)
                    
                    if questao_prova:
                        print(f"\n📋 Questão encontrada na prova completa:")
                        print(f"   Título: {questao_prova.get('title', 'N/A')}")
                        print(f"   Índice: {questao_prova.get('index', 'N/A')}")
                        
                        resposta = input(f"\nDeseja adicionar a Questão {questao_faltando.get('numero')}? (s/n): ").strip().lower()
                        
                        if resposta in ['s', 'sim', 'y', 'yes']:
                            questoes_prova_topicos = add_question_to_prova(questao_faltando, questao_prova, questoes_prova_topicos)
                            print(f"✅ Questão {questao_faltando.get('numero')} adicionada!")
                        else:
                            print(f"❌ Questão {questao_faltando.get('numero')} não foi adicionada")
                    else:
                        print(f"⚠️  Questão {questao_faltando.get('numero')} não encontrada na prova completa")
                        resposta = input("Deseja continuar mesmo assim? (s/n): ").strip().lower()
                        if resposta not in ['s', 'sim', 'y', 'yes']:
                            break
                
                break
                
            elif opcao == "3":
                print("👋 Saindo...")
                return
                
            else:
                print("❌ Opção inválida. Escolha 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada pelo usuário")
            return
        except Exception as e:
            print(f"❌ Erro: {e}")
            return
    
    # Atualiza o arquivo
    if questoes_faltando:
        print(f"\n💾 Salvando arquivo atualizado...")
        
        # Atualiza os metadados
        prova_com_topicos_data['questions'] = questoes_prova_topicos
        prova_com_topicos_data['metadata']['total_questions'] = len(questoes_prova_topicos)
        prova_com_topicos_data['metadata']['questions_with_topics'] = len([q for q in questoes_prova_topicos if q.get('topicos')])
        
        # Salva o arquivo
        with open('prova_2023_com_topicos.json', 'w', encoding='utf-8') as f:
            json.dump(prova_com_topicos_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Arquivo prova_2023_com_topicos.json atualizado com sucesso!")
        print(f"📊 Total de questões: {len(questoes_prova_topicos)}")
        print(f"📊 Questões com tópicos: {prova_com_topicos_data['metadata']['questions_with_topics']}")

if __name__ == "__main__":
    main() 