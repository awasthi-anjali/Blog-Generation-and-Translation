import uvicorn

from typing import Optional
import sqlite3
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from src.Graphs.graph_builder import GraphBuilder
from src.LLMs.groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FILE = os.path.join(BASE_DIR, "frontend", "index.html")
DB_FILE = os.path.join(BASE_DIR, "blogs.db")

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## API'S

class BlogRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="Topic to generate the blog on")
    language: Optional[str] = Field(default="", description="Optional language (hindi/french)")


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS blog_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                language TEXT,
                title TEXT,
                content TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_blog_to_db(topic: str, language: str, title: str, content: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            INSERT INTO blog_history (topic, language, title, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (topic, language, title, content, datetime.utcnow().isoformat()),
        )
        conn.commit()


def get_blog_fields(state):
    blog_data = state.get("blog", {}) if isinstance(state, dict) else {}
    if hasattr(blog_data, "model_dump"):
        blog_data = blog_data.model_dump()
    elif not isinstance(blog_data, dict):
        blog_data = {}

    title = blog_data.get("title", "")
    content = blog_data.get("content", "")
    return title, content


def generate_blog(topic: str, language: str = ""):
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Topic is required")

    # get the llm object
    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    # get the graph
    graph_builder = GraphBuilder(llm)
    if language:
        graph = graph_builder.setup_graph(usecase="language")
        state = graph.invoke({"topic": topic, "current_language": language.lower()})
    else:
        graph = graph_builder.setup_graph(usecase="topic")
        state = graph.invoke({"topic": topic})

    title, content = get_blog_fields(state)
    save_blog_to_db(topic=topic, language=language, title=title, content=content)

    return {"data": state}


@app.get("/")
async def home():
    return FileResponse(FRONTEND_FILE)


@app.get("/blogs")
async def create_blogs_get(
    topic: str = Query(..., min_length=1, description="Topic to generate the blog on"),
    language: str = Query("", description="Optional language, e.g. hindi or french"),
):
    return generate_blog(topic=topic, language=language)


@app.post("/blogs")
async def create_blogs_post(payload: BlogRequest):
    return generate_blog(topic=payload.topic, language=payload.language or "")


@app.get("/blogs/history")
async def get_blogs_history(
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, topic, language, title, content, created_at
            FROM blog_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return {"data": [dict(row) for row in rows]}


@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("DELETE FROM blog_history WHERE id = ?", (blog_id,))
        conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"message": "Blog deleted successfully", "id": blog_id}


@app.on_event("startup")
async def startup_event():
    init_db()


if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)