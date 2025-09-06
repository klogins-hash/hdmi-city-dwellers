import weaviate
import asyncio
import logging
import os
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class WeaviateManager:
    def __init__(self):
        self.client = None
        self.url = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
        self.api_key = os.getenv("WEAVIATE_API_KEY")
        
    async def initialize(self):
        """Initialize Weaviate client and setup schema"""
        try:
            self.client = weaviate.Client(
                url=self.url,
                auth_client_secret=weaviate.AuthApiKey(self.api_key),
                timeout_config=(10, 30),
            )
            
            # Test connection
            await asyncio.to_thread(self.client.schema.get)
            logger.info("Weaviate client initialized successfully")
            
            # Setup schema
            await self.setup_schema()
            
        except Exception as e:
            logger.error(f"Failed to initialize Weaviate client: {e}")
            raise
    
    async def setup_schema(self):
        """Setup basic knowledge base schema"""
        try:
            schema = await asyncio.to_thread(self.client.schema.get)
            classes = [cls["class"] for cls in schema.get("classes", [])]
            
            if "KnowledgeBase" not in classes:
                kb_schema = {
                    "class": "KnowledgeBase",
                    "vectorizer": "text2vec-openai",
                    "properties": [
                        {
                            "name": "title",
                            "dataType": ["string"],
                            "indexFilterable": True,
                            "indexSearchable": True
                        },
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "indexFilterable": False,
                            "indexSearchable": True
                        },
                        {
                            "name": "category",
                            "dataType": ["string"],
                            "indexFilterable": True,
                            "indexSearchable": True
                        },
                        {
                            "name": "created_at",
                            "dataType": ["date"],
                            "indexFilterable": True,
                            "indexSearchable": False
                        },
                        {
                            "name": "updated_at",
                            "dataType": ["date"],
                            "indexFilterable": True,
                            "indexSearchable": False
                        },
                        {
                            "name": "tags",
                            "dataType": ["string[]"],
                            "indexFilterable": True,
                            "indexSearchable": True
                        }
                    ]
                }
                
                await asyncio.to_thread(self.client.schema.create_class, kb_schema)
                logger.info("Created KnowledgeBase schema")
            
        except Exception as e:
            logger.error(f"Failed to setup schema: {e}")
            raise
    
    async def search(self, query: str, limit: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search the knowledge base"""
        try:
            def _search():
                query_builder = (
                    self.client.query
                    .get("KnowledgeBase", ["title", "content", "category", "created_at", "tags"])
                    .with_near_text({"concepts": [query], "certainty": 0.6})
                    .with_limit(limit)
                    .with_additional(["certainty", "id"])
                )
                
                if category:
                    query_builder = query_builder.with_where({
                        "path": ["category"],
                        "operator": "Equal",
                        "valueString": category
                    })
                
                return query_builder.do()
            
            result = await asyncio.to_thread(_search)
            items = result.get('data', {}).get('Get', {}).get('KnowledgeBase', [])
            return items
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    async def add_knowledge(self, title: str, content: str, category: str = "general", tags: List[str] = None) -> bool:
        """Add new knowledge to the database"""
        try:
            if tags is None:
                tags = []
                
            def _add():
                return self.client.data_object.create(
                    data_object={
                        "title": title,
                        "content": content,
                        "category": category,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                        "tags": tags
                    },
                    class_name="KnowledgeBase"
                )
            
            result = await asyncio.to_thread(_add)
            logger.info(f"Added knowledge: {title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add knowledge: {e}")
            return False
    
    async def update_knowledge(self, object_id: str, title: str = None, content: str = None, category: str = None, tags: List[str] = None) -> bool:
        """Update existing knowledge"""
        try:
            update_data = {"updated_at": datetime.now().isoformat()}
            
            if title is not None:
                update_data["title"] = title
            if content is not None:
                update_data["content"] = content
            if category is not None:
                update_data["category"] = category
            if tags is not None:
                update_data["tags"] = tags
            
            def _update():
                return self.client.data_object.update(
                    data_object=update_data,
                    class_name="KnowledgeBase",
                    uuid=object_id
                )
            
            await asyncio.to_thread(_update)
            logger.info(f"Updated knowledge: {object_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update knowledge: {e}")
            return False
    
    async def delete_knowledge(self, object_id: str) -> bool:
        """Delete knowledge by ID"""
        try:
            def _delete():
                return self.client.data_object.delete(
                    uuid=object_id,
                    class_name="KnowledgeBase"
                )
            
            await asyncio.to_thread(_delete)
            logger.info(f"Deleted knowledge: {object_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete knowledge: {e}")
            return False
    
    async def list_all(self, limit: int = 20, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all knowledge entries"""
        try:
            def _list():
                query_builder = (
                    self.client.query
                    .get("KnowledgeBase", ["title", "content", "category", "created_at", "tags"])
                    .with_limit(limit)
                    .with_additional(["id"])
                )
                
                if category:
                    query_builder = query_builder.with_where({
                        "path": ["category"],
                        "operator": "Equal",
                        "valueString": category
                    })
                
                return query_builder.do()
            
            result = await asyncio.to_thread(_list)
            items = result.get('data', {}).get('Get', {}).get('KnowledgeBase', [])
            return items
            
        except Exception as e:
            logger.error(f"List error: {e}")
            return []
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            def _get_stats():
                # Get total count
                result = self.client.query.aggregate("KnowledgeBase").with_meta_count().do()
                total_count = result.get('data', {}).get('Aggregate', {}).get('KnowledgeBase', [{}])[0].get('meta', {}).get('count', 0)
                
                # Get categories
                category_result = self.client.query.aggregate("KnowledgeBase").with_group_by_filter(["category"]).do()
                
                return {
                    "total_entries": total_count,
                    "schema_classes": len(self.client.schema.get().get("classes", [])),
                    "timestamp": datetime.now().isoformat()
                }
            
            return await asyncio.to_thread(_get_stats)
            
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {"error": str(e)}
    
    async def get_schema(self) -> Dict[str, Any]:
        """Get current schema"""
        try:
            def _get_schema():
                return self.client.schema.get()
            
            return await asyncio.to_thread(_get_schema)
            
        except Exception as e:
            logger.error(f"Schema error: {e}")
            return {"error": str(e)}
    
    async def browse_data(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """Browse database contents with pagination"""
        try:
            def _browse():
                return (
                    self.client.query
                    .get("KnowledgeBase", ["title", "content", "category", "created_at", "tags"])
                    .with_limit(limit)
                    .with_offset(offset)
                    .with_additional(["id"])
                    .do()
                )
            
            result = await asyncio.to_thread(_browse)
            items = result.get('data', {}).get('Get', {}).get('KnowledgeBase', [])
            
            return {
                "items": items,
                "limit": limit,
                "offset": offset,
                "count": len(items)
            }
            
        except Exception as e:
            logger.error(f"Browse error: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> str:
        """Check Weaviate health"""
        try:
            await asyncio.to_thread(self.client.schema.get)
            return "connected"
        except:
            return "disconnected"
    
    async def close(self):
        """Close Weaviate client"""
        pass
