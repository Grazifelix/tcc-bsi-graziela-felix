import json
from services.llm.llm_factory import get_llm_provider

class UserStoryPipeline:
    def __init__(self):
        # Carrega dinamicamente o LLM configurado
        self.llm = get_llm_provider()

    def generate_user_stories(self, transcript_text: str) -> dict:
        prompt = f"""
Você é um Product Owner especialista em metodologias ágeis.
Análise a transcrição e extraia uma lista de User Stories com timestamps de rastreabilidade.

FORMATO DA RESPOSTA: Retorne EXCLUSIVAMENTE um objeto JSON válido:
{{
  "user_stories": [
    {{
      "id": "US001",
      "titulo": "Título",
      "user_story": "Como [usuário], eu quero [funcionalidade] para que [benefício].",
      "criterios_aceite": ["Dado que...", "Quando...", "Então..."],
      "rastreabilidade": {{
        "timestamp_inicio": "00:00:00",
        "timestamp_fim": "00:00:00",
        "trecho_citado": "Trecho falado"
      }}
    }}
  ]
}}

TRANSCRIÇÃO:
{transcript_text}
"""
        return self.llm.generate_json(prompt)

    def analyze_qus(self, user_stories_data: dict) -> dict:
        prompt = f"""
Você é um Revisor de Requisitos especialista no Quality User Story (QUS) Framework.
Avalie as User Stories de acordo com os critérios do QUS Framework.

FORMATO DA RESPOSTA: Retorne EXCLUSIVAMENTE um objeto JSON válido:
{{
  "resumo_backlog": {{ "total_historias": 0, "padroes_defeitos": [], "lacunas_provaveis": [] }},
  "analise_individual": [],
  "analise_transversal_conjunto": {{}}
}}

USER STORIES:
{json.dumps(user_stories_data, ensure_ascii=False, indent=2)}
"""
        return self.llm.generate_json(prompt)

# import json
# import ollama

# class UserStoryPipeline:
#     def __init__(self, model_name="llama3.2:3b"):
#         self.model_name = model_name

#     def generate_user_stories(self, transcript_text):
#         print("\n🤖 1. Gerando User Stories com o Ollama...")
        
#         prompt_content = f"""
# Você é um Product Owner / Analista de Requisitos especialista em metodologias ágeis. 

# Sua tarefa é analisar a transcrição de uma conversa fornecida abaixo e extrair uma lista de User Stories de alta qualidade, garantindo a rastreabilidade exata de onde cada requisito foi mencionado através dos timestamps.

# ---

# ### FORMATO DA RESPOSTA:
# Retorne EXCLUSIVAMENTE um objeto JSON válido (sem markdown ou conversas adicionais):

# {{
#   "user_stories": [
#     {{
#       "id": "US001",
#       "titulo": "Título sucinto da história",
#       "user_story": "Como [usuário], eu quero [funcionalidade] para que [benefício].",
#       "criterios_aceite": [
#         "Dado que...",
#         "Quando...",
#         "Então..."
#       ],
#       "rastreabilidade": {{
#         "timestamp_inicio": "00:00:00",
#         "timestamp_fim": "00:00:00",
#         "trecho_citado": "Trecho exato falado"
#       }}
#     }}
#   ]
# }}

# ---

# ### TRANSCRIÇÃO DA CONVERSA:
# {transcript_text}
# """

#         response = ollama.chat(
#             model=self.model_name,
#             messages=[{"role": "user", "content": prompt_content}],
#             format="json"
#         )
#         return json.loads(response["message"]["content"])

#     def analyze_qus(self, user_stories_data):
#         print("\n🔍 2. Avaliando User Stories conforme o QUS-Framework...")

#         prompt_qus = f"""
# Você é um Revisor de Requisitos Ágeis especialista no Quality User Story (QUS) Framework de Lucassen et al.

# Sua tarefa é avaliar as User Stories fornecidas de acordo com os 13 critérios do QUS Framework:
# - Sintáticos (Individuais): Well-formed, Atomic, Minimal
# - Semânticos (Individuais): Conceptually sound, Problem-oriented, Unambiguous
# - Pragmáticos (Individuais): Full sentence, Estimatable
# - Conjunto (Backlog): Conflict-free, Unique, Uniform, Independent, Complete

# ---

# ### REGRAS DE AVALIAÇÃO:
# Para cada critério de cada história, atribua um dos estados: "Atende", "Viola", "Atenção" ou "Não avaliável".
# Forneça evidência textual e uma recomendação/reescrita caso haja violação.

