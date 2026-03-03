🚀 Agentic Blog Generator using LangGraph + Groq + FastAPI

An AI-powered blog generation API built using LangGraph, LangChain, Groq LLM (LLaMA 3.1), and FastAPI.

This project demonstrates how to build an agentic workflow using StateGraph (LangGraph) to generate blog titles, content, and optionally translate the blog into multiple languages using conditional graph routing.

📌 Project Overview

This system dynamically builds a graph-based AI workflow that:

Generates an SEO-friendly blog title

Generates detailed blog content

Optionally translates the blog into:

Hindi

French

Returns structured blog output via REST API

The project showcases:

✅ Agentic workflow design using LangGraph

✅ Conditional routing in AI pipelines

✅ State management using TypedDict

✅ Groq LLaMA model integration

✅ Production-ready FastAPI API structure

🏗️ Architecture Overview
🧠 Topic-Based Blog Generation Flow
4
Flow:
START
↓
Title Creation
↓
Content Generation
↓
END
🌍 Language-Based Blog Generation Flow

If a language is provided, a conditional routing system is triggered.

Flow:
START
↓
Title Creation
↓
Content Generation
↓
Route Decision
↙ ↘
Hindi French
↓ ↓
END END

This demonstrates Agentic Conditional Execution using LangGraph.

🛠️ Tech Stack

LangGraph – Stateful AI workflow orchestration

LangChain

Groq LLM (LLaMA 3.1 8B Instant)

FastAPI

Pydantic

Uvicorn

Python 3.10+

📂 Project Structure
.
├── app.py
├── src/
│ ├── Graphs/
│ │ └── graph_builder.py
│ ├── Nodes/
│ │ └── blog_node.py
│ ├── States/
│ │ └── blogstate.py
│ └── LLMs/
│ └── groqllm.py
├── .env
├── requirements.txt
└── README.md
⚙️ Code Explanation & Flow
1️⃣ app.py (FastAPI Entry Point)

This is the main API entry file.

Endpoint:
POST /blogs
Logic:

Accepts JSON input:

{
"topic": "Artificial Intelligence",
"language": "hindi"
}

Initializes:

GroqLLM

GraphBuilder

Dynamically selects graph:

If only topic → Topic Graph

If topic + language → Language Graph

Invokes the compiled graph:

state = graph.invoke({...})

Returns structured blog output.

2️⃣ graph_builder.py (Workflow Orchestration)

This file constructs the LangGraph StateGraph.

Two Graph Types:
✅ Topic Graph

Used when only topic is provided.

Nodes:

title_creation

content_generation

Edges:

START → title_creation → content_generation → END
✅ Language Graph

Used when topic + language provided.

Additional Nodes:

route

hindi_translation

french_translation

Conditional Routing:

self.graph.add_conditional_edges(
"route",
self.blog_node_obj.route_decision,
{
"hindi": "hindi_translation",
"french": "french_translation"
}
)

This demonstrates dynamic decision-based graph execution.

3️⃣ blog_node.py (Business Logic Layer)

This file contains all AI-powered operations.

🔹 title_creation()

Generates SEO-friendly title

Uses Markdown formatting

Returns partial state update

🔹 content_generation()

Generates detailed blog

Preserves generated title

Updates state with full blog

🔹 translation()

Accepts blog content

Translates into selected language

Maintains formatting

Returns updated state

🔹 route_decision()

Determines which translation node to execute.

if state["current_language"] == "hindi":
return "hindi"

This enables conditional branching in the graph.

4️⃣ blogstate.py (State Management)

Uses:

TypedDict → BlogState
Pydantic → Blog Model
BlogState:
class BlogState(TypedDict):
topic: str
blog: Blog
current_language: str

This ensures:

Structured state transitions

Predictable workflow execution

5️⃣ groqllm.py (LLM Integration)

Wraps Groq’s LLaMA 3.1 model:

ChatGroq(
model="llama-3.1-8b-instant"
)

Environment variable required:

GROQ_API_KEY=your_api_key
🚀 Installation
1️⃣ Clone Repository
git clone https://github.com/awasthi-anjali/Blog-Generation-and-Translation.git
cd agentic-blog-generator
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate # mac
venv\Scripts\activate # windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Environment Variables

Create .env file:

GROQ_API_KEY=your_api_key
LANGCHAIN_API_KEY=your_langsmith_key
5️⃣ Run Server
python app.py

Server runs at:

http://localhost:8000
🧪 API Usage
Request:
POST /blogs
Body:
{
"topic": "Future of AI",
"language": "french"
}
Response:
{
"data": {
"blog": {
"title": "...",
"content": "..."
}
}
}
💡 Key Concepts Demonstrated

🔹 Agentic AI Workflow

🔹 Conditional Graph Routing

🔹 State-Based LLM Execution

🔹 Multi-step AI Pipelines

🔹 Translation via LLM

🔹 Modular Clean Architecture
