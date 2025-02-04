import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from elasticsearch import Elasticsearch

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routes.budget import router as budget_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


# CORS setup
origins = ["http://localhost:3000"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

ES_HOST = os.getenv("ELASTIC_ENDPOINT")
ES_USERNAME = os.getenv("ELASTIC_USERNAME")
ES_PASSWORD = os.getenv("ELASTIC_PASSWORD")

es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USERNAME, ES_PASSWORD)
)

@app.get("/test_connection")
async def test_connection():
    """Test connection to Elasticsearch."""
    if es.ping():
        return {"status": "Connection successful"}
    return {"status": "Connection failed"}

@app.post("/index/")
async def index_document(index: str, doc_id: str, body: dict):
    """Index a document in Elasticsearch."""
    response = es.index(index=index, id=doc_id, document=body)
    return {"result": response["result"]}

@app.get("/search/")
async def search_document(index: str, query: str):
    """Search for documents in Elasticsearch."""
    response = es.search(index=index, query={"match": {"content": query}})
    return {"results": response["hits"]["hits"]}


# Include routers
app.include_router(budget_router, prefix="/budget", tags=["budget"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Budgeting Service"}


@app.get("/{budget_id}")
def read_budget(budget_id: uuid.UUID):
    return {"budget_id": budget_id, "details": "Budget details would be here"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)