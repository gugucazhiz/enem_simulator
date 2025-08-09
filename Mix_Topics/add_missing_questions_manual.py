#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar questões que não existem na prova original
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

def create_basic_question_structure(questao_faltando: Dict) -> Dict:
    """
    Cria uma estrutura básica para uma questão que não existe na prova original
    """
    numero = int(questao_faltando.get('numero', 0))
    
    # Cria uma estrutura básica baseada no padrão das outras questões
    questao_basica = {
        "title": f"Questão {numero} - ENEM 2023",
        "index": numero,
        "discipline": "linguagens",  # Padrão, pode ser ajustado
        "language": "portugues",     # Padrão, pode ser ajustado
        "year": 2023,
        "context": questao_faltando.get('enunciado', ''),
        "files": [],
        "correctAlternative": "A",  # Padrão, precisa ser ajustado
        "alternativesIntroduction": questao_faltando.get('enunciado', ''),
        "alternatives": [
            {
                "letter": "A",
                "text": "[Alternativa A - A ser preenchida]",
                "file": None,
                "isCorrect": True
            },
            {
                "letter": "B",
                "text": "[Alternativa B - A ser preenchida]",
                "file": None,
                "isCorrect": False
            },
            {
                "letter": "C",
                "text": "[Alternativa C - A ser preenchida]",
                "file": None,
                "isCorrect": False
            },
            {
                "letter": "D",
                "text": "[Alternativa D - A ser preenchida]",
                "file": None,
                "isCorrect": False
            },
            {
                "letter": "E",
                "text": "[Alternativa E - A ser preenchida]",
                "file": None,
                "isCorrect": False
            }
        ],
        "topicos": questao_faltando.get('topicos', []),
        "similarity_score": 1.0,
        "matched_question_number": str(numero),
        "is_manual_addition": True  # Flag para identificar questões adicionadas manualmente
    }
    
    return questao_basica

def display_question_info(questao: Dict) -> None:
    """
    Exibe informações de uma questão
    """
    print(f"\n{'='*80}")
    print(f"Questão {questao.get('numero', 'N/A')}")
    print(f"{'='*80}")
    
    enunciado = questao.get('enunciado', '')
    if len(enunciado) > 300:
        enunciado = enunciado[:300] + "..."
    
    print(f"Enunciado: {enunciado}")
    print(f"Tópicos: {', '.join(questao.get('topicos', []))}")
    print(f"{'='*80}")

def get_user_input_for_question(questao_faltando: Dict) -> Dict:
    """
    Permite ao usuário preencher informações da questão
    """
    numero = questao_faltando.get('numero', 'N/A')
    print(f"\n📝 Configurando Questão {numero}")
    print("="*50)
    
    # Cria estrutura básica
    questao_basica = create_basic_question_structure(questao_faltando)
    
    # Pergunta sobre disciplina
    print("\nDisciplinas disponíveis:")
    print("1. linguagens")
    print("2. matematica")
    print("3. ciencias_natureza")
    print("4. ciencias_humanas")
    
    while True:
        try:
            disciplina_opcao = input("Escolha a disciplina (1-4) [padrão: 1]: ").strip()
            if not disciplina_opcao:
                disciplina_opcao = "1"
            
            disciplinas = {
                "1": "linguagens",
                "2": "matematica", 
                "3": "ciencias_natureza",
                "4": "ciencias_humanas"
            }
            
            if disciplina_opcao in disciplinas:
                questao_basica["discipline"] = disciplinas[disciplina_opcao]
                break
            else:
                print("❌ Opção inválida. Escolha 1, 2, 3 ou 4.")
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada")
            return None
    
    # Pergunta sobre idioma (se for linguagens)
    if questao_basica["discipline"] == "linguagens":
        print("\nIdiomas disponíveis:")
        print("1. portugues")
        print("2. ingles")
        print("3. espanhol")
        
        while True:
            try:
                idioma_opcao = input("Escolha o idioma (1-3) [padrão: 1]: ").strip()
                if not idioma_opcao:
                    idioma_opcao = "1"
                
                idiomas = {
                    "1": "portugues",
                    "2": "ingles",
                    "3": "espanhol"
                }
                
                if idioma_opcao in idiomas:
                    questao_basica["language"] = idiomas[idioma_opcao]
                    break
                else:
                    print("❌ Opção inválida. Escolha 1, 2 ou 3.")
            except KeyboardInterrupt:
                print("\n👋 Operação cancelada")
                return None
    
    # Pergunta sobre alternativa correta
    print(f"\nAlternativa correta:")
    print("A, B, C, D ou E")
    
    while True:
        try:
            alternativa_correta = input("Escolha a alternativa correta [padrão: A]: ").strip().upper()
            if not alternativa_correta:
                alternativa_correta = "A"
            
            if alternativa_correta in ['A', 'B', 'C', 'D', 'E']:
                questao_basica["correctAlternative"] = alternativa_correta
                
                # Atualiza as alternativas
                for alt in questao_basica["alternatives"]:
                    alt["isCorrect"] = (alt["letter"] == alternativa_correta)
                
                break
            else:
                print("❌ Opção inválida. Escolha A, B, C, D ou E.")
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada")
            return None
    
    print(f"\n✅ Questão {numero} configurada!")
    print(f"   Disciplina: {questao_basica['discipline']}")
    print(f"   Idioma: {questao_basica['language']}")
    print(f"   Alternativa correta: {questao_basica['correctAlternative']}")
    
    return questao_basica

