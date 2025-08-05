#!/usr/bin/env python3
"""
Demonstração completa do sistema de scraping de questões ENEM
"""

import os
import json
import glob
from datetime import datetime

def mostrar_banner():
    """Mostra o banner do projeto"""
    print("=" * 80)
    print("🎓 SCRAPER DE QUESTÕES ENEM - DEMONSTRAÇÃO COMPLETA")
    print("=" * 80)
    print("📚 Sistema completo de extração de questões do QConcursos")
    print("🔍 Extrai questões, enunciados e tópicos de todas as páginas")
    print("=" * 80)

def verificar_arquivos():
    """Verifica quais arquivos existem no projeto"""
    print("\n📁 VERIFICANDO ARQUIVOS DO PROJETO")
    print("-" * 40)
    
    arquivos_principais = [
        ("scrapper.py", "Script principal de scraping"),
        ("scraper_questoes.py", "Script de extração de questões"),
        ("run_complete_scraper.py", "Script de execução completa"),
        ("test_scraper.py", "Script de testes"),
        ("limpar_dados.py", "Script de limpeza de dados"),
        ("requirements.txt", "Dependências do projeto")
    ]
    
    for arquivo, descricao in arquivos_principais:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo:<25} - {descricao}")
        else:
            print(f"❌ {arquivo:<25} - {descricao}")
    
    # Verificar arquivos gerados
    print("\n📊 ARQUIVOS GERADOS:")
    
    # HTMLs
    html_files = glob.glob("html_pages/page_*.html")
    if html_files:
        print(f"✅ html_pages/ - {len(html_files)} páginas HTML salvas")
    else:
        print("❌ html_pages/ - Nenhuma página HTML encontrada")
    
    # JSONs por página
    json_files = glob.glob("questoes_extraidas_page_*.json")
    if json_files:
        print(f"✅ questoes_extraidas_page_*.json - {len(json_files)} arquivos")
    else:
        print("❌ questoes_extraidas_page_*.json - Nenhum arquivo encontrado")
    
    # JSON combinado
    if os.path.exists("questoes_extraidas_completas.json"):
        with open("questoes_extraidas_completas.json", "r", encoding="utf-8") as f:
            questoes = json.load(f)
        print(f"✅ questoes_extraidas_completas.json - {len(questoes)} questões")
    else:
        print("❌ questoes_extraidas_completas.json - Não encontrado")
    
    # JSON limpo
    if os.path.exists("questoes_limpas.json"):
        with open("questoes_limpas.json", "r", encoding="utf-8") as f:
            questoes = json.load(f)
        print(f"✅ questoes_limpas.json - {len(questoes)} questões limpas")
    else:
        print("❌ questoes_limpas.json - Não encontrado")

def mostrar_estatisticas():
    """Mostra estatísticas dos dados extraídos"""
    print("\n📈 ESTATÍSTICAS DOS DADOS")
    print("-" * 40)
    
    # Contar questões totais
    total_questoes = 0
    json_files = glob.glob("questoes_extraidas_page_*.json")
    
    if json_files:
        for json_file in sorted(json_files):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    questoes = json.load(f)
                    page_num = json_file.split("_")[-1].replace(".json", "")
                    print(f"📄 Página {page_num}: {len(questoes)} questões")
                    total_questoes += len(questoes)
            except Exception as e:
                print(f"❌ Erro ao ler {json_file}: {e}")
        
        print(f"\n🎯 Total de questões extraídas: {total_questoes}")
        
        # Mostrar distribuição por tópicos
        if total_questoes > 0:
            print("\n🏷️  DISTRIBUIÇÃO POR TÓPICOS:")
            topicos_count = {}
            
            for json_file in json_files:
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        questoes = json.load(f)
                        for questao in questoes:
                            for topico in questao.get('topicos', []):
                                topicos_count[topico] = topicos_count.get(topico, 0) + 1
                except:
                    continue
            
            # Mostrar top 10 tópicos
            sorted_topicos = sorted(topicos_count.items(), key=lambda x: x[1], reverse=True)
            for topico, count in sorted_topicos[:10]:
                print(f"   • {topico}: {count} questões")
    else:
        print("❌ Nenhum arquivo JSON encontrado para análise")

def mostrar_exemplos():
    """Mostra exemplos de questões extraídas"""
    print("\n📋 EXEMPLOS DE QUESTÕES EXTRAÍDAS")
    print("-" * 40)
    
    # Procurar por questões
    json_files = glob.glob("questoes_extraidas_page_*.json")
    
    if json_files:
        # Pegar a primeira página
        with open(json_files[0], "r", encoding="utf-8") as f:
            questoes = json.load(f)
        
        if questoes:
            # Mostrar primeira questão
            questao = questoes[0]
            print(f"🎯 QUESTÃO {questao['numero']}:")
            print(f"   Tópicos: {', '.join(questao['topicos'])}")
            print(f"   Enunciado: {questao['enunciado'][:150]}...")
            
            # Mostrar questão com mais tópicos
            questao_mais_topicos = max(questoes, key=lambda x: len(x.get('topicos', [])))
            if questao_mais_topicos != questao:
                print(f"\n🏆 QUESTÃO COM MAIS TÓPICOS ({questao_mais_topicos['numero']}):")
                print(f"   Tópicos: {', '.join(questao_mais_topicos['topicos'])}")
                print(f"   Enunciado: {questao_mais_topicos['enunciado'][:150]}...")
    else:
        print("❌ Nenhuma questão encontrada para mostrar")

def mostrar_comandos():
    """Mostra comandos disponíveis"""
    print("\n🚀 COMANDOS DISPONÍVEIS")
    print("-" * 40)
    
    comandos = [
        ("python run_complete_scraper.py", "Executar processo completo de scraping"),
        ("python scrapper.py", "Executar apenas o scraper principal"),
        ("python test_scraper.py", "Executar testes do scraper"),
        ("python limpar_dados.py", "Limpar e processar dados"),
        ("python demonstracao.py", "Executar demonstração"),
        ("python scraper_questoes.py arquivo.html", "Extrair questões de um HTML específico")
    ]
    
    for comando, descricao in comandos:
        print(f"💻 {comando:<35} - {descricao}")

def mostrar_proximos_passos():
    """Mostra próximos passos recomendados"""
    print("\n🎯 PRÓXIMOS PASSOS RECOMENDADOS")
    print("-" * 40)
    
    if not glob.glob("html_pages/page_*.html"):
        print("1️⃣  Execute o scraping completo:")
        print("   python run_complete_scraper.py")
        print()
    
    if not os.path.exists("questoes_limpas.json"):
        print("2️⃣  Processe e limpe os dados:")
        print("   python limpar_dados.py")
        print()
    
    print("3️⃣  Analise os resultados:")
    print("   - Verifique os arquivos em html_pages/")
    print("   - Analise os JSONs gerados")
    print("   - Use questoes_limpas.json para análise")
    print()
    
    print("4️⃣  Personalize o scraper:")
    print("   - Modifique scrapper.py para outros sites")
    print("   - Ajuste os seletores em scraper_questoes.py")
    print("   - Adicione novos campos de extração")

def main():
    """Função principal"""
    mostrar_banner()
    
    # Verificar arquivos
    verificar_arquivos()
    
    # Mostrar estatísticas
    mostrar_estatisticas()
    
    # Mostrar exemplos
    mostrar_exemplos()
    
    # Mostrar comandos
    mostrar_comandos()
    
    # Mostrar próximos passos
    mostrar_proximos_passos()
    
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main() 