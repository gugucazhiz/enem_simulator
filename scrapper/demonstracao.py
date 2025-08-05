#!/usr/bin/env python3
"""
Demonstração do Scraper de Questões ENEM
Mostra todas as funcionalidades implementadas
"""

import json
from scraper_questoes import extrair_questoes
from limpar_dados import processar_questoes

def mostrar_estatisticas(questoes):
    """Mostra estatísticas detalhadas das questões extraídas"""
    print("=" * 60)
    print("📊 ESTATÍSTICAS DO SCRAPER")
    print("=" * 60)
    
    print(f"📝 Total de questões extraídas: {len(questoes)}")
    
    # Contar questões por disciplina
    disciplinas = {}
    for questao in questoes:
        for topico in questao['topicos']:
            if 'Inglês' in topico or 'Português' in topico:
                disciplina = 'Inglês' if 'Inglês' in topico else 'Português'
                disciplinas[disciplina] = disciplinas.get(disciplina, 0) + 1
    
    print(f"\n📚 Distribuição por disciplina:")
    for disciplina, count in disciplinas.items():
        print(f"   • {disciplina}: {count} questões")
    
    # Mostrar todos os tópicos únicos
    todos_topicos = set()
    for questao in questoes:
        todos_topicos.update(questao['topicos'])
    
    print(f"\n🏷️  Tópicos encontrados ({len(todos_topicos)} total):")
    for topico in sorted(todos_topicos):
        print(f"   • {topico}")
    
    # Questão com mais tópicos
    questao_mais_topicos = max(questoes, key=lambda x: len(x['topicos']))
    print(f"\n🎯 Questão com mais tópicos:")
    print(f"   Questão {questao_mais_topicos['numero']} - {len(questao_mais_topicos['topicos'])} tópicos")
    print(f"   Tópicos: {', '.join(questao_mais_topicos['topicos'])}")

def mostrar_exemplos(questoes):
    """Mostra exemplos de questões extraídas"""
    print("\n" + "=" * 60)
    print("📋 EXEMPLOS DE QUESTÕES EXTRAÍDAS")
    print("=" * 60)
    
    # Exemplo 1: Questão de Inglês
    questao_ingles = next((q for q in questoes if 'Inglês' in q['topicos']), None)
    if questao_ingles:
        print(f"\n🇬🇧 QUESTÃO DE INGLÊS (Questão {questao_ingles['numero']}):")
        print(f"Enunciado: {questao_ingles['enunciado'][:150]}...")
        print(f"Tópicos: {', '.join(questao_ingles['topicos'])}")
    
    # Exemplo 2: Questão de Português
    questao_portugues = next((q for q in questoes if 'Português' in q['topicos']), None)
    if questao_portugues:
        print(f"\n🇧🇷 QUESTÃO DE PORTUGUÊS (Questão {questao_portugues['numero']}):")
        print(f"Enunciado: {questao_portugues['enunciado'][:150]}...")
        print(f"Tópicos: {', '.join(questao_portugues['topicos'])}")

def mostrar_estrutura_json():
    """Mostra a estrutura do JSON gerado"""
    print("\n" + "=" * 60)
    print("📄 ESTRUTURA DO JSON GERADO")
    print("=" * 60)
    
    try:
        with open('questoes_limpas.json', 'r', encoding='utf-8') as f:
            questoes = json.load(f)
        
        if questoes:
            exemplo = questoes[0]
            print("Estrutura de cada questão:")
            print(json.dumps(exemplo, ensure_ascii=False, indent=2))
            
            print(f"\n📁 Arquivos gerados:")
            print("   • questoes_extraidas.json - Dados brutos")
            print("   • questoes_limpas.json - Dados processados")
            
    except FileNotFoundError:
        print("❌ Arquivo JSON não encontrado. Execute o scraper primeiro!")

def main():
    """Função principal de demonstração"""
    print("🚀 DEMONSTRAÇÃO DO SCRAPER DE QUESTÕES ENEM")
    print("=" * 60)
    
    try:
        # Processar questões limpas
        questoes_limpas = processar_questoes()
        
        if questoes_limpas:
            # Mostrar estatísticas
            mostrar_estatisticas(questoes_limpas)
            
            # Mostrar exemplos
            mostrar_exemplos(questoes_limpas)
            
            # Mostrar estrutura JSON
            mostrar_estrutura_json()
            
            print("\n" + "=" * 60)
            print("✅ SCRAPER EXECUTADO COM SUCESSO!")
            print("=" * 60)
            print("📁 Arquivos criados:")
            print("   • scraper_questoes.py - Script principal")
            print("   • limpar_dados.py - Script de limpeza")
            print("   • questoes_extraidas.json - Dados brutos")
            print("   • questoes_limpas.json - Dados finais")
            print("   • README.md - Documentação")
            print("   • requirements.txt - Dependências")
            
        else:
            print("❌ Erro ao processar questões!")
            
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")

if __name__ == "__main__":
    main() 