def add_question_to_prova(questao_basica: Dict, prova_com_topicos: List[Dict]) -> List[Dict]:
    """
    Adiciona uma questão ao arquivo prova_com_topicos
    """
    # Adiciona a questão na posição correta (ordenada por índice)
    prova_com_topicos.append(questao_basica)
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
    
    # Extrai as questões
    questoes_prova_topicos = prova_com_topicos_data.get('questions', [])
    
    # Encontra questões que faltam
    questoes_faltando = find_missing_questions(questoes_com_topicos, questoes_prova_topicos)
    
    if not questoes_faltando:
        print("✅ Todas as questões já estão no arquivo prova_2023_com_topicos.json!")
        return
    
    print(f"\n❌ Encontradas {len(questoes_faltando)} questões que faltam:")
    
    for i, questao in enumerate(questoes_faltando, 1):
        print(f"{i}. Questão {questao.get('numero', 'N/A')}")
    
    print(f"\n{'='*80}")
    print("Essas questões não existem na prova original.")
    print("Deseja adicioná-las manualmente?")
    print("1. Sim - Adicionar todas com configuração padrão")
    print("2. Sim - Configurar cada questão individualmente")
    print("3. Não - Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (1-3): ").strip()
            
            if opcao == "1":
                # Adiciona todas com configuração padrão
                print("\n🔄 Adicionando todas as questões com configuração padrão...")
                
                for questao_faltando in questoes_faltando:
                    questao_basica = create_basic_question_structure(questao_faltando)
                    questoes_prova_topicos = add_question_to_prova(questao_basica, questoes_prova_topicos)
                    print(f"✅ Questão {questao_faltando.get('numero')} adicionada com configuração padrão")
                
                break
                
            elif opcao == "2":
                # Configura cada questão individualmente
                print("\n🔍 Configurando questões individualmente...")
                
                for questao_faltando in questoes_faltando:
                    display_question_info(questao_faltando)
                    
                    resposta = input(f"\nDeseja adicionar a Questão {questao_faltando.get('numero')}? (s/n): ").strip().lower()
                    
                    if resposta in ['s', 'sim', 'y', 'yes']:
                        questao_basica = get_user_input_for_question(questao_faltando)
                        
                        if questao_basica:
                            questoes_prova_topicos = add_question_to_prova(questao_basica, questoes_prova_topicos)
                            print(f"✅ Questão {questao_faltando.get('numero')} adicionada!")
                        else:
                            print(f"❌ Questão {questao_faltando.get('numero')} não foi adicionada")
                    else:
                        print(f"❌ Questão {questao_faltando.get('numero')} não foi adicionada")
                
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
        with open('prova_2022_com_topicos.json', 'w', encoding='utf-8') as f:
            json.dump(prova_com_topicos_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Arquivo prova_2022_com_topicos.json atualizado com sucesso!")
        print(f"📊 Total de questões: {len(questoes_prova_topicos)}")
        print(f"📊 Questões com tópicos: {prova_com_topicos_data['metadata']['questions_with_topics']}")
        
        # Mostra questões adicionadas manualmente
        questoes_manuais = [q for q in questoes_prova_topicos if q.get('is_manual_addition')]
        if questoes_manuais:
            print(f"\n📝 Questões adicionadas manualmente:")
            for questao in questoes_manuais:
                print(f"   - Questão {questao.get('index')} ({questao.get('discipline')})")

if __name__ == "__main__":
    main() 