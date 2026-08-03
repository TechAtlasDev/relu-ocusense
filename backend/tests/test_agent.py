import pytest
from langchain_core.messages import HumanMessage
from app.services.agent import create_agent_graph


@pytest.mark.asyncio
async def test_agent_graph_execution():
    """Prueba la ejecución del grafo de LangGraph."""
    graph = create_agent_graph()
    inputs = {"messages": [HumanMessage(content="Hola agent")]}
    config = {"configurable": {"thread_id": "test_thread"}}

    result = await graph.ainvoke(inputs, config=config)

    assert "messages" in result
    assert len(result["messages"]) == 2  # HumanMessage + AIMessage
    last_msg = result["messages"][-1]
    assert len(last_msg.content) > 0


