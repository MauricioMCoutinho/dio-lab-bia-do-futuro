# Passo a Passo de Execução

## Setup Ollama

```bash
# 1. Instalar Ollama (ollama.ai)
# 2. Baixar um modelo leve
ollama pull llama3

#3.Testar se funciona
ollama run llama3 "Olá!"
```

## Código completo
todo o código fonte está no arquivo `app.py`

## Requirements

todos os requirements no arquivo `requirements.txt`

## Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Garantir que o Ollama está rodando
ollama serve

# 3. Rodar a aplicação
python -m streamlit run src/app.py
```
