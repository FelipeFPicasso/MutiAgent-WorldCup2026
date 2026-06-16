# Multi Agent World Cup 2026

## Sobre o Projeto

O Assistente Multiagente da Copa do Mundo 2026 é um sistema de Inteligência Artificial desenvolvido para responder perguntas sobre a história das Copas do Mundo, seleções, jogadores, estádios e estatísticas históricas.

O projeto utiliza uma arquitetura multiagente baseada em LLMs locais executados via Ollama, combinada com técnicas de Retrieval-Augmented Generation (RAG), banco vetorial e ferramentas especializadas para fornecer respostas contextualizadas e fundamentadas em dados.

---

## Arquitetura do Sistema

O sistema é composto por quatro componentes principais:

### Orchestrator Agent

Responsável por coordenar o fluxo de execução, distribuir tarefas entre os agentes especializados e consolidar os resultados.

### Scout Agent

Especializado na recuperação de informações históricas através do mecanismo RAG e da base vetorial.

### Tactical Agent

Responsável pela análise de dados, cálculos estatísticos e utilização das ferramentas especializadas.

### Narrator Agent

Gera a resposta final em linguagem natural utilizando o contexto produzido pelos demais agentes.

---

## Tecnologias Utilizadas

* Python 3
* Ollama
* LLaMA 3.2 (modelo local)
* ChromaDB
* Sentence Transformers
* RAG (Retrieval-Augmented Generation)
* MCP (implementação acadêmica simplificada)
* Colorama
* Requests

---

## Funcionalidades

### Base de Conhecimento Vetorial (RAG)

O sistema utiliza documentos históricos sobre a Copa do Mundo que são transformados em embeddings e armazenados no ChromaDB para recuperação semântica.

### Dataset Estruturado

As informações históricas são carregadas a partir de um dataset JSON contendo:

* Países campeões
* Títulos por seleção
* Artilheiros históricos
* Estádios da Copa de 2026
* Conquistas por edição
* Estatísticas históricas

Eliminando a necessidade de dados "chumbados" diretamente no código.

### Ferramentas Especializadas

#### Busca na Base de Conhecimento

Recupera informações relevantes da base vetorial utilizando similaridade semântica.

#### Probabilidade de Vitória

Calcula probabilidades simplificadas com base no histórico de títulos das seleções.

#### Filtros Estatísticos

Permite consultar:

* Campeões mundiais
* Maiores artilheiros
* Estádios da Copa 2026

---

## MCP Simplificado

O projeto implementa uma camada de comunicação inspirada nos princípios do Model Context Protocol (MCP), utilizando mensagens padronizadas entre os agentes por meio de:

* MCPMessage
* MCPResponse
* MCPBus

Embora não utilize uma implementação oficial do protocolo MCP, a solução adota seus conceitos fundamentais de troca estruturada de contexto e coordenação entre agentes.

---

## Execução Local

Diferentemente de soluções dependentes exclusivamente de APIs externas, este projeto executa modelos de linguagem localmente através do Ollama.

Exemplo de modelo utilizado:

* llama3.2:3b

Isso permite:

* Funcionamento offline após instalação do modelo
* Menor dependência de serviços externos
* Maior controle sobre os dados processados
* Redução de custos operacionais

---

## Fluxo de Funcionamento

1. O usuário envia uma pergunta pelo terminal.
2. O Orchestrator recebe a solicitação.
3. O Scout Agent recupera contexto relevante via RAG.
4. O Tactical Agent executa análises e ferramentas especializadas.
5. O Narrator Agent gera a resposta final.
6. A resposta é apresentada ao usuário.

---

## Exemplos de Perguntas

* Qual é o histórico do Brasil na Copa do Mundo?
* Quem são os maiores artilheiros da história?
* Quais serão os estádios da Copa 2026?
* Qual a probabilidade de o Brasil vencer a Argentina?
* Como foi a final da Copa do Mundo de 2022?
* Quantos títulos a Alemanha possui?

---

## Objetivo Acadêmico

Este projeto foi desenvolvido para demonstrar a integração de:

* Sistemas Multiagentes
* Modelos de Linguagem de Grande Escala (LLMs)
* Retrieval-Augmented Generation (RAG)
* Bancos Vetoriais
* Ferramentas Especializadas
* Comunicação baseada em MCP

aplicados ao domínio histórico e estatístico da Copa do Mundo FIFA.

----
## Instalação e execução:

### Instalação
1.  Clonar o repositório -> https://github.com/FelipeFPicasso/MutiAgent-WorldCup2026.git

2. Criar Ambiente Virtual:
    * Linux/macOS:

        python3 -m venv venv
        source venv/bin/activate

    * Windows:

        python -m venv venv venv\Scripts\activate

3. Instalar Dependências:

    * pip install -r requirements.txt

4. Instalar o Ollama:

    * Baixe e instale o Ollama -> https://ollama.com


    * Verifique a instalação -> ollama - - version

5. Baixar o Modelo Local:

    * O projeto foi configurado para utilizar o modelo -> ollama pull llama3.2:3b

    * Verifique se o modelo foi instalado -> ollama list

    * Saída esperada:

        *   NAME
            llama3.2:3b

### Execução:
    
1. Iniciar o Ollama (Terminal) -> ollama serve
2. Executar o Assistente

    Na pasta raiz do projeto (terminal) -> python3 main.py ou python main.py
-----
## Desenvolvedores:

* Felipe Frantz Picasso -> https://github.com/FelipeFPicasso
* Guilherme Reginato da Silva -> https://github.com/Guilherme196928 
