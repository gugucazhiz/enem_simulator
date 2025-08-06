#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para demonstrar como adicionar uma questão com alternativas
"""

import json
from fix_and_improve_questions import get_user_input_for_question, add_question_to_prova, load_json_file

def test_add_question_with_alternatives():
    """
    Testa a adição de uma questão com alternativas
    """
    print("🧪 Teste: Adicionando questão com alternativas")
    print("="*50)
    
    # Carrega os arquivos
    questoes_com_topicos = load_json_file('questoes_extraidas_completas.json')
    if not questoes_com_topicos:
        return
    
    prova_com_topicos_data = load_json_file('prova_2023_com_topicos.json')
    if not prova_com_topicos_data:
        return
    
    questoes_prova_topicos = prova_com_topicos_data.get('questions', [])
    
    # Simula uma questão que faltou
    questao_teste = {
        "numero": "999",
        "enunciado": "Esta é uma questão de teste para demonstrar como adicionar alternativas. Qual é a capital do Brasil?",
        "topicos": [
            "Geografia",
            "Conhecimentos Gerais",
            "Brasil"
        ]
    }
    
    print(f"\n📝 Questão de teste:")
    print(f"   Número: {questao_teste['numero']}")
    print(f"   Enunciado: {questao_teste['enunciado']}")
    print(f"   Tópicos: {', '.join(questao_teste['topicos'])}")
    
    print(f"\n💡 Agora você pode configurar esta questão:")
    print("   - Escolher disciplina")
    print("   - Escolher idioma (se aplicável)")
    print("   - Inserir as 5 alternativas (A, B, C, D, E)")
    print("   - Definir qual é a alternativa correta")
    
    resposta = input(f"\nDeseja testar a adição da Questão {questao_teste['numero']}? (s/n): ").strip().lower()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        questao_configurada = get_user_input_for_question(questao_teste)
        
        if questao_configurada:
            questoes_prova_topicos = add_question_to_prova(questao_configurada, questoes_prova_topicos)
            
            # Atualiza o arquivo
            prova_com_topicos_data['questions'] = questoes_prova_topicos
            prova_com_topicos_data['metadata']['total_questions'] = len(questoes_prova_topicos)
            prova_com_topicos_data['metadata']['questions_with_topics'] = len([q for q in questoes_prova_topicos if q.get('topicos')])
            
            # Salva o arquivo
            with open('prova_2023_com_topicos.json', 'w', encoding='utf-8') as f:
                json.dump(prova_com_topicos_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Questão {questao_teste['numero']} adicionada com sucesso!")
            print(f"📊 Total de questões: {len(questoes_prova_topicos)}")
            
            # Mostra a questão adicionada
            print(f"\n📋 Questão adicionada:")
            print(f"   Título: {questao_configurada['title']}")
            print(f"   Disciplina: {questao_configurada['discipline']}")
            print(f"   Idioma: {questao_configurada['language']}")
            print(f"   Alternativa correta: {questao_configurada['correctAlternative']}")
            print(f"   Alternativas:")
            for alt in questao_configurada['alternatives']:
                status = "✓" if alt['isCorrect'] else " "
                print(f"     {status} {alt['letter']}: {alt['text']}")
        else:
            print(f"❌ Questão {questao_teste['numero']} não foi adicionada")
    else:
        print("❌ Teste cancelado")

if __name__ == "__main__":
    test_add_question_with_alternatives() 