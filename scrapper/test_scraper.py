#!/usr/bin/env python3
"""
Script de teste para verificar se o scraper está funcionando corretamente
"""

import os
import json
import subprocess
from scraper_questoes import extrair_questoes

def test_scraper_with_sample():
    """Testa o scraper com o arquivo debug_page.html existente"""
    print("🧪 Testando scraper com arquivo existente...")
    
    if not os.path.exists("debug_page.html"):
        print("❌ Arquivo debug_page.html não encontrado!")
        return False
    
    try:
        # Ler o arquivo HTML
        with open("debug_page.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Extrair questões
        questoes = extrair_questoes(html_content)
        
        if questoes:
            print(f"✅ Teste bem-sucedido! {len(questoes)} questões extraídas")
            
            # Mostrar exemplo
            print(f"\n📋 Exemplo da primeira questão:")
            print(f"   Número: {questoes[0]['numero']}")
            print(f"   Tópicos: {', '.join(questoes[0]['topicos'])}")
            print(f"   Enunciado: {questoes[0]['enunciado'][:100]}...")
            
            return True
        else:
            print("❌ Nenhuma questão foi extraída")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def test_scraper_command_line():
    """Testa o scraper via linha de comando"""
    print("\n🔧 Testando scraper via linha de comando...")
    
    if not os.path.exists("debug_page.html"):
        print("❌ Arquivo debug_page.html não encontrado!")
        return False
    
    try:
        # Executar scraper via linha de comando
        result = subprocess.run([
            "python", "scraper_questoes.py", "debug_page.html", "test_output.json"
        ], capture_output=True, text=True, encoding="utf-8")
        
        if result.returncode == 0:
            print("✅ Scraper executado com sucesso via linha de comando")
            
            # Verificar se o arquivo foi criado
            if os.path.exists("test_output.json"):
                with open("test_output.json", "r", encoding="utf-8") as f:
                    questoes = json.load(f)
                print(f"   • {len(questoes)} questões salvas em test_output.json")
                
                # Limpar arquivo de teste
                os.remove("test_output.json")
                return True
            else:
                print("❌ Arquivo de saída não foi criado")
                return False
        else:
            print(f"❌ Erro ao executar scraper: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 INICIANDO TESTES DO SCRAPER")
    print("=" * 50)
    
    # Teste 1: Scraper direto
    test1_success = test_scraper_with_sample()
    
    # Teste 2: Scraper via linha de comando
    test2_success = test_scraper_command_line()
    
    # Resultado final
    print("\n" + "=" * 50)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 50)
    
    if test1_success and test2_success:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎯 O scraper está funcionando corretamente")
        print("\n📝 Próximos passos:")
        print("   1. Execute: python scrapper.py")
        print("   2. Aguarde o processamento de todas as páginas")
        print("   3. Verifique os arquivos gerados em html_pages/")
        print("   4. Verifique os JSONs gerados: questoes_extraidas_page_*.json")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        if not test1_success:
            print("   • Teste direto do scraper falhou")
        if not test2_success:
            print("   • Teste via linha de comando falhou")
        print("\n🔧 Verifique:")
        print("   1. Se o arquivo debug_page.html existe")
        print("   2. Se todas as dependências estão instaladas")
        print("   3. Se há erros no código")

if __name__ == "__main__":
    main() 