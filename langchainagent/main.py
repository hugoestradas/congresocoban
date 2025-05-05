# main.py

import os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import BaseTool
from typing import Optional

# Cargar variables de entorno (asegúrate de tener un archivo .env con tu API key de OpenAI)
load_dotenv()

# Inicializar modelo LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")  # Puedes usar "gpt-3.5-turbo" si no tienes acceso a GPT-4

# 🔧 Herramienta personalizada: Calculadora
class CalculatorTool(BaseTool):
    name: str = "Simple Calculator"
    description: str = (
        "Usa esta herramienta para evaluar operaciones matemáticas simples. Ej: 3 + 4 * 2"
    )

    def _run(self, query: str) -> str:
        try:
            result = eval(query, {"__builtins__": {}})
            return f"El resultado es: {result}"
        except Exception as e:
            return f"Error al calcular: {e}"

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Esta herramienta no soporta ejecución async")

# 🧠 Memoria de conversación
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🧠 Inicializar agente
tools = [CalculatorTool()]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True,
)

# 💬 Loop de conversación
def run_chat():
    print("🤖 Agente conversacional iniciado. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Hasta luego!")
            break
        response = agent.run(user_input)
        print("Agente:", response)

if __name__ == "__main__":
    run_chat()
