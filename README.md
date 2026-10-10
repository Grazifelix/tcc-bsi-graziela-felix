# User Story & QUS Generator API

Uma API RESTful desenvolvida em **FastAPI** para automatizar o processo de engenharia de requisitos. Esta API recebe ficheiros de áudio (reuniões, entrevistas), realiza a transcrição, extrai **User Stories** com rastreabilidade (timestamps) e realiza uma análise de qualidade baseada no **QUS-Framework** (Quality User Story).

O projeto utiliza uma arquitetura flexível baseada no **Padrão Factory**, permitindo alternar facilmente entre diferentes provedores de LLM (como Google Gemini e Ollama local) sem necessidade de alterar o código principal.

## 🚀 Funcionalidades

*   **Transcrição de Áudio:** Utiliza `faster-whisper` para transcrever áudio com alta precisão e extrair timestamps.
*   **Geração de User Stories:** Analisa a transcrição e extrai histórias de utilizador seguindo padrões ágeis (BDD, critérios de aceite).
*   **Análise QUS-Framework:** Avalia as histórias geradas com base nos 13 critérios sintáticos, semânticos e pragmáticos definidos por Lucassen et al.
*   **Múltiplos LLMs:** Suporte nativo para **Ollama** (modelos locais) e **Google Gemini**, gerenciado via variáveis de ambiente.

## 📂 Estrutura do Projeto

```text
.
├── main.py                     # Ficheiro principal da API (Endpoints FastAPI)
├── config.py                   # Configurações globais
├── requirements.txt            # Dependências do projeto
├── .env                        # Variáveis de ambiente (não versionado)
├── services/
│   ├── transcriber.py          # Serviço de transcrição (Whisper)
│   └── llm/
│       ├── base_llm_provider.py # Interface abstrata (BaseLLMProvider)
│       ├── ollama_service.py    # Implementação para Ollama
│       ├── gemini_service.py    # Implementação para Google Gemini
│       ├── factory.py           # Factory (Registry Pattern) para instanciar os LLMs
│       └── user_story_pipeline.py # Lógica de negócio (Geração e Análise)
└── outputs/                    # Diretório de relatórios gerados (opcional)
```

## ⚙️ Pré-requisitos

*   **Python 3.9+**
*   **FFmpeg:** Necessário para o processamento de áudio do Whisper.
*   *(Opcional)* **Ollama:** Se pretender utilizar modelos locais (ex: `llama3.2:3b`). Instale em [ollama.com](https://ollama.com/).

## 🛠️ Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone <url-do-seu-repositorio>
   cd <nome-da-pasta>
   ```

2. **Crie um ambiente virtual e instale as dependências:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   pip install fastapi uvicorn pydantic python-multipart faster-whisper ollama google-genai
   ```

3. **Configuração das Variáveis de Ambiente:**
   Crie um ficheiro `.env` na raiz do projeto. Utilize o padrão Factory para definir qual LLM a API deve utilizar.

   *Exemplo para Google Gemini:*
   ```env
   LLM_PROVIDER=gemini
   GEMINI_MODEL=gemini-3.8-flash
   GEMINI_API_KEY=sua_chave_api_aqui
   ```

   *Exemplo para Ollama (Local):*
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.2:3b
   ```

## ▶️ Execução

Inicie o servidor FastAPI com recarregamento automático:

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

## 📡 Endpoints da API

Pode aceder à documentação interativa (Swagger UI) em **`http://127.0.0.1:8000/docs`**.

### 1. `POST /api/v1/transcribe`
Recebe um ficheiro de áudio e devolve a transcrição segmentada com timestamps.
*   **Input:** Ficheiro `multipart/form-data` (áudio).
*   **Output:** JSON com metadados, texto completo e segmentos.

### 2. `POST /api/v1/generate-user-stories`
Recebe o texto de uma transcrição e utiliza o LLM configurado para gerar as histórias e a análise QUS.
*   **Input:** JSON contendo o `transcript_text`.
*   **Output:** JSON contendo o array de `user_stories` e a `qus_analysis`.

### 3. `POST /api/v1/process-audio-pipeline`
Executa o fluxo completo em apenas uma chamada: Transcreve o áudio -> Gera User Stories -> Analisa via QUS.
*   **Input:** Ficheiro `multipart/form-data` (áudio).
*   **Output:** Relatório consolidado em JSON.