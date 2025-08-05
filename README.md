# Scraper de Questões ENEM - Versão Completa

Este projeto extrai questões, enunciados e tópicos de todas as páginas do site QConcursos, salvando os HTMLs e executando o scraper em cada um deles.

## 🚀 Funcionalidades

- **Scraping de múltiplas páginas**: Percorre automaticamente todas as páginas do site
- **Salvamento de HTMLs**: Salva cada página HTML em sequência
- **Extração de questões**: Identifica todas as questões em cada página
- **Número da questão**: Extrai o número de cada questão
- **Enunciado**: Captura o texto completo do enunciado
- **Tópicos/Assuntos**: Extrai todos os tópicos relacionados à questão
- **Limpeza de dados**: Remove formatação HTML e normaliza o texto
- **Exportação JSON**: Salva os dados em formato JSON estruturado
- **Combinação automática**: Combina todos os JSONs em um arquivo final

## 📁 Estrutura dos Dados

Cada questão extraída contém:

```json
{
  "numero": "1",
  "enunciado": "Texto do enunciado da questão...",
  "topicos": [
    "Inglês",
    "Interpretação de texto | Reading comprehension"
  ]
}
```

## 🛠️ Arquivos do Projeto

### Scripts Principais
- `scrapper.py` - Script principal que percorre todas as páginas
- `scraper_questoes.py` - Script de extração de questões de um HTML
- `run_complete_scraper.py` - Script principal que executa todo o processo
- `test_scraper.py` - Script de teste para verificar funcionamento

### Scripts de Processamento
- `limpar_dados.py` - Script para limpeza e formatação dos dados
- `demonstracao.py` - Script de demonstração das funcionalidades

### Arquivos de Configuração
- `requirements.txt` - Dependências do projeto
- `README.md` - Documentação completa

### Arquivos Gerados
- `html_pages/` - Diretório com todas as páginas HTML salvas
- `questoes_extraidas_page_*.json` - Questões extraídas por página
- `questoes_extraidas_completas.json` - Todas as questões combinadas
- `questoes_limpas.json` - Dados processados e limpos

## 🎯 Como Usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o processo completo

```bash
python run_complete_scraper.py
```

### 3. Ou executar manualmente

```bash
# Executar scraper principal
python scrapper.py

# Limpar e processar os dados
python limpar_dados.py
```

### 4. Testar o funcionamento

```bash
python test_scraper.py
```

## 📊 Processo de Execução

1. **Verificação**: Checa dependências e arquivos necessários
2. **Navegação**: Percorre todas as páginas do site
3. **Salvamento**: Salva cada página HTML em `html_pages/`
4. **Extração**: Executa scraper em cada arquivo HTML
5. **Combinação**: Combina todos os JSONs em um arquivo final
6. **Limpeza**: Processa e limpa os dados (opcional)

## 🎯 Resultados Esperados

O scraper irá gerar:

- **Páginas HTML**: Uma pasta `html_pages/` com todas as páginas salvas
- **JSONs por página**: Arquivos `questoes_extraidas_page_*.json`
- **JSON combinado**: Arquivo `questoes_extraidas_completas.json` com todas as questões
- **Dados limpos**: Arquivo `questoes_limpas.json` com dados processados

## 🔍 Estrutura HTML Analisada

O scraper identifica:

- **Questões**: `<div class="js-question-item q-question-item">`
- **Números**: `<span class="q-index js-question-index visible">`
- **Enunciados**: `<div class="q-question-enunciation">`
- **Tópicos**: `<div class="q-question-breadcrumb">` com `<a class="q-link">`

## 📈 Exemplo de Uso

```python
from scraper_questoes import extrair_questoes

# Ler um arquivo HTML específico
with open('html_pages/page_001.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extrair questões
questoes = extrair_questoes(html_content)

# Processar dados
for questao in questoes:
    print(f"Questão {questao['numero']}: {questao['enunciado'][:100]}...")
    print(f"Tópicos: {', '.join(questao['topicos'])}")
```

## 🚨 Considerações Importantes

- **Tempo de execução**: O processo pode demorar dependendo do número de páginas
- **Conexão com internet**: Requer conexão estável durante o scraping
- **Recursos**: Pode consumir memória com muitas páginas
- **Rate limiting**: Respeita delays entre requisições para não sobrecarregar o servidor

## 🔧 Tecnologias Utilizadas

- **Python 3.11**
- **Selenium** - Automação de navegador
- **BeautifulSoup4** - Parsing HTML
- **lxml** - Parser XML/HTML
- **JSON** - Formato de saída

## 📝 Logs e Debug

O sistema gera logs detalhados durante a execução:

- Progresso de cada página
- Questões extraídas por página
- Erros e avisos
- Estatísticas finais

## 🎉 Status do Projeto

✅ **Funcionalidades implementadas:**
- Scraping de múltiplas páginas
- Salvamento de HTMLs
- Extração de questões
- Processamento de dados
- Combinação de resultados
- Testes automatizados
- Documentação completa 