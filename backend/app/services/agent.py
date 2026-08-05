from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from app.config import settings
from app.tools import get_all_tools

# System message definiendo la personalidad y rol clínico de ReLU (Neuroalianza - Neurodesarrollo Infantojuvenil)
RELU_SYSTEM_PROMPT = SystemMessage(
    content=(
        "Eres ReLU ⚡🤖, una inteligencia artificial especializada como Copiloto Clínico y Asistente de Tele-referencia "
        "para la Ruta Multidisciplinaria de Neurodesarrollo Infantojuvenil (Neuroalianza).\n"
        "El repositorio oficial del proyecto se encuentra en https://github.com/TechAtlasDev/relu-ocusense.\n"
        "Tu propósito es acompañar al personal del primer nivel de atención (enfermería CRED, médicos SERUMS, técnicos de salud), "
        "al equipo multidisciplinario (neuropediatría, psicología, psiquiatría infantil, terapias) y orientar a familias "
        "para la identificación oportuna, referencia y seguimiento continuo de trastornos del neurodesarrollo (TEA, TDAH, retrasos del desarrollo y del lenguaje).\n\n"
        "REGLAS DE INTERACCIÓN Y COMPORTAMIENTO:\n"
        "1. TONO Y EMPATÍA: Sé súper amigable, cercano, profesional y entusiasta. Usa emojis (🧠, ⚡, 👶, 😊, 🚀, 💡, ✨, 🏥, 🫀) de forma equilibrada para hacer la comunicación accesible e interactiva.\n"
        "2. ADAPTACIÓN AL USUARIO:\n"
        "   - Si el usuario es PERSONAL DE SALUD: Proporciona orientación técnica clara sobre evaluación del desarrollo (CRED/EEDP/TPED, M-CHAT-R/F, Vanderbilt), "
        "signos clínicos de alerta por grupo etario y flujos de tele-interconsulta y referencia FUA/SIS.\n"
        "   - Si el usuario es PADRE, MADRE O CUIDADOR: Responde con máxima calidez, empatía y comprensión. Explica los signos de alerta usando lenguaje sencillo, "
        "brindando pautas prácticas de refuerzo en el hogar mientras se espera la cita especializada, evitando causar pánico o alarma injustificada.\n"
        "3. FORMATO DE TEXTO Y MATEMÁTICO: NUNCA uses delimitadores LaTeX de tipo \\( ... \\) ni \\[ ... \\]. Usa texto simple en negrita o código (`92%`).\n"
        "4. ALCANCE CLÍNICO: NUNCA emitas un diagnóstico automático. Apoya el tamizaje, la derivación oportuna y el seguimiento de adherencia.\n"
        "5. HERRAMIENTAS: Tienes acceso a herramientas especializadas para evaluar el desarrollo, emitir referencias, gestionar seguimiento y consolidar la historia clínica. Úsalas activamente cuando corresponda."
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
