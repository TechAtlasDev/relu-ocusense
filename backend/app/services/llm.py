import asyncio
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage
from app.config import settings

from app.services.agent import agent_graph


class LLMService:
    """Servicio para integrar el flujo conversacional con LangGraph, Gemini y memoria por usuario."""

    async def generate_response_stream(
        self, prompt: str, thread_id: str = "default", delay: float = 0.05
    ) -> AsyncGenerator[str, None]:
        """Ejecuta el agente de LangGraph en el hilo de memoria especificado y emite fragmentos en streaming."""
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [HumanMessage(content=prompt)]}

        api_key = settings.effective_gemini_api_key
        if api_key:
            accumulated_text = ""
            tools_notified = set()
            
            # Ejecutar el grafo de LangGraph
            async for message, metadata in agent_graph.astream(inputs, config=config, stream_mode="messages"):
                node_name = metadata.get("langgraph_node")
                
                # Emitir evento independiente de herramienta utilizada
                if node_name == "tools":
                    tool_name = getattr(message, "name", None) or "herramienta"
                    if tool_name not in tools_notified:
                        tools_notified.add(tool_name)
                        yield {"type": "tool_used", "tool_name": tool_name}

                # Emitir streaming limpio generado por el modelo (IA)
                elif node_name == "chatbot":
                    if message.content:
                        text_delta = ""
                        if isinstance(message.content, str):
                            text_delta = message.content
                        elif isinstance(message.content, list):
                            for part in message.content:
                                if isinstance(part, str):
                                    text_delta += part
                                elif isinstance(part, dict) and "text" in part:
                                    text_delta += part.get("text", "")

                        if text_delta:
                            accumulated_text += text_delta
                            yield accumulated_text
                            await asyncio.sleep(delay)

        else:
            # Fallback en caso de no contar con la clave de API
            result = await agent_graph.ainvoke(inputs, config=config)
            final_msg = result["messages"][-1].content
            words = str(final_msg).split(" ")
            current = ""
            for word in words:
                current += (word + " ")
                yield current.strip()
                await asyncio.sleep(delay)


llm_service = LLMService()
