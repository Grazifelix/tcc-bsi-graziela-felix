import ollama

# Substitua 'llama3' pelo nome exato do modelo que você baixou no Ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": 
            """
Você é um Product Owner / Analista de Requisitos especialista em metodologias ágeis. 

Sua tarefa é analisar a transcrição de uma conversa fornecida abaixo e extrair uma lista de User Stories de alta qualidade, garantindo a rastreabilidade exata de onde cada requisito foi mencionado na conversa através dos timestamps.

---

### DIRETRIZES DE QUALIDADE DAS USER STORIES:
1. **Estrutura Padrão:** Cada User Story deve seguir rigorosamente o formato: "Como [tipo de usuário], eu quero [ação/funcionalidade] para que [benefício/valor de negócio]".
2. **Critérios de Aceite:** Cada User Story deve conter Critérios de Aceite claros e testáveis no formato BDD (Dado que..., Quando..., Então...) ou em lista objetiva.
3. **Clareza e Concisão:** Evite dubiedades. Se a fala na transcrição for vaga, refine a User Story para torná-la acionável para o time de desenvolvimento.
4. **Rastreabilidade (Timestamps):** Indique o timestamp de início e fim (ou os timestamps específicos) onde essa necessidade foi discutida na transcrição.

---

### FORMATO DA RESPOSTA:
Retorne EXCLUSIVAMENTE um objeto JSON válido (sem textos introdutórios ou explicativos antes ou depois do código JSON).

Estrutura JSON esperada:

{
  "user_stories": [
    {
      "id": "US001",
      "titulo": "Título sucinto da história",
      "user_story": "Como [usuário], eu quero [funcionalidade] para que [benefício].",
      "rastreabilidade": {
        "timestamp_inicio": "00:00:00",
        "timestamp_fim": "00:00:00",
        "trecho_citado": "Transcrição exata ou aproximada do trecho relevante falado na conversa"
      }
    }
  ]
}

---

### TRANSCRIÇÃO DA CONVERSA COM TIMESTAMPS:

**Transcrição da Reunião de Alinhamento de Requisitos**

**Participantes:**

* **Carlos (Stakeholder):** Gerente de Operações da Empresa
* **Mariana (Analista de Requisitos):** Equipe de Tecnologia / Produto

---

[00:00 - 00:25] **Mariana:** Bom dia, Carlos! Obrigado por reservar um tempo hoje. O objetivo desta reunião é entender melhor o que você precisa para o novo módulo de relatórios do sistema de vendas, para que possamos mapear os requisitos da melhor forma.

[00:25 - 00:58] **Carlos:** Bom dia, Mariana. O prazer é meu. Olha, a gente está com um gargalo enorme no final do mês. A equipe gasta horas consolidadas em planilhas do Excel para gerar o relatório de vendas por região. Eu preciso de algo no sistema que faça isso automaticamente e em tempo real.

[00:58 - 01:25] **Mariana:** Perfeito, entendi a dor principal. Quando você fala em relatório por região, quais informações específicas precisam ser exibidas? Estamos falando apenas do valor total de vendas ou precisamos detalhar por produto, vendedor ou categoria?

[01:25 - 02:05] **Carlos:** No nível executivo, eu preciso ver o total por região de forma simples. Mas os supervisores regionais vão usar o mesmo relatório, então eles precisam conseguir "clicar" na região e expandir para ver o detalhamento por vendedor e por linha de produto. Se puder ter um filtro de data customizável, seria ideal.

[02:05 - 02:40] **Mariana:** Excelente. Então temos um relatório com visão macro para diretoria e recurso de *drill-down* para os supervisores, com filtros por Período, Região, Vendedor e Categoria. Sobre a exportação desses dados, existe a necessidade de baixar isso em algum formato específico, como PDF ou Excel?

[02:40 - 03:10] **Carlos:** Com certeza. O pessoal de finanças sempre pede em Excel para cruzar com outros dados, e a diretoria prefere receber em PDF nas reuniões semanais. Então precisamos das duas opções de exportação.

[03:10 - 03:42] **Mariana:** Combinado, vou incluir a exportação em PDF e XLSX nos requisitos funcionais. Uma última dúvida sobre regras de acesso e segurança: qualquer usuário logado no sistema poderá ver o relatório completo de todas as regiões, ou deve haver restrição baseada no perfil?

[03:42 - 04:18] **Carlos:** Boa pergunta. Cada supervisor regional só deve enxergar os dados da sua própria região. Apenas a minha diretoria e a equipe financeira podem ter acesso à visão global de todas as regiões.

[04:18 - 04:45] **Mariana:** Anotado! Acesso restrito por perfil e escopo regional. Já tenho o suficiente para estruturar a primeira versão do documento de requisitos e as histórias de usuário. Até a próxima terça-feira eu te envio para validação e aprovação. Muito obrigada, Carlos!

[04:45 - 05:00] **Carlos:** Perfeito, Mariana! Muito obrigado pela agilidade. Fico no aguardo do documento. Bom trabalho!

""",
        },
    ],
)

print(response["message"]["content"])