#!/usr/bin/env python3
"""
Script de teste para verificar a detecção de páginas
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

def setup_chrome_options():
    """Configura as opções do Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options

def test_page_detection():
    """Testa a detecção de páginas"""
    print("🔍 TESTANDO DETECÇÃO DE PÁGINAS")
    print("=" * 50)
    
    # Configurar Chrome
    chrome_options = setup_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # URL base
        base_url = "https://www.qconcursos.com/questoes-do-enem/provas/inep-2023-enem-exame-nacional-do-ensino-medio-primeiro-e-segundo-dia-edital-2023/questoes"
        
        print(f"Acessando: {base_url}")
        driver.get(base_url)
        time.sleep(5)
        
        print("\n📄 ANALISANDO ELEMENTOS DE PAGINAÇÃO:")
        print("-" * 40)
        
        # 1. Procurar por elementos de paginação
        pagination_selectors = [
            ".pagination",
            ".pager", 
            "[class*='pagination']",
            "[class*='pager']",
            ".page-numbers",
            ".pagination-numbers",
            ".pagination-container",
            ".pagination-wrapper",
            "[class*='page']",
            "nav[class*='pagination']",
            "ul[class*='pagination']",
            ".pagination-nav",
            ".pagination-list",
            ".pagination-items"
        ]
        
        found_elements = []
        for selector in pagination_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                found_elements.append((selector, len(elements)))
                print(f"✅ {selector}: {len(elements)} elementos")
        
        if not found_elements:
            print("❌ Nenhum elemento de paginação encontrado")
        
        # 2. Procurar por números de página
        print("\n🔢 PROCURANDO NÚMEROS DE PÁGINA:")
        print("-" * 40)
        
        page_numbers = []
        
        # Procurar em todos os elementos
        all_elements = driver.find_elements(By.CSS_SELECTOR, "*")
        for element in all_elements:
            try:
                text = element.text.strip()
                if text.isdigit() and 1 <= int(text) <= 20:
                    page_numbers.append(int(text))
            except:
                continue
        
        # Remover duplicatas e ordenar
        page_numbers = sorted(list(set(page_numbers)))
        print(f"Encontrados números de página: {page_numbers}")
        
        if page_numbers:
            max_page = max(page_numbers)
            print(f"📊 Máximo número de página encontrado: {max_page}")
        else:
            print("❌ Nenhum número de página encontrado")
        
        # 3. Procurar por botões "próximo"
        print("\n➡️  PROCURANDO BOTÕES 'PRÓXIMO':")
        print("-" * 40)
        
        next_selectors = [
            "a[rel='next']",
            ".next",
            ".pagination-next", 
            "[class*='next']",
            "button[class*='next']",
            ".btn-next",
            ".next-page",
            "a[aria-label*='next']",
            "button[aria-label*='next']"
        ]
        
        found_next = False
        for selector in next_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"✅ Botão 'próximo' encontrado: {selector}")
                found_next = True
        
        if not found_next:
            print("❌ Nenhum botão 'próximo' encontrado")
        
        # 4. Procurar por elipses
        print("\n⋯ PROCURANDO ELIPSES:")
        print("-" * 40)
        
        ellipsis_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '...') or contains(text(), '…')]")
        if ellipsis_elements:
            print(f"✅ Encontradas {len(ellipsis_elements)} elipses")
            for elem in ellipsis_elements[:3]:  # Mostrar apenas as primeiras 3
                print(f"   - Texto: '{elem.text[:50]}...'")
        else:
            print("❌ Nenhuma elipse encontrada")
        
        # 5. Testar páginas específicas
        print("\n🧪 TESTANDO PÁGINAS ESPECÍFICAS:")
        print("-" * 40)
        
        existing_pages = []
        for test_page in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            try:
                test_url = f"{base_url}?page={test_page}"
                print(f"Testando página {test_page}...", end=" ")
                
                driver.get(test_url)
                time.sleep(2)
                
                # Verificar se a página carregou corretamente
                if "404" not in driver.title.lower() and "não encontrado" not in driver.page_source.lower():
                    print("✅ EXISTE")
                    existing_pages.append(test_page)
                else:
                    print("❌ NÃO EXISTE")
                    break
                    
            except Exception as e:
                print(f"❌ ERRO: {e}")
                break
        
        print(f"\n📊 RESULTADO FINAL:")
        print(f"   • Páginas existentes: {existing_pages}")
        print(f"   • Total de páginas: {len(existing_pages)}")
        
        if existing_pages:
            print(f"   • Última página: {max(existing_pages)}")
        
        return existing_pages
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return []
    
    finally:
        driver.quit()
        print("\nDriver fechado.")

def main():
    """Função principal"""
    print("🚀 INICIANDO TESTE DE DETECÇÃO DE PÁGINAS")
    print("=" * 60)
    
    existing_pages = test_page_detection()
    
    print("\n" + "=" * 60)
    print("🎯 CONCLUSÃO DO TESTE")
    print("=" * 60)
    
    if existing_pages:
        print(f"✅ Encontradas {len(existing_pages)} páginas: {existing_pages}")
        
        if len(existing_pages) >= 9:
            print("🎉 Todas as 9 páginas foram detectadas!")
        else:
            print(f"⚠️  Faltam {9 - len(existing_pages)} páginas para completar as 9")
    else:
        print("❌ Nenhuma página foi detectada")
    
    print("\n💡 RECOMENDAÇÕES:")
    if len(existing_pages) < 9:
        print("   • Verifique se o site mudou sua estrutura")
        print("   • Teste manualmente acessando as páginas 6-9")
        print("   • Considere ajustar os seletores de paginação")
    else:
        print("   • A detecção está funcionando corretamente")
        print("   • Execute o scraper principal para extrair todas as páginas")

if __name__ == "__main__":
    main() 