# Multi Agent World Cup 2026

## Integrantes da Equipe

* **Felipe Frantz Picasso**
  GitHub: https://github.com/FelipeFPicasso

* **Guilherme Reginato da Silva**
  GitHub: https://github.com/Guilherme196928

---

# Sobre o Projeto

O Assistente Multiagente da Copa do Mundo 2026 é um sistema de Inteligência Artificial desenvolvido para responder perguntas sobre a história das Copas do Mundo, seleções, jogadores, estádios, grupos da Copa de 2026 e estatísticas históricas.

O projeto utiliza uma arquitetura baseada em agentes especializados executando um modelo LLaMA local através do Ollama, juntamente com técnicas de Retrieval-Augmented Generation (RAG), banco vetorial e ferramentas especializadas para fornecer respostas contextualizadas.

---

# Problema Escolhido

A Copa do Mundo reúne uma grande quantidade de informações históricas e estatísticas. Consultar essas informações manualmente pode ser demorado, enquanto modelos de linguagem utilizados isoladamente podem gerar respostas incorretas ou sem embasamento.

Assim, o projeto busca unir recuperação de informações e inteligência artificial para fornecer respostas mais precisas e fundamentadas.

---

# Objetivo da Solução

Desenvolver um assistente inteligente capaz de responder perguntas sobre a Copa do Mundo utilizando:

* Arquitetura Multiagente;
* Modelos LLaMA executados localmente;
* Retrieval-Augmented Generation (RAG);
* Banco Vetorial;
* Ferramentas especializadas para consultas estatísticas.

---

# Arquitetura Multiagente

O sistema é composto por quatro agentes especializados:

```
Usuário
   │
   ▼
Orchestrator
   │
   ├────────────► Scout (RAG)
   │
   ├────────────► Tactical (Tools)
   │
   ▼
Narrator
   │
   ▼
Resposta Final
```

---

# Papel de Cada Agente

## Orchestrator Agent

Coordena toda a execução do sistema.

É responsável por:

* receber a pergunta do usuário;
* decidir quais agentes serão utilizados;
* distribuir as tarefas;
* reunir os resultados.

---

## Scout Agent

Responsável pela recuperação de informações utilizando RAG.

Suas funções são:

* consultar a base vetorial;
* recuperar documentos relevantes;
* enviar o contexto para os demais agentes.

---

## Tactical Agent

Executa análises especializadas utilizando ferramentas.

É responsável por:

* cálculos de probabilidade;
* consultas estatísticas;
* análises históricas;
* processamento de dados estruturados.

---

## Narrator Agent

Recebe todas as informações produzidas pelos demais agentes e gera uma resposta final em linguagem natural utilizando o modelo LLaMA executado localmente.

---

# Ferramentas Disponíveis

O projeto possui três ferramentas principais.

## search_knowledge_base()

Realiza busca semântica na base vetorial utilizando embeddings.

Utilizada pelo Scout Agent.

---

## calculate_win_probability()

Calcula uma probabilidade simplificada baseada no histórico de títulos das seleções.

Exemplo:

* Brasil × Argentina

---

## filter_stats()

Consulta informações estruturadas do dataset.

Permite responder perguntas sobre:

* Campeões;
* Artilheiros;
* Títulos;
* Estádios da Copa 2026.

---

# Como o MCP foi Utilizado

O projeto implementa uma versão simplificada do Model Context Protocol (MCP).

A comunicação entre os agentes ocorre através de mensagens padronizadas utilizando:

* MCPMessage
* MCPResponse
* MCPBus

O Orchestrator envia mensagens aos agentes especializados, que processam a solicitação e retornam respostas estruturadas.

Essa abordagem facilita a coordenação entre agentes e separa claramente as responsabilidades de cada componente.

---

# Estratégia de RAG

A estratégia utilizada segue as seguintes etapas:

1. Leitura dos arquivos TXT da base de conhecimento.
2. Divisão dos documentos em pequenos trechos (chunks).
3. Geração dos embeddings utilizando Sentence Transformers.
4. Armazenamento dos vetores no ChromaDB.
5. Busca semântica dos trechos mais relevantes.
6. Envio do contexto recuperado ao modelo LLaMA para geração da resposta.

---

# Base de Conhecimento

A base de conhecimento foi construída especificamente para este projeto.

Ela é composta por documentos TXT contendo informações sobre:

* História das Copas do Mundo;
* Campeões mundiais;
* Artilheiros históricos;
* Estádios da Copa de 2026;
* Grupos da Copa de 2026;
* Informações gerais da Copa de 2026.

Além disso, o projeto utiliza um dataset JSON contendo informações estruturadas como títulos, campeões, artilheiros e estádios, permitindo consultas rápidas sem necessidade de recuperação vetorial.

---

# Embeddings e Armazenamento Vetorial

## Modelo de Embeddings

```
sentence-transformers
all-MiniLM-L6-v2
```

