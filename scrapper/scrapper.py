from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import time
import os
import subprocess
import glob
import re

def setup_chrome_options():
    """Configura as opções do Chrome para suprimir warnings e melhorar performance"""
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")  # Suprimir logs do Chrome
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

def wait_for_element(driver, by, value, timeout=10):
    """Aguarda um elemento aparecer na página"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Timeout aguardando elemento: {value}")
        return None

def handle_popups(driver):
    """Tenta fechar popups e anúncios que possam aparecer"""
    try:
        # Lista de seletores comuns para popups/ads
        popup_selectors = [
            "button[class*='close']",
            "button[class*='Close']",
            "button[class*='CLOSE']",
            ".close",
            ".Close",
            ".CLOSE",
            "[class*='modal'] [class*='close']",
            "[class*='popup'] [class*='close']",
            "[class*='ad'] [class*='close']",
            "button[aria-label*='close']",
            "button[aria-label*='Close']",
            ".modal-close",
            ".popup-close",
            ".ad-close",
            "[data-dismiss='modal']",
            "[data-close]",
            ".btn-close",
            ".close-button",
            "[class*='dismiss']",
            "[class*='Dismiss']"
        ]
        
        popups_closed = 0
        for selector in popup_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        print(f"Fechando popup encontrado: {selector}")
                        element.click()
                        time.sleep(0.5)
                        popups_closed += 1
            except:
                continue
        
        # Tentar pressionar ESC para fechar popups
        try:
            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)
            print("Pressionado ESC para fechar popups")
        except:
            pass
        
        if popups_closed > 0:
            print(f"Fechados {popups_closed} popups/anúncios")
        
    except Exception as e:
        print(f"Erro ao tentar fechar popups: {e}")

def get_total_pages(driver):
    """Tenta encontrar o número total de páginas"""
    try:
        print("🔍 Procurando elementos de paginação...")
        
        # Procurar por elementos de paginação mais específicos
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
        
        max_page = 1
        
        for selector in pagination_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Encontrado elemento de paginação: {selector}")
                    
                    for element in elements:
                        # Procurar por números de página dentro do elemento
                        page_elements = element.find_elements(By.CSS_SELECTOR, "a, span, li, button, .page, .page-number")
                        
                        for page_elem in page_elements:
                            try:
                                text = page_elem.text.strip()
                                # Verificar se é um número
                                if text.isdigit():
                                    page_num = int(text)
                                    if page_num > max_page:
                                        max_page = page_num
                                        print(f"   Encontrada página: {page_num}")
                            except:
                                continue
                        
                        # Procurar por atributos que possam conter números de página
                        try:
                            href = element.get_attribute("href")
                            if href and "page=" in href:
                                # Extrair número da URL
                                match = re.search(r'page=(\d+)', href)
                                if match:
                                    page_num = int(match.group(1))
                                    if page_num > max_page:
                                        max_page = page_num
                                        print(f"   Encontrada página na URL: {page_num}")
                        except:
                            pass
            except Exception as e:
                continue
        
        # Procurar por texto que contenha números de página
        try:
            page_text = driver.page_source
            # Procurar por padrões como "Página X de Y" ou "Page X of Y"
            patterns = [
                r'página\s+(\d+)\s+de\s+(\d+)',
                r'page\s+(\d+)\s+of\s+(\d+)',
                r'(\d+)\s*/\s*(\d+)\s*páginas',
                r'(\d+)\s*/\s*(\d+)\s*pages'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        total_pages = int(match[1])
                        if total_pages > max_page:
                            max_page = total_pages
                            print(f"Encontradas {max_page} páginas no texto")
                            break
        except:
            pass
        
        # Procurar por botões "próximo" ou "next" e tentar navegar para ver quantas páginas existem
        try:
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
            
            for selector in next_selectors:
                try:
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    if next_buttons:
                        print(f"Encontrado botão 'próximo': {selector}")
                        # Se encontrou botão próximo, provavelmente há mais páginas
                        if max_page < 5:
                            max_page = 10  # Assumir pelo menos 10 páginas
                        break
                except:
                    continue
        except:
            pass
        
        # Verificar se há elipses (...) que indicam mais páginas
        try:
            ellipsis_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '...') or contains(text(), '…')]")
            if ellipsis_elements:
                print("Encontradas elipses, indicando mais páginas")
                if max_page < 5:
                    max_page = 10  # Assumir pelo menos 10 páginas
        except:
            pass
        
        # Verificar se há elementos com números maiores que 5
        try:
            # Procurar por qualquer número maior que 5 na página
            all_text = driver.page_source
            numbers = re.findall(r'\b(\d+)\b', all_text)
            for num_str in numbers:
                try:
                    num = int(num_str)
                    if 5 < num <= 20:  # Números razoáveis para páginas
                        if num > max_page:
                            max_page = num
                            print(f"Encontrado número de página: {num}")
                except:
                    continue
        except:
            pass
        
        # Se ainda não encontrou páginas suficientes, tentar uma abordagem mais agressiva
        if max_page < 9:
            print("⚠️  Tentando abordagem mais agressiva para detectar páginas...")
            
            # Tentar navegar para páginas específicas para ver se existem
            for test_page in [6, 7, 8, 9, 10]:
                try:
                    test_url = f"{driver.current_url}?page={test_page}"
                    print(f"Testando página {test_page}: {test_url}")
                    
                    # Fazer uma requisição rápida para verificar se a página existe
                    driver.get(test_url)
                    time.sleep(1)
                    
                    # Verificar se a página carregou corretamente (não é 404)
                    if "404" not in driver.title.lower() and "não encontrado" not in driver.page_source.lower():
                        max_page = max(max_page, test_page)
                        print(f"   Página {test_page} existe!")
                    else:
                        print(f"   Página {test_page} não existe (404)")
                        break
                        
                except Exception as e:
                    print(f"   Erro ao testar página {test_page}: {e}")
                    break
        
        if max_page > 1:
            print(f"✅ Total de páginas detectadas: {max_page}")
            return max_page
        else:
            print("⚠️  Não foi possível determinar o número de páginas, assumindo 1 página")
            return 1
        
    except Exception as e:
        print(f"❌ Erro ao determinar número de páginas: {e}")
        return 1

def save_page_html(driver, page_number):
    """Salva o HTML da página atual"""
    try:
        # Criar diretório se não existir
        os.makedirs("html_pages", exist_ok=True)
        
        filename = f"html_pages/page_{page_number:03d}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        print(f"HTML da página {page_number} salvo em: {filename}")
        return filename
    except Exception as e:
        print(f"Erro ao salvar HTML da página {page_number}: {e}")
        return None

def check_if_page_is_duplicate(driver, first_page_content, page_number):
    """Verifica se a página atual é uma duplicata da primeira página"""
    try:
        current_content = driver.page_source
        
        # Se for a primeira página, não é duplicata
        if page_number == 1:
            return False, current_content
        
        # Comparar o conteúdo atual com o da primeira página
        # Vamos usar uma abordagem mais robusta: comparar apenas partes específicas
        
        # Extrair questões da página atual
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(current_content, 'html.parser')
        current_questions = soup.find_all('div', class_='js-question-item q-question-item')
        
        # Extrair questões da primeira página
        first_soup = BeautifulSoup(first_page_content, 'html.parser')
        first_questions = first_soup.find_all('div', class_='js-question-item q-question-item')
        
        # Se não encontrou questões, usar comparação de texto
        if not current_questions or not first_questions:
            # Comparar uma parte do conteúdo (primeiros 1000 caracteres)
            current_sample = current_content[:1000]
            first_sample = first_page_content[:1000]
            
            similarity = len(set(current_sample) & set(first_sample)) / len(set(current_sample) | set(first_sample))
            
            if similarity > 0.8:  # 80% de similaridade
                print(f"⚠️  Página {page_number} parece ser duplicata da primeira página (similaridade: {similarity:.2f})")
                return True, current_content
            else:
                return False, current_content
        
        # Comparar IDs ou números das questões
        current_question_ids = []
        first_question_ids = []
        
        for question in current_questions:
            # Tentar extrair ID da questão
            question_id_elem = question.find('span', class_='q-index js-question-index visible')
            if question_id_elem:
                current_question_ids.append(question_id_elem.text.strip())
        
        for question in first_questions:
            question_id_elem = question.find('span', class_='q-index js-question-index visible')
            if question_id_elem:
                first_question_ids.append(question_id_elem.text.strip())
        
        # Se encontrou IDs, comparar
        if current_question_ids and first_question_ids:
            if current_question_ids == first_question_ids:
                print(f"⚠️  Página {page_number} é duplicata da primeira página (mesmas questões)")
                return True, current_content
        
        # Comparar URLs das questões
        current_urls = []
        first_urls = []
        
        for question in current_questions:
            link = question.find('a')
            if link and link.get('href'):
                current_urls.append(link.get('href'))
        
        for question in first_questions:
            link = question.find('a')
            if link and link.get('href'):
                first_urls.append(link.get('href'))
        
        if current_urls and first_urls:
            if current_urls == first_urls:
                print(f"⚠️  Página {page_number} é duplicata da primeira página (mesmas URLs)")
                return True, current_content
        
        # Comparar títulos das questões
        current_titles = []
        first_titles = []
        
        for question in current_questions:
            title_elem = question.find('h3') or question.find('h2') or question.find('h1')
            if title_elem:
                current_titles.append(title_elem.text.strip())
        
        for question in first_questions:
            title_elem = question.find('h3') or question.find('h2') or question.find('h1')
            if title_elem:
                first_titles.append(title_elem.text.strip())
        
        if current_titles and first_titles:
            if current_titles == first_titles:
                print(f"⚠️  Página {page_number} é duplicata da primeira página (mesmos títulos)")
                return True, current_content
        
        # Se chegou até aqui, provavelmente não é duplicata
        return False, current_content
        
    except Exception as e:
        print(f"Erro ao verificar duplicata da página {page_number}: {e}")
        return False, current_content

def run_scraper_on_html(html_file):
    """Executa o scraper_questoes.py no arquivo HTML especificado"""
    try:
        print(f"Executando scraper em: {html_file}")
        
        # Extrair número da página do nome do arquivo
        match = re.search(r'page_(\d+)', html_file)
        if match:
            page_num = match.group(1)
            output_file = f'questoes_extraidas_page_{page_num}.json'
        else:
            output_file = f'questoes_extraidas_{os.path.basename(html_file).replace(".html", "")}.json'
        
        # Executar o scraper diretamente
        result = subprocess.run([
            "python", "scraper_questoes.py", html_file, output_file
        ], capture_output=True, text=True, encoding="utf-8")
        
        if result.returncode == 0:
            print(f"✅ Scraper executado com sucesso em {html_file}")
            print(result.stdout)
        else:
            print(f"❌ Erro ao executar scraper em {html_file}")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Erro ao executar scraper em {html_file}: {e}")
        return False

def main():
    # Configurar opções do Chrome
    chrome_options = setup_chrome_options()
    
    # Inicializar o driver com as opções
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🚀 Iniciando scraping de todas as páginas...")
        
        # URL base
        base_url = "https://www.qconcursos.com/questoes-do-enem/provas/inep-2023-enem-exame-nacional-do-ensino-medio-primeiro-e-segundo-dia-edital-2023/questoes"
        
        # Acessar primeira página
        print(f"Acessando primeira página: {base_url}")
        driver.get(base_url)
        
        # Aguardar a página carregar
        print("Aguardando carregamento da página...")
        time.sleep(5)
        
        # Tentar fechar popups
        print("Verificando e fechando popups...")
        handle_popups(driver)
        
        # Aguardar mais um pouco após fechar popups
        time.sleep(2)
        
        # Determinar número total de páginas
        total_pages = get_total_pages(driver)
        print(f"📄 Total de páginas encontradas: {total_pages}")
        
        # Verificação adicional: se encontrou menos de 9 páginas, tentar forçar 9
        if total_pages < 9:
            print("⚠️  Detectadas menos de 9 páginas, tentando verificar se existem mais...")
            
            # Tentar navegar para a página 9 para verificar se existe
            try:
                test_url = f"{base_url}?page=9"
                print(f"Testando se a página 9 existe: {test_url}")
                driver.get(test_url)
                time.sleep(3)
                
                # Verificar se a página carregou corretamente
                if "404" not in driver.title.lower() and "não encontrado" not in driver.page_source.lower():
                    print("✅ Página 9 existe! Atualizando total para 9 páginas.")
                    total_pages = 9
                else:
                    print("❌ Página 9 não existe.")
            except Exception as e:
                print(f"Erro ao testar página 9: {e}")
        
        # Lista para armazenar todos os arquivos HTML salvos
        html_files = []
        
        # Variável para armazenar o conteúdo da primeira página
        first_page_content = None
        
        # Percorrer todas as páginas
        for page in range(1, total_pages + 1):
            print(f"\n{'='*50}")
            print(f"📖 Processando página {page}/{total_pages}")
            print(f"{'='*50}")
            
            # Se não for a primeira página, navegar para a página
            if page > 1:
                page_url = f"{base_url}?page={page}"
                print(f"Navegando para: {page_url}")
                driver.get(page_url)
                
                # Aguardar carregamento
                time.sleep(3)
                
                # Fechar popups novamente
                handle_popups(driver)
                time.sleep(1)
            
            # Verificar se a página carregou corretamente
            if "404" in driver.title.lower() or "não encontrado" in driver.page_source.lower():
                print(f"⚠️  Página {page} não encontrada (404), pulando...")
                continue
            
            # Verificar se é duplicata da primeira página
            if page > 1 and first_page_content:
                is_duplicate, _ = check_if_page_is_duplicate(driver, first_page_content, page)
                if is_duplicate:
                    print(f"🛑 Página {page} é duplicata da primeira página. Parando o scraping.")
                    print(f"✅ Scraping concluído com {page-1} páginas únicas.")
                    break
            
            # Salvar HTML da página
            html_file = save_page_html(driver, page)
            if html_file:
                html_files.append(html_file)
                
                # Se for a primeira página, salvar o conteúdo para comparação
                if page == 1:
                    first_page_content = driver.page_source
                    print("📝 Conteúdo da primeira página salvo para verificação de duplicatas")
            
            # Aguardar um pouco entre as páginas
            time.sleep(2)
        
        print(f"\n✅ Todas as {len(html_files)} páginas foram salvas!")
        
        # Executar scraper em cada arquivo HTML
        print(f"\n🔍 Executando scraper em todos os arquivos HTML...")
        
        successful_scrapes = 0
        for html_file in html_files:
            if run_scraper_on_html(html_file):
                successful_scrapes += 1
        
        print(f"\n📊 RESUMO FINAL:")
        print(f"   • Páginas processadas: {len(html_files)}")
        print(f"   • Scrapers executados com sucesso: {successful_scrapes}")
        print(f"   • Arquivos HTML salvos em: html_pages/")
        print(f"   • Arquivos JSON salvos em: questoes_extraidas_page_*.json")
        
        # Combinar todos os JSONs em um único arquivo
        print(f"\n🔗 Combinando todos os JSONs...")
        combine_all_jsons()
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()
        print("Driver fechado.")

def combine_all_jsons():
    """Combina todos os JSONs de questões em um único arquivo"""
    try:
        # Encontrar todos os arquivos JSON de questões
        json_files = glob.glob("questoes_extraidas_page_*.json")
        
        if not json_files:
            print("Nenhum arquivo JSON encontrado para combinar")
            return
        
        print(f"Encontrados {len(json_files)} arquivos JSON para combinar")
        
        all_questoes = []
        
        for json_file in sorted(json_files):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    questoes = json.load(f)
                    if isinstance(questoes, list):
                        all_questoes.extend(questoes)
                    else:
                        print(f"Formato inesperado em {json_file}")
            except Exception as e:
                print(f"Erro ao ler {json_file}: {e}")
        
        # Salvar arquivo combinado
        combined_filename = "questoes_extraidas_completas.json"
        with open(combined_filename, "w", encoding="utf-8") as f:
            json.dump(all_questoes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(all_questoes)} questões combinadas em: {combined_filename}")
        
    except Exception as e:
        print(f"Erro ao combinar JSONs: {e}")

if __name__ == "__main__":
    main()