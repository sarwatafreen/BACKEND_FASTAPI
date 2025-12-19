import os
import uvicorn
from dotenv import load_dotenv
from typing import List, Optional

# FastAPI and CORS imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# 1. Initialize FastAPI app
app = FastAPI(title="AI Todo API")

# 2. Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Data Models
class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory database
todos: List[Todo] = []
todo_id_counter = 1

# --- 4. CRUD Endpoints ---
@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    """Get all todos"""
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    """Create a new todo"""
    global todo_id_counter
    todo.id = todo_id_counter
    todo_id_counter += 1
    todos.append(todo)
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    """Update a specific todo by ID"""
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            # Preserve the ID from the path parameter
            updated_todo.id = todo_id
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a specific todo by ID"""
    global todos
    for index, item in enumerate(todos):
        if item.id == todo_id:
            del todos[index]
            return {"detail": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")


# --- 5. Simple Chat Endpoint (placeholder - AI agent integration would go here) ---
@app.get("/chat")
async def chat_with_agent(query: str):
    """Simple chat endpoint - placeholder for AI agent integration"""
    # For now, just echo back the query with a note about AI integration
    return {
        "response": f"You asked: '{query}'. AI agent integration coming soon!",
        "note": "AI agent functionality requires proper agent framework setup"
    }


# 6. Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Todo API is running"}


# 7. Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)