# ---

# ### FORMATO DA RESPOSTA:
# Retorne EXCLUSIVAMENTE um objeto JSON válido no seguinte formato:

# {{
#   "resumo_backlog": {{
#     "total_historias": 0,
#     "padroes_defeitos": ["..."],
#     "lacunas_provaveis": ["..."]
#   }},
#   "analise_individual": [
#     {{
#       "id": "US001",
#       "user_story_original": "Como...",
#       "avaliacao_criterios": {{
#         "well_formed": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
#         "atomic": {{"resultado": "Viola", "evidencia": "...", "acao": "..."}},
#         "minimal": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
#         "conceptually_sound": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
#         "problem_oriented": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
#         "unambiguous": {{"resultado": "Atenção", "evidencia": "...", "acao": "..."}},
#         "full_sentence": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
#         "estimatable": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}}
#       }},
#       "reescrita_sugerida": "Caso necessário, apresente a versão corrigida (ou separada se violar Atomic)."
#     }}
#   ],
#   "analise_transversal_conjunto": {{
#     "conflict_free": {{"resultado": "Atende", "observacao": "..."}},
#     "unique": {{"resultado": "Atende", "observacao": "..."}},
#     "uniform": {{"resultado": "Atende", "observacao": "..."}},
#     "independent": {{"resultado": "Atende", "observacao": "..."}},
#     "complete": {{"resultado": "Atenção", "observacao": "..."}}
#   }}
# }}

# ---

# ### USER STORIES PARA ANÁLISE:
# {json.dumps(user_stories_data, ensure_ascii=False, indent=2)}
# """

#         response = ollama.chat(
#             model=self.model_name,
#             messages=[{"role": "user", "content": prompt_qus}],
#             format="json"
#         )
#         return json.loads(response["message"]["content"])


# import json
# import ollama

# class UserStoryGenerator:
#     def __init__(self, model_name="llama3.2:3b"):
#         self.model_name = model_name

#     def generate_user_stories(self, transcript_text):
#         print("\n🤖 Analisando a transcrição e gerando User Stories com o Ollama...")
        
#         prompt_content = f"""
# Você é um Product Owner / Analista de Requisitos especialista em metodologias ágeis. 

# Sua tarefa é analisar a transcrição de uma conversa fornecida abaixo e extrair uma lista de User Stories de alta qualidade, garantindo a rastreabilidade exata de onde cada requisito foi mencionado na conversa através dos timestamps.

# ---

# ### DIRETRIZES DE QUALIDADE DAS USER STORIES:
# 1. **Estrutura Padrão:** Cada User Story deve seguir rigorosamente o formato: "Como [tipo de usuário], eu quero [ação/funcionalidade] para que [benefício/valor de negócio]".
# 2. **Critérios de Aceite:** Cada User Story deve conter Critérios de Aceite claros e testáveis no formato BDD (Dado que..., Quando..., Então...) ou em lista objetiva.
# 3. **Clareza e Concisão:** Evite dubiedades. Se a fala na transcrição for vaga, refine a User Story para torná-la acionável para o time de desenvolvimento.
# 4. **Rastreabilidade (Timestamps):** Indique o timestamp de início e fim (ou os timestamps específicos) onde essa necessidade foi discutida na transcrição.

# ---

# ### FORMATO DA RESPOSTA:
# Retorne EXCLUSIVAMENTE um objeto JSON válido (sem textos introdutórios ou explicativos antes ou depois do código JSON).

# Estrutura JSON esperada:
# {{
#   "user_stories": [
#     {{
#       "id": "US001",
#       "titulo": "Título sucinto da história",
#       "user_story": "Como [usuário], eu quero [funcionalidade] para que [benefício].",
#       "criterios_aceite": [
#         "Dado que...",
#         "Quando...",
#         "Então..."
#       ],
#       "rastreabilidade": {{
#         "timestamp_inicio": "00:00:00",
#         "timestamp_fim": "00:00:00",
#         "trecho_citado": "Transcrição exata ou aproximada do trecho relevante falado na conversa"
#       }}
#     }}
#   ]
# }}

# ---

# ### TRANSCRIÇÃO DA CONVERSA COM TIMESTAMPS:
# {transcript_text}
# """

#         response = ollama.chat(
#             model=self.model_name,
#             messages=[{"role": "user", "content": prompt_content}],
#             format="json"
#         )

#         content = response["message"]["content"]
#         return json.loads(content)

# # import json
# # import ollama

