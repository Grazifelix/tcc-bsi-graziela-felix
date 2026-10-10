import ollama

# Substitua 'llama3' pelo nome exato do modelo que você baixou no Ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": 
            """
Você é um Revisor de Requisitos Ágeis especialista no Quality User Story (QUS) Framework de Lucassen et al.

Sua tarefa é avaliar as User Stories fornecidas de acordo com os 13 critérios do QUS Framework:
- Sintáticos (Individuais): Well-formed, Atomic, Minimal
- Semânticos (Individuais): Conceptually sound, Problem-oriented, Unambiguous
- Pragmáticos (Individuais): Full sentence, Estimatable
- Conjunto (Backlog): Conflict-free, Unique, Uniform, Independent, Complete

---

### REGRAS DE AVALIAÇÃO:
Para cada critério de cada história, atribua um dos estados: "Atende", "Viola", "Atenção" ou "Não avaliável".
Forneça evidência textual e uma recomendação/reescrita caso haja violação.

---

### FORMATO DA RESPOSTA:
Retorne EXCLUSIVAMENTE um objeto JSON válido no seguinte formato:

{{
  "resumo_backlog": {{
    "total_historias": 0,
    "padroes_defeitos": ["..."],
    "lacunas_provaveis": ["..."]
  }},
  "analise_individual": [
    {{
      "id": "US001",
      "user_story_original": "Como...",
      "avaliacao_criterios": {{
        "well_formed": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
        "atomic": {{"resultado": "Viola", "evidencia": "...", "acao": "..."}},
        "minimal": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
        "conceptually_sound": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
        "problem_oriented": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
        "unambiguous": {{"resultado": "Atenção", "evidencia": "...", "acao": "..."}},
        "full_sentence": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}},
        "estimatable": {{"resultado": "Atende", "evidencia": "...", "acao": "..."}}
      }},
      "reescrita_sugerida": "Caso necessário, apresente a versão corrigida (ou separada se violar Atomic)."
    }}
  ],
  "analise_transversal_conjunto": {{
    "conflict_free": {{"resultado": "Atende", "observacao": "..."}},
    "unique": {{"resultado": "Atende", "observacao": "..."}},
    "uniform": {{"resultado": "Atende", "observacao": "..."}},
    "independent": {{"resultado": "Atende", "observacao": "..."}},
    "complete": {{"resultado": "Atenção", "observacao": "..."}}
  }}
}}

# USER STORY
"As a bank customer, I want to check my balance online, so that I can manage my finances."

""",
        },
    ],
)

print(response["message"]["content"])