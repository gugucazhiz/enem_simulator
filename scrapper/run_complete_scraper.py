#!/usr/bin/env python3
"""
Script principal para executar o scraping completo de todas as páginas
"""

import os
import time
import subprocess
import json
import glob

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = ['selenium', 'beautifulsoup4', 'lxml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Dependências faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def check_files():
    """Verifica se os arquivos necessários existem"""
    print("\n📁 Verificando arquivos necessários...")
    
    required_files = ['scrapper.py', 'scraper_questoes.py']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file}")
    
    if missing_files:
        print(f"\n❌ Arquivos faltando: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos os arquivos necessários encontrados!")
    return True

def run_scrapper():
    """Executa o script principal de scraping"""
    print("\n🚀 Executando scraper principal...")
    
    try:
        # Executar o scrapper
        result = subprocess.run(["python", "scrapper.py"], 
                              capture_output=True, text=True, encoding="utf-8")
        
        if result.returncode == 0:
            print("✅ Scraper principal executado com sucesso!")
            print(result.stdout)
            return True
        else:
            print("❌ Erro ao executar scraper principal:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar scraper: {e}")
        return False

def check_results():
    """Verifica os resultados do scraping"""
    print("\n📊 Verificando resultados...")
    
    # Verificar arquivos HTML
    html_files = glob.glob("html_pages/page_*.html")
    if html_files:
        print(f"   ✅ {len(html_files)} arquivos HTML salvos em html_pages/")
    else:
        print("   ❌ Nenhum arquivo HTML encontrado")
    
    # Verificar arquivos JSON
    json_files = glob.glob("questoes_extraidas_page_*.json")
    if json_files:
        print(f"   ✅ {len(json_files)} arquivos JSON gerados")
        
        # Contar total de questões
        total_questoes = 0
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    questoes = json.load(f)
                    total_questoes += len(questoes)
            except:
                continue
        
        print(f"   📝 Total de questões extraídas: {total_questoes}")
    else:
        print("   ❌ Nenhum arquivo JSON encontrado")
    
    # Verificar arquivo combinado
    if os.path.exists("questoes_extraidas_completas.json"):
        with open("questoes_extraidas_completas.json", 'r', encoding='utf-8') as f:
            questoes = json.load(f)
        print(f"   🎯 Arquivo combinado: {len(questoes)} questões")
    else:
        print("   ❌ Arquivo combinado não encontrado")
    
    return len(html_files) > 0 and len(json_files) > 0

def show_summary():
    """Mostra um resumo final"""
    print("\n" + "="*60)
    print("🎉 PROCESSO DE SCRAPING CONCLUÍDO!")
    print("="*60)
    
    # Contar arquivos
    html_files = glob.glob("html_pages/page_*.html")
    json_files = glob.glob("questoes_extraidas_page_*.json")
    
    print(f"📄 Páginas processadas: {len(html_files)}")
    print(f"📝 Arquivos JSON gerados: {len(json_files)}")
    
    # Contar questões totais
    total_questoes = 0
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                questoes = json.load(f)
                total_questoes += len(questoes)
        except:
            continue
    
    print(f"🎯 Total de questões extraídas: {total_questoes}")
    
    if os.path.exists("questoes_extraidas_completas.json"):
        print(f"📁 Arquivo final: questoes_extraidas_completas.json")
    
    print("\n📂 Arquivos gerados:")
    print("   • html_pages/ - Páginas HTML salvas")
    print("   • questoes_extraidas_page_*.json - Questões por página")
    print("   • questoes_extraidas_completas.json - Todas as questões")
    
    print("\n🎯 Próximos passos:")
    print("   1. Verifique os arquivos gerados")
    print("   2. Use limpar_dados.py para processar os dados")
    print("   3. Analise as questões extraídas")

def main():
    """Função principal"""
    print("🚀 INICIANDO PROCESSO COMPLETO DE SCRAPING")
    print("="*60)
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Verificar arquivos
    if not check_files():
        return
    
    # Executar scraper
    if not run_scrapper():
        print("\n❌ Falha no processo de scraping!")
        return
    
    # Verificar resultados
    if not check_results():
        print("\n⚠️  Alguns resultados podem estar incompletos!")
    
    # Mostrar resumo
    show_summary()

if __name__ == "__main__":
    main() 