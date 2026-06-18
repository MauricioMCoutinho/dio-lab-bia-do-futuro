import json
import streamlit as st
import pandas as pd
import requests

# =========== CONFIGURAÇÃO =========== #

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3"

# ========== CARREGAR DADOS ========== #

configuracoes = json.load(open("data/configuracoes_familia.json"))
contas_fixas = json.load(open("data/contas_fixas.json"))
historico = pd.read_csv("data/historico_atendimento.csv")
transacoes = pd.read_csv("data/transacoes.csv")

# ========== CALCULAR SOBRA-========== #

total_contas_fixas = sum(conta["valor_estimado"] for conta in contas_fixas)
total_gastos_csv = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()

# Cálculo final da sobra
sobra_real = configuracoes["renda_mensal_total"] - total_contas_fixas - total_gastos_csv

# ============= CONTEXTO ============= #

contexto = f"""
FAMÍLIA: {configuracoes['familia']}
RENDA MENSAL TOTAL: R$ {configuracoes['renda_mensal_total']:.2f}
SOBRA REAL ATUAL DO ORÇAMENTO: R$ {sobra_real:.2f}
DIA DE FECHAMENTO: {configuracoes['dia_fechamento']}

LIMITES MENSAIS:

- Alimentação: R$ {configuracoes['limites_mensais']['alimentacao']:.2f}
- Lazer: R$ {configuracoes['limites_mensais']['lazer']:.2f}
- Transporte: R$ {configuracoes['limites_mensais']['transporte']:.2f}

TRANSAÇÕES RECENTES:{transacoes.to_string(index=False)}
ATENDIMENTOS ANTERIORES:{historico.to_string(index=False)}
CONTAS FIXAS CADASTRADAS:{json.dumps(contas_fixas, indent=2, ensure_ascii=False)}
"""

# ========== SYSTEM PROMPT ========== #

system_prompt = """Você é o Mauboto, Co-Piloto Financeiro focado exclusivamente em fluxo de caixa e previsão de saldo familiar.
OBJETIVO:
Auxiliar a família a entender suas finanças, identificar oportunidades de economia e garantir que o saldo bancário nunca fique negativo.

REGRAS:

1. Responda única e exclusivamente com os dados injetados no contexto. Nunca invente valores ou transações.
2. O arquivo de configurações contém apenas LIMITES (tetos máximos permitidos). Para responder "Quanto gastei", use APENAS o histórico de transações reais e registros de gastos confirmados no chat. Nunca some limites aos gastos reais.
3. Se a pergunta for sobre o GASTO ATUAL de uma categoria específica, responda apenas o total somado daquela categoria. Deixe a fórmula de fechamento do mês (Entradas - Contas Fixas - Gastos) EXCLUSIVAMENTE para perguntas sobre a "previsão do saldo final" ou "fechamento do mês".
4. Para previsões de fechamento, considere apenas receitas fixas confirmadas. Se faltar o valor de uma conta futura mencionada, peça o valor exato ou o teto máximo previsto antes de recalcular a projeção. Não tente adivinhar.
5. Emita um alerta imediato e sugira contenção se:
   - Um único gasto passar de 10% da renda mensal.
   - Uma categoria atingir/ultrapassar a zona de perigo configurada.
   - A projeção de saldo final do mês ficar negativa.
6. Você não faz transações, não opina sobre impostos e está proibido de recomendar investimentos. Se questionado sobre onde investir, decline educadamente e indique a busca por um especialista. Se o saldo ou a sobra real do mês atual estiverem calculados no contexto, mostre-os em **negrito** (ex: "Sua sobra atual é de **R$ X**"). Caso contrário, apenas decline educadamente sem exibir valores zerados.
7. Suas respostas devem ser extremamente diretas, escaneáveis, com valores e categorias em **negrito**, e limite máximo de 3 parágrafos.
8. Ao colocar valores em negrito, certifique-se de aplicar os asteriscos CORRETAMENTE envolvendo todo o termo, exatamente assim: **R$ 720,00** (nunca faça R **720 ou **R$**720).
9. Aplique o negrito apenas em valores e nos nomes das categorias.
"""

# ========== CHAMAR OLLAMA ========== #


def perguntar(msg):
    prompt = f"""
    {system_prompt}
    CONTEXTO DO CLIENTE:
    {contexto}
    PERGUNTA: {msg}"""

    try:
        # Usamos o endpoint padrão que casa perfeitamente com a estrutura do seu código original
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=60,
        )

        dados_resposta = r.json()

        # Tentativa 1: Formato padrão (/api/generate)
        if "response" in dados_resposta and dados_resposta["response"].strip():
            return dados_resposta["response"]

        # Tentativa 2: Formato de Chat (/api/chat) caso mude a URL depois
        elif "message" in dados_resposta and "content" in dados_resposta["message"]:
            return dados_resposta["message"]["content"]

        # Tentativa 3: Se o Ollama avisar algum erro interno
        elif "error" in dados_resposta:
            return f"❌ Erro do Ollama: {dados_resposta['error']}"

        else:
            return f"⚠️ O modelo processou, mas não retornou texto. Resposta bruta: {dados_resposta}"

    except Exception as e:
        return f"💥 Erro ao conectar com o modelo: {str(e)}"


# =========== INTERFACE =========== #

st.title("Mauboto - Co-Piloto Financeiro")

if pergunta := st.chat_input(
    "Faça uma pergunta sobre o fluxo de caixa ou previsão de saldo:"
):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
