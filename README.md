# ⚽ Assistente Multiagente — Copa do Mundo 2026

Sistema multiagente baseado em LLMs para responder perguntas sobre a Copa do Mundo 2026, utilizando RAG, embeddings, MCP e modelo LLaMA 3.

---

## 👥 Integrantes

- Nome 1
- Nome 2
- Nome 3
- Nome 4

---

## 🎯 Problema escolhido

Torcedores e curiosos têm dificuldade em encontrar informações consolidadas sobre a Copa do Mundo 2026 — histórico de seleções, estatísticas, estádios e probabilidades — de forma rápida e contextualizada. O assistente resolve isso com agentes especializados que cooperam para entregar respostas completas e empolgantes via terminal.

---

## 🏗️ Arquitetura multiagente

```
Usuário (terminal)
       ↓
Agente Orquestrador   ← coordena via MCP
   ↙       ↓       ↘
Scout   Tático   Narrador
   ↘       ↓       ↙
  Base Vetorial (ChromaDB)
       ↓
  Tools (busca, stats, probabilidade)
       ↓
  LLaMA 3 via Groq API
```

---

## 🤖 Papel de cada agente

| Agente | Responsabilidade |
|---|---|
| **Orquestrador** | Recebe a pergunta, coordena os agentes via MCP e consolida a resposta |
| **Scout** | Busca informações relevantes na base vetorial via RAG |
| **Tático** | Analisa confrontos, formações e probabilidades usando tools |
| **Narrador** | Transforma os dados em resposta empolgante no estilo locutor esportivo |

---

## 🛠️ Tools disponíveis

- `search_knowledge_base(query)` — busca semântica na base vetorial
- `calculate_win_probability(team_a, team_b)` — estima probabilidade baseada em histórico
- `filter_stats(category)` — retorna estatísticas filtradas (artilheiros, campeões, estádios)

---

## 🔗 Como o MCP foi utilizado

O **Model Context Protocol (MCP)** foi implementado como um barramento de mensagens (`MCPBus`) que:
- Registra cada agente com um nome único
- Roteia mensagens tipadas (`MCPMessage`) entre agentes
- Retorna respostas padronizadas (`MCPResponse`) com status e resultado
- Mantém log de todas as interações para rastreabilidade

---

## 📚 Estratégia de RAG

1. Documentos `.txt` da base de conhecimento são carregados e divididos em parágrafos
2. Cada parágrafo é convertido em embedding com `sentence-transformers`
3. Os embeddings são indexados no ChromaDB (banco vetorial persistente)
4. Na consulta, a pergunta do usuário é convertida em embedding e os trechos mais similares são recuperados
5. O contexto recuperado é injetado no prompt do agente Scout

---

## 🗃️ Base de conhecimento

Arquivos `.txt` em `data/knowledge_base/` contendo:
- Histórico completo de todas as Copas do Mundo
- Estatísticas de artilheiros e campeões
- Informações sobre os estádios da Copa 2026
- Confrontos históricos entre seleções
- Perfil de jogadores e seleções favoritas

---

## 🧠 Tecnologias de embeddings e armazenamento vetorial

- **Embeddings:** `sentence-transformers` — modelo `all-MiniLM-L6-v2`
- **Armazenamento vetorial:** `ChromaDB` — banco vetorial local persistente

---

## 🤖 Modelo local utilizado

- **Modelo:** LLaMA 3 (8B parâmetros) — modelo open-source da Meta
- **Execução:** via [Groq API](https://console.groq.com) (inferência gratuita de modelos open-source)
- **Justificativa:** o Groq executa LLaMA 3 localmente em hardware especializado, disponibilizando o modelo open-source via API gratuita, o que permite uso em qualquer ambiente sem GPU dedicada

---

## 📦 Dependências

```
groq==0.9.0
chromadb==0.5.0
sentence-transformers==3.0.1
colorama==0.4.6
python-dotenv==1.0.1
requests==2.32.3
```

---

## 🚀 Instalação e execução

### Pré-requisitos

- Python 3.10 ou superior
- Conta gratuita no [Groq Console](https://console.groq.com) para obter a API key

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/copa2026-multiagente
cd copa2026-multiagente

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a chave da API
copy .env.example .env
# Edite o arquivo .env e insira sua GROQ_API_KEY

# 5. Execute o assistente
python main.py
```

---

## 💬 Exemplos de uso no terminal

```
⚽ Você: Qual é o histórico do Brasil na Copa do Mundo?

[Orquestrador] Processando: 'Qual é o histórico do Brasil na Copa do Mundo?'
  [Scout] Buscando na base vetorial...
  [Tático] Analisando dados táticos...
  [Narrador] Gerando resposta final...

🎙️ Resposta:

QUE HISTÓRIA INCRÍVEL! ⚽🏆 O Brasil é o maior vencedor da Copa do
Mundo com 5 títulos conquistados...
```

```
⚽ Você: Qual a probabilidade de Brasil vencer a Argentina?

🎙️ Resposta:

O CLÁSSICO DAS AMÉRICAS! ⚽🔥 Baseado no histórico de títulos...
```

---

## 📁 Estrutura do projeto

```
copa2026-multiagente/
├── agents/
│   ├── orchestrator.py   # Agente orquestrador
│   ├── scout.py          # Agente de busca RAG
│   ├── tactical.py       # Agente de análise tática
│   └── narrator.py       # Agente narrador
├── rag/
│   └── retriever.py      # Embeddings e busca vetorial
├── tools/
│   └── tools.py          # Tools dos agentes
├── mcp/
│   └── protocol.py       # Barramento MCP
├── data/
│   └── knowledge_base/   # Documentos indexados
├── main.py               # Interface terminal
├── requirements.txt
├── .env.example
└── README.md
```
