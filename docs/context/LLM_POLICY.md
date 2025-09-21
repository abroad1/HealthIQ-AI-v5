# 🤖 LLM Policy for HealthIQ AI

HealthIQ AI v5 uses **Google Gemini** as its sole LLM engine across all systems.

- No GPT-4, Claude, OpenAI, or Anthropic services are used in production.
- All behavioural recommendations, insight synthesis, and narrative generation are powered by Gemini.
- Any legacy references to other LLMs are deprecated and must not be reintroduced.

Cursor and human agents must treat this file as the single source of truth for LLM usage.
