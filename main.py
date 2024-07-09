import os
import anthropic
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from gtts import gTTS

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos y la carpeta de históricos
DB_NAME = "english_lessons.db"
HISTORIC_FOLDER = "historic"

def init_db():
    """
    Inicializa la base de datos SQLite.
    Crea la tabla 'conversations' si no existe.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     timestamp TEXT,
     role TEXT,
     content TEXT)
    ''')
    conn.commit()
    conn.close()

def load_conversation():
    """
    Carga la conversación desde la base de datos.
    Si no hay conversación, devuelve una conversación inicial predeterminada.
    
    Returns:
        list: Lista de diccionarios con la conversación cargada.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM conversations ORDER BY id")
    conversation = cursor.fetchall()
    conn.close()

    if not conversation:
        # Conversación inicial predeterminada
        return [
            {"role": "user", "content": "You are a British English teacher. You should teach and converse at an A1 level, using simple vocabulary and grammar. Speak in a friendly, encouraging manner, and correct any mistakes gently. Always respond in English, even if the student uses another language."},
            {"role": "assistant", "content": "Understood. I'll act as a friendly British English teacher, focusing on A1 level English. I'll use simple language, encourage the student, and provide gentle corrections when needed. I'm ready to begin our lesson."}
        ]
    return [{"role": role, "content": content} for role, content in conversation]

def save_message(role, content):
    """
    Guarda un mensaje en la base de datos.
    
    Args:
        role (str): El rol del mensaje ('user' o 'assistant').
        content (str): El contenido del mensaje.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO conversations (timestamp, role, content) VALUES (?, ?, ?)",
                   (timestamp, role, content))
    conn.commit()
    conn.close()

def save_conversation_to_pdf_and_mp3():
    """
    Guarda la conversación actual en archivos PDF y MP3.
    Los archivos se guardan en la carpeta 'historic' con nombres basados en la fecha y hora actuales.
    """
    if not os.path.exists(HISTORIC_FOLDER):
        os.makedirs(HISTORIC_FOLDER)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, role, content FROM conversations ORDER BY id")
    conversation = cursor.fetchall()
    conn.close()

    if not conversation:
        print("No conversation to save.")
        return

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    pdf_filename = f"{HISTORIC_FOLDER}/{timestamp}.pdf"
    mp3_filename = f"{HISTORIC_FOLDER}/{timestamp}.mp3"

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Crear contenido para MP3
    mp3_content = ""

    for timestamp, role, content in conversation:
        # Añadir al PDF
        pdf.cell(200, 10, txt=f"{timestamp} - {role}:", ln=1)
        pdf.multi_cell(0, 10, txt=content)
        pdf.ln(10)

        # Añadir al contenido MP3
        mp3_content += f"{role}: {content}\n"

    # Guardar PDF
    pdf.output(pdf_filename)

    # Crear y guardar MP3
    tts = gTTS(mp3_content, lang='en', tld='co.uk')  # 'co.uk' para acento británico
    tts.save(mp3_filename)

    print(f"Conversation saved to {pdf_filename} and {mp3_filename}")

def clear_all_data():
    """
    Limpia todos los datos de la conversación.
    Primero guarda la conversación actual en PDF y MP3, luego borra la tabla de la base de datos.
    
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario.
    """
    try:
        # Primero, guardar la conversación actual en PDF y MP3
        save_conversation_to_pdf_and_mp3()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Eliminar todos los registros de la tabla de conversaciones
        cursor.execute("DROP TABLE IF EXISTS conversations")
        
        # Recrear la tabla vacía
        cursor.execute('''
        CREATE TABLE conversations
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp TEXT,
         role TEXT,
         content TEXT)
        ''')
        
        conn.commit()
        conn.close()
        
        print("All conversation data cleared successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while clearing data: {str(e)}")
        return False

def english_teacher_bot():
    """
    Función principal que ejecuta el bot de enseñanza de inglés.
    Maneja la interacción con el usuario, procesa las entradas y genera respuestas usando la API de Anthropic.
    """
    init_db()
    conversation_history = load_conversation()
    
    # Obtener la clave API del archivo .env
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file.")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print("Hello! I'm your British English teacher. I'm here to help you practice English at an A1 level.")
    print("Type 'clear' to clear all conversation data, or 'exit' to end our lesson.")
    
    while True:
        user_input = input("Student: ").strip()
        
        if user_input.lower() == 'exit':
            print("Teacher: Well done today! Goodbye and keep practicing your English!")
            break
        elif user_input.lower() == 'clear':
            if clear_all_data():
                conversation_history = load_conversation()
                print("Teacher: I've cleared our conversation history and saved it as PDF and MP3. Let's start fresh!")
            continue
        
        # Añadir la entrada del usuario a la conversación y guardarla
        conversation_history.append({"role": "user", "content": user_input})
        save_message("user", user_input)

        print("Teacher is typing...")
        # Generar respuesta usando la API de Anthropic
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=conversation_history
        )
        
        assistant_response = response.content[0].text
        print(f"Teacher: {assistant_response}")
        
        # Añadir la respuesta del asistente a la conversación y guardarla
        conversation_history.append({"role": "assistant", "content": assistant_response})
        save_message("assistant", assistant_response)

if __name__ == "__main__":
    english_teacher_bot()