from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import time
from typing import Optional, List, Dict, Any

from weaviate_manager import WeaviateManager
from chat_processor import ChatProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HDMI City Dwellers Knowledge Base", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
weaviate_manager = WeaviateManager()
chat_processor = ChatProcessor(weaviate_manager)

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    processing_time: float
    timestamp: float
    action_performed: Optional[str] = None
    data_modified: bool = False

@app.on_startup
async def startup():
    """Initialize services"""
    await weaviate_manager.initialize()
    await chat_processor.initialize()
    logger.info("HDMI City Dwellers services initialized")

@app.on_shutdown
async def shutdown():
    """Cleanup services"""
    await weaviate_manager.close()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Main chat endpoint - handles both queries and database commands"""
    start_time = time.time()
    
    try:
        result = await chat_processor.process_message(message.message, message.session_id)
        
        processing_time = time.time() - start_time
        logger.info(f"Message processed in {processing_time:.3f}s")
        
        return ChatResponse(
            response=result["response"],
            processing_time=processing_time,
            timestamp=time.time(),
            action_performed=result.get("action"),
            data_modified=result.get("data_modified", False)
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/database/stats")
async def get_database_stats():
    """Get database statistics"""
    try:
        stats = await weaviate_manager.get_database_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get database stats")

@app.get("/api/database/schema")
async def get_schema():
    """Get current database schema"""
    try:
        schema = await weaviate_manager.get_schema()
        return schema
    except Exception as e:
        logger.error(f"Error getting schema: {e}")
        raise HTTPException(status_code=500, detail="Failed to get schema")

@app.get("/api/database/browse")
async def browse_data(limit: int = 10, offset: int = 0):
    """Browse database contents"""
    try:
        data = await weaviate_manager.browse_data(limit, offset)
        return data
    except Exception as e:
        logger.error(f"Error browsing data: {e}")
        raise HTTPException(status_code=500, detail="Failed to browse data")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "HDMI City Dwellers",
        "weaviate": await weaviate_manager.health_check(),
        "timestamp": time.time()
    }

@app.get("/")
async def root():
    """Root endpoint with usage instructions"""
    return {
        "message": "HDMI City Dwellers Knowledge Base",
        "version": "1.0.0",
        "description": "AI-powered knowledge management system for urban technology insights",
        "usage": {
            "chat": "POST /api/chat with {'message': 'your message'}",
            "commands": [
                "Search: 'find information about X'",
                "Add: 'add: title | content | category'", 
                "Delete: 'delete: search term'",
                "Update: 'update: search term | new content'",
                "List: 'list all' or 'list category X'",
                "Stats: 'show stats' or 'database info'"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
