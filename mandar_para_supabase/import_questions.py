import json
from supabase import create_client, Client

SUPABASE_URL = "https://gqicstkraeduyacemzct.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxaWNzdGtyYWVkdXlhY2VtemN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0NDU3MzcsImV4cCI6MjA3MDAyMTczN30.n5vRK9_514dzJ6OS_QR3HEQyyDzL0p3jHkeZmulxfls"
JSON_PATH = "prova_2022_com_topicos.json"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Ler o arquivo JSON
with open(JSON_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

questions = data['questions']

#Inserir as questões no banco de dados
# === INSERIR QUESTÕES ===
for q in questions:
    response = supabase.table("questions").insert({
        "index": q["index"],
        "title": q["title"],
        "discipline": q["discipline"],
        "language": q["language"],
        "year": q["year"],
        "context": q.get("context"),
        "files": q.get("files", []),
        "correct_alternative": q.get("correctAlternative"),
        "alternatives_intro": q.get("alternativesIntroduction"),
        "alternatives": q.get("alternatives", []),
        "topics": q.get("topicos", []),
        "similarity_score": q.get("similarity_score"),
    }).execute()

print(f"Inseridas {len(questions)} Questões")
