import pytest
from langchain_core.messages import HumanMessage
from app.services.agent import create_agent_graph


@pytest.mark.asyncio
async def test_memory_isolation_between_threads():
    """Verifica que dos hilos conversacionales (thread_id) mantengan memoria independiente."""
    graph = create_agent_graph()

    config_user1 = {"configurable": {"thread_id": "user_100"}}
    config_user2 = {"configurable": {"thread_id": "user_200"}}

    # Usuario 1 le dice al bot que se llama Juan
    await graph.ainvoke({"messages": [HumanMessage(content="Hola, me llamo Juan")]}, config=config_user1)

    # Usuario 2 le dice al bot que se llama Pedro
    await graph.ainvoke({"messages": [HumanMessage(content="Hola, me llamo Pedro")]}, config=config_user2)

    # Obtener estados guardados por el checkpointer
    state_user1 = await graph.aget_state(config_user1)
    state_user2 = await graph.aget_state(config_user2)

    msg_history1 = [m.content for m in state_user1.values["messages"]]
    msg_history2 = [m.content for m in state_user2.values["messages"]]

    assert any("Juan" in str(msg) for msg in msg_history1)
    assert not any("Pedro" in str(msg) for msg in msg_history1)

    assert any("Pedro" in str(msg) for msg in msg_history2)
    assert not any("Juan" in str(msg) for msg in msg_history2)