# # def load_transcript_for_prompt(json_filepath):
# #     """Lê o arquivo JSON da transcrição e formata os dados com timestamps."""
# #     with open(json_filepath, "r", encoding="utf-8") as f:
# #         data = json.load(f)

# #     # 1. Se o JSON já tiver o campo 'formatted_transcript', usa direto
# #     if "formatted_transcript" in data:
# #         return data["formatted_transcript"]

# #     # 2. Caso contrário, monta a string a partir do array 'segments'
# #     formatted_lines = []
# #     for segment in data.get("segments", []):
# #         start = segment["start"]
# #         end = segment["end"]
# #         text = segment["text"]
# #         formatted_lines.append(f"[{start}s -> {end}s] {text}")

# #     return "\n".join(formatted_lines)


# # # 1. Carrega e formata a transcrição do JSON
# # json_path = "transcription.json"
# # transcription_text = load_transcript_for_prompt(json_path)

# # # 2. Monta o prompt utilizando f-string (f""")
# # prompt_content = f"""
# # Você é um Product Owner / Analista de Requisitos especialista em metodologias ágeis. 

# # Sua tarefa é analisar a transcrição de uma conversa fornecida abaixo e extrair uma lista de User Stories de alta qualidade, garantindo a rastreabilidade exata de onde cada requisito foi mencionado na conversa através dos timestamps.

# # ---

# # ### DIRETRIZES DE QUALIDADE DAS USER STORIES:
# # 1. **Estrutura Padrão:** Cada User Story deve seguir rigorosamente o formato: "Como [tipo de usuário], eu quero [ação/funcionalidade] para que [benefício/valor de negócio]".
# # 2. **Critérios de Aceite:** Cada User Story deve conter Critérios de Aceite claros e testáveis no formato BDD (Dado que..., Quando..., Então...) ou em lista objetiva.
# # 3. **Clareza e Concisão:** Evite dubiedades. Se a fala na transcrição for vaga, refine a User Story para torná-la acionável para o time de desenvolvimento.
# # 4. **Rastreabilidade (Timestamps):** Indique o timestamp de início e fim (ou os timestamps específicos) onde essa necessidade foi discutida na transcrição.

# # ---

# # ### FORMATO DA RESPOSTA:
# # Retorne EXCLUSIVAMENTE um objeto JSON válido (sem textos introdutórios ou explicativos antes ou depois do código JSON).

# # Estrutura JSON esperada:
# # {{
# #   "user_stories": [
# #     {{
# #       "id": "US001",
# #       "titulo": "Título sucinto da história",
# #       "user_story": "Como [usuário], eu quero [funcionalidade] para que [benefício].",
# #       "criterios_aceite": [
# #         "Dado que...",
# #         "Quando...",
# #         "Então..."
# #       ],
# #       "rastreabilidade": {{
# #         "timestamp_inicio": "00:00:00",
# #         "timestamp_fim": "00:00:00",
# #         "trecho_citado": "Transcrição exata ou aproximada do trecho relevante falado na conversa"
# #       }}
# #     }}
# #   ]
# # }}

# # ---

# # ### TRANSCRIÇÃO DA CONVERSA COM TIMESTAMPS:
# # {transcription_text}
# # """

# # # 3. Chama o modelo no Ollama
# # response = ollama.chat(
# #     model="llama3.2:3b",
# #     messages=[
# #         {
# #             "role": "user",
# #             "content": prompt_content,
# #         },
# #     ],
# #     # Força a API do Ollama a retornar estritamente um JSON estruturado
# #     format="json"
# # )

# # # 4. Exibe o resultado enviado pelo modelo
# # print(response["message"]["content"])




# # import ollama

# # # Substitua 'llama3' pelo nome exato do modelo que você baixou no Ollama
# # response = ollama.chat(
# #     model="llama3.2:3b",
# #     messages=[
# #         {
# #             "role": "user",
# #             "content": 
# #             """
# # Você é um Product Owner / Analista de Requisitos especialista em metodologias ágeis. 

# # Sua tarefa é analisar a transcrição de uma conversa fornecida abaixo e extrair uma lista de User Stories de alta qualidade, garantindo a rastreabilidade exata de onde cada requisito foi mencionado na conversa através dos timestamps.

# # ---

