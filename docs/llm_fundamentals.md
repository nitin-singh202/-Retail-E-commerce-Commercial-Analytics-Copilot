# LLM Fundamentals & Practical Engineering Guide

This document explains the core parameters, mechanisms, and architectural trade-offs in building enterprise-grade LLM applications.

---

## 1. Parameters & Mechanics

### Temperature
- **What it does**: Scales the logits (pre-softmax output layer of the LLM) before sampling the next token.
- **Formula**: `P(token_i) = exp(z_i / T) / sum_j(exp(z_j / T))`
- **Behavior**:
  - `T = 0.0` (Greedy decoding): Always selects the argmax token. Crucial for reproducible tasks like SQL generation, structured JSON extraction, and exact math.
  - `T > 0.7`: Flattens the probability distribution, introducing randomness and variety (suitable for creative brainstorming, but dangerous for analytics).

### Top-p (Nucleus Sampling)
- **What it controls**: Sets a cumulative probability threshold $p \in (0, 1]$. The model filters out the long tail of low-probability tokens, considering only the smallest set whose summed probability exceeds $p$.
- **Why it matters**: Truncates unlikely tokens while preserving diversity among plausible candidates.

### Max Tokens vs Context Window
- **Context Window**: Total capacity (input prompt + output tokens) that the model's self-attention mechanism can process simultaneously (e.g. 8k, 32k, 128k tokens).
- **Max Tokens**: An explicit generation limit for output tokens to prevent runaway loops and control latency/cost.

---

## 2. Embeddings & Vector Representation

### Why Embeddings are Needed
- LLMs operate on discrete tokens, but similarity in natural language is continuous and semantic.
- Embedding models map variable-length texts into dense, fixed-dimension vectors (e.g., 384 dimensions for `all-MiniLM-L6-v2`).
- Semantic similarity is computed via cosine similarity or dot product in vector space.

---

## 3. Why RAG instead of Pure LLM Generation?
1. **Freshness & Private Knowledge**: LLM weights are frozen after training; RAG retrieves up-to-date, proprietary enterprise documents.
2. **Eliminating Hallucinations**: Grounding answers in verified text snippets provides an auditable paper trail.
3. **Context Window Efficiency**: Instead of stuffing hundreds of pages of documentation into every prompt, RAG retrieves only the top-$K$ most relevant passages.

---

## 4. Common Failure Modes & Mitigations
- **Prompt Injection**: User input instructs the model to ignore safety rules. *Mitigation*: Strict role separation, tagging untrusted context as data, using structured output schemas.
- **SQL Hallucination**: Model invents non-existent columns or joins. *Mitigation*: Injecting precise DDL schemas into the system prompt and using AST parsers (`sqlglot`) to validate queries before execution.
