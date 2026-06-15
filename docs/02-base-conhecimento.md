# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta [`data`](../data), por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| [`historico_atendimento.csv`](../data/historico_atendimento.csv) | CSV | Registrar o log das conversas do chat com os membros da família para garantir contexto contínuo nas interações. |
| [`configuracoes_familia.json`](../data/configuracoes_familia.json) | JSON | Definir a renda mensal da casa, dia de fechamento e os limites de teto por categoria para os alertas. |
| [`contas_fixas.json`](../data/contas_fixas.json) | JSON | Listar as despesas recorrentes (aluguel, contas de consumo, assinaturas) para calcular a previsão do saldo futuro. |
| [`transacoes.csv`](../data/transacoes.csv) | CSV | Registrar e analisar o fluxo de caixa real (entradas e saídas diárias) da família para projetar o saldo final. |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados originais, que eram focados em uma corretora de investimentos, foram totalmente reestruturados para refletir a rotina de um orçamento doméstico:
* **`perfil_investidor.json`** virou **`configuracoes_familia.json`**: Removemos dados de risco e patrimônio e inserimos as regras do jogo da família (renda mensal, dia de fechamento do mês e limites de gastos por categoria).
* **`produtos_financeiros.json`** virou **`contas_fixas.json`**: Excluímos os investimentos (CDB, Tesouro) e substituímos por despesas recorrentes (Aluguel, Luz, Internet) para viabilizar as projeções matemáticas do saldo.
* **`historico_atendimento.csv`**: Foi adaptado para funcionar como um log de conversas de chat (quem falou, o que foi dito, e como o agente respondeu), permitindo que o bot mantenha o contexto do papo com a família.
* **`transacoes.csv`**: A estrutura foi mantida, mas os dados fictícios foram atualizados para simular saídas comuns de uma casa (supermercado, farmácia, assinaturas de streaming).

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo: 

```Python
import json
import pandas as pd

configuracoes = json.load(open("data/configuracoes_familia.json"))
contas_fixas = json.load(open("data/contas_fixas.json"))
historico = pd.read_csv("data/historico_atendimento.csv")
transacoes = pd.read_csv("data/transacoes.csv")
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

A injeção é dividida em duas partes para otimizar o processamento:
1. **System Prompt (Estático):** Recebe as informações do `configuracoes_familia.json` e `contas_fixas.json`, pois são as regras imutáveis do mês, orientando como o agente deve se comportar e calcular as previsões.
2. **Contexto Dinâmico:** As informações de `transacoes.csv` e o histórico recente do chat são injetados na janela de contexto de acordo com as interações mais recentes, evitando sobrecarregar o prompt com gastos de meses anteriores que não afetam a projeção atual.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```text
[Configurações da Família]
- Família: Silva
- Renda Mensal Declarada: R$ 8.000,00
- Dia de Fechamento: 30
- Limites Mensais: Alimentação (R$ 2.000,00), Lazer (R$ 500,00)

[Contas Fixas Previstas]
- Aluguel: R$ 1.500,00 (Vence dia 05)
- Conta de Luz: R$ 200,00 (Valor estimado, Vence dia 15)

[Últimas Transações Registradas]
- 10/06: Supermercado - Saída - R$ 150,00 (Alimentação)
- 11/06: Uber - Saída - R$ 45,00 (Transporte)
- 12/06: Netflix - Saída - R$ 55,90 (Lazer)

[Últimas Interações no Chat]
- Pai (11/06 14:15): Como vamos fechar o mês?
- Co-Piloto (11/06 14:15): Pelos meus cálculos, vamos fechar com R$ 300 sobrando. Pode seguir viagem!
- Filho (12/06 18:20): Queria comprar um jogo de 200 reais hoje.