## Banco Vetorial

```
ChromaDB
```

Os embeddings representam semanticamente os documentos da base de conhecimento, permitindo recuperar informações relevantes mesmo quando a pergunta utiliza palavras diferentes das presentes no texto original.

---

# Modelo Local Utilizado

O sistema utiliza o modelo:

```
llama3.2:3b
```

executado localmente através do Ollama.

Essa abordagem permite:

* funcionamento offline após instalação do modelo;
* menor dependência de APIs externas;
* maior controle sobre os dados processados;
* redução de custos operacionais.

---

# Tecnologias Utilizadas

* Python 3
* Ollama
* LLaMA 3.2
* ChromaDB
* Sentence Transformers
* Transformers
* Torch
* RAG
* MCP
* Requests
* Colorama

---

# Estrutura do Projeto

```
MultiAgent-WorldCup2026/
│
├── agents/
│   ├── orchestrator.py
│   ├── scout.py
│   ├── tactical.py
│   └── narrator.py
│
├── rag/
│   ├── retriever.py
│   └── __init__.py
│
├── tools/
│
├── mcp/
│
├── data/
│   ├── knowledge_base/
│   ├── copa_dataset.json
│   └── chroma_db/
│
├── llm_client.py
├── main.py
└── requirements.txt
```

---

# Dependências

```
groq==0.9.0
chromadb==0.5.0
sentence-transformers==3.0.1
transformers==4.41.2
torch
python-dotenv==1.0.1
requests==2.32.3
colorama==0.4.6
```

---

# Instalação

## Clonar o Repositório

```bash
git clone https://github.com/FelipeFPicasso/MutiAgent-WorldCup2026.git

cd MutiAgent-WorldCup2026
```

---

# Ubuntu / Linux

## Criar ambiente virtual

```bash
python3 -m venv .venv

source .venv/bin/activate
```

## Atualizar pip

```bash
pip install --upgrade pip
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Instalar Ollama

https://ollama.com

Verificar instalação:

```bash
ollama --version
```

## Baixar o modelo

```bash
ollama pull llama3.2:3b
```

---

# Windows

## Criar ambiente virtual

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Caso a execução de scripts esteja bloqueada:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Atualizar pip

```powershell
python -m pip install --upgrade pip
```

## Instalar dependências

```powershell
pip install -r requirements.txt
```

## Instalar Ollama

https://ollama.com/download

Verificar:

```powershell
ollama --version
```

## Baixar o modelo

```powershell
ollama pull llama3.2:3b
```

---

# Execução

## Iniciar o Ollama

```bash
ollama serve
```

## Executar o projeto

Linux

```bash
python3 main.py
```

Windows

```powershell
python main.py
```

---

# Exemplo de Execução

```text
$ python main.py

    ASSISTENTE MULTIAGENTE — COPA DO MUNDO 2026
  Powered by LLaMA (local via Ollama) · RAG · MCP · Agentes Especializados
=======================================================

[Sistema] Pronto! Digite sua pergunta sobre a Copa 2026.

Exemplos de perguntas:
 • Qual é o histórico do Brasil na Copa do Mundo?
 • Quem são os maiores artilheiros da história?
 • Quais são os estádios da Copa 2026?
 • Qual a probabilidade de Brasil vencer a Argentina?
 • Como foi a final da Copa 2022?
 • Quantos títulos a Alemanha tem?

Comandos:
 • ajuda
 • sair
```

## Exemplo 1

```text
Você: Qual país possui mais títulos?

[Orquestrador] Dados estruturados encontrados — bypassing RAG.
[Narrador] Gerando resposta final...

Resposta:

O Brasil possui o maior número de títulos da Copa do Mundo, com cinco conquistas.
```

---

## Exemplo 2

```text
Você: A Argentina tem quantos títulos?

[Orquestrador] Dados estruturados encontrados — bypassing RAG.
[Narrador] Gerando resposta final...

Resposta:

A Argentina possui três títulos mundiais, conquistados em 1978, 1986 e 2022.
```

---

## Exemplo 3

```text
Você: Quantos gols o Mbappé tem na Copa?

[Scout] Buscando na base vetorial...
[Tático] Analisando dados...
[Narrador] Gerando resposta final...

Resposta:

Kylian Mbappé marcou 12 gols em Copas do Mundo, participando das edições de 2018 e 2022.
```

---

# Objetivo Acadêmico

Este projeto foi desenvolvido para demonstrar a integração entre:

* Sistemas Multiagentes;
* Modelos de Linguagem (LLMs);
* Retrieval-Augmented Generation (RAG);
* Banco Vetorial;
* Embeddings;
* Ferramentas Especializadas;
* Comunicação inspirada no Model Context Protocol (MCP).

A solução demonstra como diferentes agentes especializados podem cooperar para produzir respostas contextualizadas e fundamentadas utilizando um modelo de linguagem executado localmente.
