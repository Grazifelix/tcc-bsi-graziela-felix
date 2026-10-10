import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from services.transcriber import AudioTranscriber
from services.user_story_generator import UserStoryPipeline

app = FastAPI(
    title="User Story & QUS Generator API",
    description="API para transcrição de áudio, geração de User Stories e análise QUS-Framework.",
    version="1.0.0"
)

# Inicialização dos serviços (carregados uma vez para otimizar desempenho)
transcriber = AudioTranscriber(model_size="small", device="cpu", compute_type="int8")
pipeline = UserStoryPipeline()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Modelos de Resposta (Pydantic) ---

class TextProcessRequest(BaseModel):
    transcript_text: str

class PipelineResponse(BaseModel):
    transcription: Dict[str, Any]
    user_stories: Dict[str, Any]
    qus_analysis: Dict[str, Any]

# --- Endpoints ---

@app.post("/api/v1/transcribe", summary="Transcrever ficheiro de áudio")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """Recebe um ficheiro de áudio (.m4a, .mp3, .wav) e devolve a transcrição com timestamps."""
    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcription_data = transcriber.transcribe(temp_file_path)
        return transcription_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar áudio: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/api/v1/generate-user-stories", summary="Gerar User Stories e Análise QUS")
async def generate_stories_endpoint(payload: TextProcessRequest):
    """Recebe o texto formatado da transcrição e gera as User Stories juntamente com a análise QUS."""
    try:
        user_stories_data = pipeline.generate_user_stories(transcript_text=payload.transcript_text)
        qus_result = pipeline.analyze_qus(user_stories_data)
        return {
            "user_stories": user_stories_data,
            "qus_analysis": qus_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento do LLM: {str(e)}")

@app.post("/api/v1/process-audio-pipeline", response_model=PipelineResponse, summary="Executar Pipeline Completa por Áudio")
async def process_full_pipeline_endpoint(file: UploadFile = File(...)):
    """Endpoint único: Envia o áudio, executa a transcrição, gera as User Stories e analisa via QUS."""
    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Transcrição
        transcription_data = transcriber.transcribe(temp_file_path)

        # 2. Geração de User Stories
        formatted_transcript = transcription_data.get("formatted_transcript", "")
        user_stories_data = pipeline.generate_user_stories(transcript_text=formatted_transcript)

        # 3. Análise QUS
        qus_result = pipeline.analyze_qus(user_stories_data)

        return PipelineResponse(
            transcription=transcription_data,
            user_stories=user_stories_data,
            qus_analysis=qus_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na execução da pipeline: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# import json
# import os
# from services.transcriber import AudioTranscriber
# from services.user_story_generator import UserStoryPipeline

# def save_json(data, filepath):
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
#     print(f"💾 Salvo em: {filepath}")

# def run_pipeline(audio_file):
#     base_name = os.path.splitext(os.path.basename(audio_file))[0]
    
#     transcript_json_path = f"outputs/{base_name}_transcription.json"
#     user_stories_json_path = f"outputs/{base_name}_user_stories.json"
#     qus_analysis_json_path = f"outputs/{base_name}_qus_analysis.json"

#     # 1. Transcrição
#     transcriber = AudioTranscriber(model_size="small", device="cpu", compute_type="int8")
#     transcription_data = transcriber.transcribe(audio_file)
#     save_json(transcription_data, transcript_json_path)

#     # 2. Geração de User Stories
#     pipeline = UserStoryPipeline(model_name="llama3.2:3b")
#     user_stories_data = pipeline.generate_user_stories(
#         transcript_text=transcription_data["formatted_transcript"]
#     )
#     save_json(user_stories_data, user_stories_json_path)

#     # 3. Análise QUS-Framework
#     qus_result = pipeline.analyze_qus(user_stories_data)
#     save_json(qus_result, qus_analysis_json_path)

#     print("\n✅ Processo completo concluído com sucesso!")
#     print(f"📄 Transcrição: {transcript_json_path}")
#     print(f"📄 User Stories: {user_stories_json_path}")
#     print(f"📄 Análise QUS: {qus_analysis_json_path}")

# if __name__ == "__main__":
#     audio_input = "audio2.m4a"
#     run_pipeline(audio_input)

# import json
# import os
# from services.transcriber import AudioTranscriber
# from user_story_generator import UserStoryGenerator

# def save_json(data, filepath):
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
#     print(f"💾 Salvo em: {filepath}")

# def run_pipeline(audio_file):
#     # Configuração dos arquivos de saída
#     base_name = os.path.splitext(os.path.basename(audio_file))[0]
#     transcript_json_path = f"outputs/{base_name}_transcription.json"
#     user_stories_json_path = f"outputs/{base_name}_user_stories.json"

#     # Passo 1: Transcrever o Áudio
#     transcriber = AudioTranscriber(model_size="small", device="cpu", compute_type="int8")
#     transcription_data = transcriber.transcribe(audio_file)

#     # Passo 2: Salvar Transcrição em JSON
#     save_json(transcription_data, transcript_json_path)

#     # Passo 3: Enviar para o LLM
#     generator = UserStoryGenerator(model_name="llama3.2:3b")
#     user_stories_data = generator.generate_user_stories(
#         transcript_text=transcription_data["formatted_transcript"]
#     )

#     # Passo 4: Salvar User Stories em JSON
#     save_json(user_stories_data, user_stories_json_path)

#     print("\n✅ Processo concluído com sucesso!")
#     print(f"📋 Total de User Stories geradas: {len(user_stories_data.get('user_stories', []))}")

# if __name__ == "__main__":
#     audio_input = "audio2.m4a"
#     run_pipeline(audio_input)


# # import json
# # from services.transcription import AudioTranscriber

# # def save_to_json(data, output_filepath):
# #     with open(output_filepath, "w", encoding="utf-8") as f:
# #         json.dump(data, f, ensure_ascii=False, indent=4)

# # if __name__ == "__main__":
# #     audio_file = "audio2.m4a"
# #     json_file = "transcription.json"

# #     # Inicializa o transcritor
# #     transcriber = AudioTranscriber(model_size="small", device="cpu", compute_type="int8")

# #     # Realiza a transcrição
# #     print(f"Iniciando transcrição do áudio '{audio_file}'...")
# #     transcription_data = transcriber.transcribe(audio_file)

# #     # print("\nInformações do Idioma:")
# #     # print("Detected language '%s' with probability %f" % (
# #     #     transcription_data["metadata"]["language"], 
# #     #     # transcription_data["metadata"]["language_probability"]
# #     # ))

# #     # Salva no arquivo JSON
# #     save_to_json(transcription_data, json_file)
# #     print(f"\nTranscrição salva com sucesso em '{json_file}'!")