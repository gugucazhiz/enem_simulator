import json
import re

def limpar_enunciado(enunciado: str) -> str:
    """
    Limpa e formata o enunciado da questão
    """
    # Remover quebras de linha excessivas
    enunciado = re.sub(r'\n\s*\n', '\n', enunciado)
    
    # Remover espaços em branco no início e fim
    enunciado = enunciado.strip()
    
    # Substituir múltiplos espaços por um único
    enunciado = re.sub(r'\s+', ' ', enunciado)
    
    return enunciado

def limpar_topicos(topicos: list) -> list:
    """
    Limpa e formata os tópicos
    """
    topicos_limpos = []
    
    for topico in topicos:
        # Remover vírgulas no final
        topico = topico.rstrip(',')
        
        # Remover espaços em branco
        topico = topico.strip()
        
        if topico:  # Só adicionar se não estiver vazio
            topicos_limpos.append(topico)
    
    return topicos_limpos

def processar_questoes(arquivo_entrada: str = 'questoes_extraidas.json', 
                       arquivo_saida: str = 'questoes_limpas.json'):
    """
    Processa e limpa os dados das questões
    """
    try:
        # Ler dados originais
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            questoes = json.load(f)
        
        questoes_limpas = []
        
        for questao in questoes:
            questao_limpa = {
                'numero': questao['numero'],
                'enunciado': limpar_enunciado(questao['enunciado']),
                'topicos': limpar_topicos(questao['topicos'])
            }
            questoes_limpas.append(questao_limpa)
        
        # Salvar dados limpos
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(questoes_limpas, f, ensure_ascii=False, indent=2)
        
        print(f"Dados limpos salvos em: {arquivo_saida}")
        print(f"Total de questões processadas: {len(questoes_limpas)}")
        
        # Mostrar estatísticas
        print("\nEstatísticas dos tópicos:")
        todos_topicos = set()
        for questao in questoes_limpas:
            todos_topicos.update(questao['topicos'])
        
        print(f"- Total de tópicos únicos: {len(todos_topicos)}")
        print("- Tópicos encontrados:")
        for topico in sorted(todos_topicos):
            print(f"  • {topico}")
        
        return questoes_limpas
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        return None
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        return None

def mostrar_exemplo(questoes_limpas, numero_questao: str = "1"):
    """
    Mostra um exemplo de questão específica
    """
    for questao in questoes_limpas:
        if questao['numero'] == numero_questao:
            print(f"\nExemplo da questão {numero_questao}:")
            print(json.dumps(questao, ensure_ascii=False, indent=2))
            return
    
    print(f"Questão {numero_questao} não encontrada!")

if __name__ == "__main__":
    questoes_limpas = processar_questoes()
    
    if questoes_limpas:
        mostrar_exemplo(questoes_limpas, "1")
        mostrar_exemplo(questoes_limpas, "6")  # Questão de português com mais tópicos 