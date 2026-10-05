# System Architecture

## 1. High-Level Flow

```mermaid
flowchart TD
    subgraph DataLayer [1. Ingestion & Storage]
        Olist[Olist Public E-Commerce Data] --> Ingest[Data Cleaning & ETL]
        SynthGen[Deterministic Synthetic Commercial Layer] --> Ingest
        Ingest --> MySQL[(MySQL 8 / SQLite Engine)]
        MySQL --> Views[Analytical Views: v_order_facts, v_customer_summary, etc.]
    end

    subgraph DataScience [2. Analytics & Data Science Models]
        Views --> RFM[Customer Segmentation: RFM + K-Means]
        Views --> Propensity[Repeat-Purchase Propensity: XGBoost + Logistic Reg]
        Views --> Forecast[Demand Forecasting: SARIMAX / Moving Average]
        Views --> Territory[Territory Balancing: Heuristic Optimization]
    end

    subgraph RAGLayer [3. Knowledge Retrieval]
        Docs[Playbook & Schema Reference] --> Chunk[Chunking Engine]
        Chunk --> Embed[Sentence-Transformers Embeddings]
        Embed --> FAISS[(FAISS Vector Index)]
    end

    subgraph AgentLayer [4. Agentic Decision Support]
        UserQuery[User Natural Language Query] --> Agent[Lightweight Python Tool Agent]
        Agent --> Guardrails[Safety, Prompt Injection & SQL Guardrails]
        Guardrails --> ToolSelect{Tool Router}
        ToolSelect -->|Run SQL Query| SQLTool[Read-Only Safe SQL Engine]
        ToolSelect -->|Retrieve Guidance| RAGTool[Vector Retriever]
        ToolSelect -->|Demand Forecast| ForecastTool[Category Forecast Service]
        ToolSelect -->|Segment Profile| SegmentTool[RFM Profile Service]
        ToolSelect -->|Territory Balance| TerritoryTool[Territory Analysis Service]
        SQLTool --> StructOutput[Pydantic Structured Output Formatter]
        RAGTool --> StructOutput
        ForecastTool --> StructOutput
        SegmentTool --> StructOutput
        TerritoryTool --> StructOutput
    end

    subgraph InterfaceLayer [5. Serving & UI]
        StructOutput --> FastAPI[FastAPI REST API Service]
        FastAPI --> Streamlit[Streamlit Executive & Copilot UI]
    end
```

## 2. Component Design Principles
- **Separation of Concerns**: Data transformations, statistical models, RAG retrieval, agent tooling, and API routing operate as decoupled modules.
- **Explainability & Transparency**: The agent provides strict evidence attribution, displaying SQL queries, tool invocations, confidence levels, and model caveats.
- **Fail-Safe Operation**: Read-only database execution, strict query limits, prompt-injection defense, and structured validation prevent runaway errors.