# # ### DIRETRIZES DE QUALIDADE DAS USER STORIES:
# # 1. **Estrutura Padrão:** Cada User Story deve seguir rigorosamente o formato: "Como [tipo de usuário], eu quero [ação/funcionalidade] para que [benefício/valor de negócio]".
# # 2. **Critérios de Aceite:** Cada User Story deve conter Critérios de Aceite claros e testáveis no formato BDD (Dado que..., Quando..., Então...) ou em lista objetiva.
# # 3. **Clareza e Concisão:** Evite dubiedades. Se a fala na transcrição for vaga, refine a User Story para torná-la acionável para o time de desenvolvimento.
# # 4. **Rastreabilidade (Timestamps):** Indique o timestamp de início e fim (ou os timestamps específicos) onde essa necessidade foi discutida na transcrição.

# # ---

# # ### FORMATO DA RESPOSTA:
# # Retorne EXCLUSIVAMENTE um objeto JSON válido (sem textos introdutórios ou explicativos antes ou depois do código JSON).

# # Estrutura JSON esperada:

# # {
# #   "user_stories": [
# #     {
# #       "id": "US001",
# #       "titulo": "Título sucinto da história",
# #       "user_story": "Como [usuário], eu quero [funcionalidade] para que [benefício].",
# #       "rastreabilidade": {
# #         "timestamp_inicio": "00:00:00",
# #         "timestamp_fim": "00:00:00",
# #         "trecho_citado": "Transcrição exata ou aproximada do trecho relevante falado na conversa"
# #       }
# #     }
# #   ]
# # }

# # ---

# # ### TRANSCRIÇÃO DA CONVERSA COM TIMESTAMPS:

# # **Transcrição da Reunião de Alinhamento de Requisitos**

# # **Participantes:**

# # * **Carlos (Stakeholder):** Gerente de Operações da Empresa
# # * **Mariana (Analista de Requisitos):** Equipe de Tecnologia / Produto

# # ---

# # [00:00 - 00:25] **Mariana:** Bom dia, Carlos! Obrigado por reservar um tempo hoje. O objetivo desta reunião é entender melhor o que você precisa para o novo módulo de relatórios do sistema de vendas, para que possamos mapear os requisitos da melhor forma.

# # [00:25 - 00:58] **Carlos:** Bom dia, Mariana. O prazer é meu. Olha, a gente está com um gargalo enorme no final do mês. A equipe gasta horas consolidadas em planilhas do Excel para gerar o relatório de vendas por região. Eu preciso de algo no sistema que faça isso automaticamente e em tempo real.

# # [00:58 - 01:25] **Mariana:** Perfeito, entendi a dor principal. Quando você fala em relatório por região, quais informações específicas precisam ser exibidas? Estamos falando apenas do valor total de vendas ou precisamos detalhar por produto, vendedor ou categoria?

# # [01:25 - 02:05] **Carlos:** No nível executivo, eu preciso ver o total por região de forma simples. Mas os supervisores regionais vão usar o mesmo relatório, então eles precisam conseguir "clicar" na região e expandir para ver o detalhamento por vendedor e por linha de produto. Se puder ter um filtro de data customizável, seria ideal.

# # [02:05 - 02:40] **Mariana:** Excelente. Então temos um relatório com visão macro para diretoria e recurso de *drill-down* para os supervisores, com filtros por Período, Região, Vendedor e Categoria. Sobre a exportação desses dados, existe a necessidade de baixar isso em algum formato específico, como PDF ou Excel?

# # [02:40 - 03:10] **Carlos:** Com certeza. O pessoal de finanças sempre pede em Excel para cruzar com outros dados, e a diretoria prefere receber em PDF nas reuniões semanais. Então precisamos das duas opções de exportação.

# # [03:10 - 03:42] **Mariana:** Combinado, vou incluir a exportação em PDF e XLSX nos requisitos funcionais. Uma última dúvida sobre regras de acesso e segurança: qualquer usuário logado no sistema poderá ver o relatório completo de todas as regiões, ou deve haver restrição baseada no perfil?

# # [03:42 - 04:18] **Carlos:** Boa pergunta. Cada supervisor regional só deve enxergar os dados da sua própria região. Apenas a minha diretoria e a equipe financeira podem ter acesso à visão global de todas as regiões.

# # [04:18 - 04:45] **Mariana:** Anotado! Acesso restrito por perfil e escopo regional. Já tenho o suficiente para estruturar a primeira versão do documento de requisitos e as histórias de usuário. Até a próxima terça-feira eu te envio para validação e aprovação. Muito obrigada, Carlos!

# # [04:45 - 05:00] **Carlos:** Perfeito, Mariana! Muito obrigado pela agilidade. Fico no aguardo do documento. Bom trabalho!

# # """,
# #         },
# #     ],
# # )

# # print(response["message"]["content"])