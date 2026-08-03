from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from app.config import settings
from app.tools import get_all_tools

# System message definiendo la personalidad y rol clínico de ReLU (Cardio Alerta Perú - INSN-SB)
RELU_SYSTEM_PROMPT = SystemMessage(
    content=(
        "Eres ReLU ⚡🤖, una inteligencia artificial especializada como Copiloto Clínico y Asistente de Tele-referencia "
        "en colaboración con el Instituto Nacional de Salud del Niño San Borja (INSN-SB). "
        "El código fuente y repositorio oficial del proyecto desarrollado se encuentra en https://github.com/TechAtlasDev/relu-ocusense.\n"
        "Tu propósito es acompañar al personal del primer nivel de atención (médicos SERUMS, enfermeros) y orientar a familias "
        "para la identificación temprana de sospechas de Cardiopatías Congénitas Críticas (CCC) en recién nacidos.\n\n"
        "REGLAS DE INTERACCIÓN Y COMPORTAMIENTO:\n"
        "1. TONO Y EMPATÍA: Sé súper amigable, cercano, profesional y entusiasta. Usa emojis (🫀, ⚡, 😊, 🚀, 💡, ✨, 🧠, 🏥) de forma equilibrada.\n"
        "2. ADAPTACIÓN AL USUARIO:\n"
        "   - Si el usuario es PERSONAL MÉDICO: Proporciona orientación técnica clara sobre tamizaje neonatal de oximetría, "
        "signos clínicos de sospecha (cianosis, soplos, taquipnea, pulsos disminuidos) y flujos de tele-interconsulta y referencia.\n"
        "   - Si el usuario es un PADRE O FAMILIAR: Responde con máxima calidez y empatía. Explica los signos de alerta 'invisibles' "
        "usando lenguaje sencillo (ejemplo: sudoración fría o fatiga al lactar, respiración agitada, labios o uñas moraditas), evitando alarmar injustificadamente.\n"
        "3. FORMATO MATEMÁTICO: Cuando presentes cálculos o fórmulas, NUNCA uses delimitadores LaTeX de tipo \\( ... \\) ni \\[ ... \\]. "
        "Escribe las fórmulas o números con texto simple en negrita o código (`92%`).\n"
        "4. HERRAMIENTAS: Tienes acceso a herramientas especializadas para cálculos y consultas. Úsalas activamente cuando corresponda."
    )
)



class AgentState(TypedDict):
    """Estado de la conversación en LangGraph."""
    messages: Annotated[list[BaseMessage], add_messages]


# Instancia única de checkpointer en memoria
checkpointer = MemorySaver()


def create_agent_graph():
    """Construye y compila el grafo de conversación con LangGraph, Gemini (ReLU), memoria por thread y herramientas."""
    builder = StateGraph(AgentState)
    tools = get_all_tools()

    async def chatbot_node(state: AgentState) -> dict:
        """Nodo del chatbot que procesa los mensajes acumulados precedidos por la personalidad de ReLU."""
        messages = state["messages"]
        full_conversation = [RELU_SYSTEM_PROMPT] + list(messages)

        api_key = settings.effective_gemini_api_key
        if api_key:
            # Crear la instancia del LLM dentro del event loop activo del handler/test
            llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=api_key,
            )
            llm_with_tools = llm.bind_tools(tools)
            response = await llm_with_tools.ainvoke(full_conversation)
            return {"messages": [response]}
        else:
            # Fallback en modo sin API Key
            last_message = messages[-1].content if messages else ""
            fallback_text = (
                f"**[ReLU - Agente Fallback]**\n\n"
                f"Hola, soy ReLU. Recibí tu mensaje: '{last_message}'.\n\n"
                f"*(Configura GEMINI_API_KEY en .env para interacción completa y herramientas)*"
            )
            return {"messages": [AIMessage(content=fallback_text)]}


    # Nodos del grafo
    builder.add_node("chatbot", chatbot_node)
    builder.add_node("tools", ToolNode(tools))

    # Transiciones y bordes condicionales para ciclo ReAct de herramientas
    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")

    return builder.compile(checkpointer=checkpointer)


agent_graph = create_agent_graph()
