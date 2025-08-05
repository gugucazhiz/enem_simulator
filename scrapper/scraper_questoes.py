import json
import re
import sys
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def extrair_questoes(html_content: str) -> List[Dict[str, Any]]:
    """
    Extrai questões do HTML com número, enunciado e tópicos
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    questoes = []
    
    # Encontrar todas as questões
    question_items = soup.find_all('div', class_='js-question-item q-question-item')
    
    for item in question_items:
        questao = {}
        
        # Extrair número da questão
        q_index = item.find('span', class_='q-index js-question-index visible')
        if q_index:
            questao['numero'] = q_index.get_text(strip=True)
        
        # Extrair enunciado
        enunciado_div = item.find('div', class_='q-question-enunciation')
        if enunciado_div:
            # Remover tags HTML mas manter o texto
            enunciado_texto = enunciado_div.get_text(strip=True)
            questao['enunciado'] = enunciado_texto
        
        # Extrair tópicos/assuntos
        breadcrumb = item.find('div', class_='q-question-breadcrumb')
        topicos = []
        if breadcrumb:
            links = breadcrumb.find_all('a', class_='q-link')
            for link in links:
                topico = link.get_text(strip=True)
                if topico:  # Só adicionar se não estiver vazio
                    topicos.append(topico)
        
        questao['topicos'] = topicos
        
        # Só adicionar se tiver número e enunciado
        if 'numero' in questao and 'enunciado' in questao:
            questoes.append(questao)
    
    return questoes

def salvar_json(questoes: List[Dict[str, Any]], arquivo_saida: str = 'questoes_extraidas.json'):
    """
    Salva as questões extraídas em um arquivo JSON
    """
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(questoes, f, ensure_ascii=False, indent=2)
    
    print(f"Questões salvas em: {arquivo_saida}")
    print(f"Total de questões extraídas: {len(questoes)}")

def main():
    """
    Função principal para executar o scraper
    """
    try:
        # Verificar se foi passado um arquivo como argumento
        if len(sys.argv) > 1:
            html_file = sys.argv[1]
            print(f"Usando arquivo HTML: {html_file}")
        else:
            html_file = 'debug_page.html'
            print(f"Usando arquivo padrão: {html_file}")
        
        # Ler o arquivo HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("Iniciando extração de questões...")
        
        # Extrair questões
        questoes = extrair_questoes(html_content)
        
        # Determinar nome do arquivo de saída
        if len(sys.argv) > 2:
            arquivo_saida = sys.argv[2]
        else:
            # Extrair número da página do nome do arquivo
            import re
            match = re.search(r'page_(\d+)', html_file)
            if match:
                page_num = match.group(1)
                arquivo_saida = f'questoes_extraidas_page_{page_num}.json'
            else:
                arquivo_saida = 'questoes_extraidas.json'
        
        # Salvar em JSON
        salvar_json(questoes, arquivo_saida)
        
        # Mostrar algumas estatísticas
        print("\nEstatísticas:")
        print(f"- Total de questões: {len(questoes)}")
        
        if questoes:
            print(f"- Primeira questão: {questoes[0]['numero']}")
            print(f"- Última questão: {questoes[-1]['numero']}")
            
            # Mostrar exemplo da primeira questão
            print("\nExemplo da primeira questão:")
            print(json.dumps(questoes[0], ensure_ascii=False, indent=2))
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{html_file}' não encontrado!")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main() 