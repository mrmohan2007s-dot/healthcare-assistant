# System Design

- Backend: Flask API with `/ask` endpoint. Safety filter enforces non-diagnostic behavior.
- LLM integration: `backend/llm_handler.py` (pluggable to OpenAI or other providers).
- Frontend: simple static page calling `/ask`.
- Data: curated `data/` files with sources and symptom mappings.
