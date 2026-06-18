# mauboto 🤖

O **mauboto** é uma solução inteligente e customizada desenvolvida para o ecossistema "BIA do Futuro" (DIO). O projeto consiste em um agente conversacional integrado a uma interface interativa capaz de gerenciar e analisar dados familiares, transações financeiras e acompanhamento de contas fixas.

Este repositório reflete a implementação completa da solução, superando o template original do fork.

## 📁 Estrutura do Repositório

```text
├── data/                       # Base de dados estruturada do sistema
│   ├── configuracoes_familia.json
│   ├── contas_fixas.json
│   ├── transacoes.csv
│   └── historico_atendimento.csv
├── docs/                       # Documentação completa do desenvolvimento
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
├── src/                        # Código-fonte da aplicação
│   ├── app.py                  # Aplicação principal (Streamlit)
│   └── requirements.txt        # Dependências do projeto
└── assets/                     # Recursos visuais e roteiros de suporte
```

## 🚀 Tecnologias Utilizadas

* **Python 3** — Linguagem principal do ecossistema.
* **Streamlit** — Interface de usuário ágil e interativa.
* **Pandas** — Manipulação, filtragem e análise de dados estruturados.
* **Requests** — Integração de chamadas de API e comunicação do agente.

## 🛠️ Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/mauriciomcoutinho/dio-lab-bia-do-futuro.git
   cd dio-lab-bia-do-futuro/src
   ```

2. **Instale as dependências necessárias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie a aplicação local:**
   ```bash
   streamlit run app.py
   ```

## 📝 Documentação do Desenvolvimento

Toda a inteligência de negócios, governança e engenharia do **mauboto** está detalhada na pasta [`/docs`](./docs), contendo:
* **01-documentacao-agente.md**: Alinhamento estratégico e regras de negócio do assistente.
* **02-base-conhecimento.md**: Dados de contexto que alimentam o modelo.
* **03-prompts.md**: Engenharia de prompts e personas configuradas.
* **04-metricas.md**: KPIs, avaliação de desempenho e eficácia do chatbot.
* **05-pitch.md**: Visão de valor e apresentação comercial da solução.
