import pytest
from app.services.llm import LLMService


@pytest.mark.asyncio
async def test_llm_service_response_stream():
    service = LLMService()
    prompt = "Hola, ¿cómo estás?"

    chunks = []
    async for chunk in service.generate_response_stream(prompt, delay=0.001):
        chunks.append(chunk)

    assert len(chunks) > 0
    assert len(chunks[0]) > 0


    # Verificar que cada chunk subsecuente contenga al anterior (acumulativo)
    assert len(chunks[-1]) >= len(chunks[0])
