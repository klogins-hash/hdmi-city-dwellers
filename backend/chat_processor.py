import re
import logging
from typing import Dict, Any, List, Optional
import aioredis
import os

from weaviate_manager import WeaviateManager

logger = logging.getLogger(__name__)

class ChatProcessor:
    def __init__(self, weaviate_manager: WeaviateManager):
        self.weaviate = weaviate_manager
        self.redis = None
        
        # Command patterns
        self.commands = {
            'add': r'^add:\s*(.+?)\s*\|\s*(.+?)(?:\s*\|\s*(.+?))?$',
            'delete': r'^delete:\s*(.+)$',
            'update': r'^update:\s*(.+?)\s*\|\s*(.+)$',
            'list': r'^list(?:\s+(.+))?$',
            'stats': r'^(?:show\s+)?stats?|database\s+info$',
            'help': r'^help$',
            'clear': r'^clear(?:\s+(.+))?$'
        }
    
    async def initialize(self):
        """Initialize chat processor"""
        try:
            self.redis = aioredis.from_url(
                os.getenv("REDIS_URL", "redis://redis:6379"),
                encoding="utf-8",
                decode_responses=True,
                max_connections=10
            )
            await self.redis.ping()
            logger.info("Chat processor initialized")
        except Exception as e:
            logger.warning(f"Redis not available: {e}")
            self.redis = None
    
    async def process_message(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """Process incoming message - either command or search query"""
        message = message.strip()
        
        # Check if it's a command
        command_result = await self.process_command(message)
        if command_result:
            return command_result
        
        # Otherwise, treat as search query
        return await self.process_search(message, session_id)
    
    async def process_command(self, message: str) -> Optional[Dict[str, Any]]:
        """Process database management commands"""
        message_lower = message.lower()
        
        # Add command: add: title | content | category
        if match := re.match(self.commands['add'], message, re.IGNORECASE):
            title = match.group(1).strip()
            content = match.group(2).strip()
            category = match.group(3).strip() if match.group(3) else "general"
            
            success = await self.weaviate.add_knowledge(title, content, category)
            
            if success:
                return {
                    "response": f"✅ Successfully added '{title}' to the HDMI City Dwellers knowledge base in category '{category}'.",
                    "action": "add",
                    "data_modified": True
                }
            else:
                return {
                    "response": "❌ Failed to add knowledge to the database.",
                    "action": "add_failed",
                    "data_modified": False
                }
        
        # Delete command: delete: search term
        elif match := re.match(self.commands['delete'], message, re.IGNORECASE):
            search_term = match.group(1).strip()
            
            # First, search for items to delete
            items = await self.weaviate.search(search_term, limit=5)
            
            if not items:
                return {
                    "response": f"❌ No items found matching '{search_term}' to delete.",
                    "action": "delete_not_found",
                    "data_modified": False
                }
            
            # Delete the first match (most relevant)
            item_id = items[0]['_additional']['id']
            item_title = items[0]['title']
            
            success = await self.weaviate.delete_knowledge(item_id)
            
            if success:
                return {
                    "response": f"✅ Successfully deleted '{item_title}' from the knowledge base.",
                    "action": "delete",
                    "data_modified": True
                }
            else:
                return {
                    "response": f"❌ Failed to delete '{item_title}' from the database.",
                    "action": "delete_failed",
                    "data_modified": False
                }
        
        # Update command: update: search term | new content
        elif match := re.match(self.commands['update'], message, re.IGNORECASE):
            search_term = match.group(1).strip()
            new_content = match.group(2).strip()
            
            # Search for item to update
            items = await self.weaviate.search(search_term, limit=1)
            
            if not items:
                return {
                    "response": f"❌ No items found matching '{search_term}' to update.",
                    "action": "update_not_found",
                    "data_modified": False
                }
            
            item_id = items[0]['_additional']['id']
            item_title = items[0]['title']
            
            success = await self.weaviate.update_knowledge(item_id, content=new_content)
            
            if success:
                return {
                    "response": f"✅ Successfully updated '{item_title}' in the knowledge base.",
                    "action": "update",
                    "data_modified": True
                }
            else:
                return {
                    "response": f"❌ Failed to update '{item_title}' in the database.",
                    "action": "update_failed",
                    "data_modified": False
                }
        
        # List command: list or list category
        elif match := re.match(self.commands['list'], message, re.IGNORECASE):
            category = match.group(1).strip() if match.group(1) else None
            
            if category and category.lower() == "all":
                category = None
            
            items = await self.weaviate.list_all(limit=10, category=category)
            
            if not items:
                category_text = f" in category '{category}'" if category else ""
                return {
                    "response": f"📋 No items found{category_text}.",
                    "action": "list_empty",
                    "data_modified": False
                }
            
            response_lines = [f"📋 HDMI City Dwellers Knowledge Base{f' (Category: {category})' if category else ''}:\n"]
            
            for i, item in enumerate(items, 1):
                title = item.get('title', 'Untitled')
                category_name = item.get('category', 'general')
                content_preview = item.get('content', '')[:100] + "..." if len(item.get('content', '')) > 100 else item.get('content', '')
                response_lines.append(f"{i}. **{title}** ({category_name})")
                response_lines.append(f"   {content_preview}\n")
            
            return {
                "response": "\n".join(response_lines),
                "action": "list",
                "data_modified": False
            }
        
        # Stats command
        elif re.match(self.commands['stats'], message, re.IGNORECASE):
            stats = await self.weaviate.get_database_stats()
            
            if "error" in stats:
                return {
                    "response": f"❌ Error getting database stats: {stats['error']}",
                    "action": "stats_error",
                    "data_modified": False
                }
            
            response = f"""📊 **HDMI City Dwellers Database Statistics**

📚 Total Entries: {stats.get('total_entries', 0)}
🏗️ Schema Classes: {stats.get('schema_classes', 0)}
🕒 Last Updated: {stats.get('timestamp', 'Unknown')}

Use 'list all' to see all entries or 'list category_name' to filter by category."""
            
            return {
                "response": response,
                "action": "stats",
                "data_modified": False
            }
        
        # Help command
        elif re.match(self.commands['help'], message, re.IGNORECASE):
            help_text = """🤖 **HDMI City Dwellers Knowledge Base Commands:**

**Search & Query:**
• Just type your question naturally to search the knowledge base

**Database Management:**
• `add: title | content | category` - Add new knowledge
• `delete: search term` - Delete matching entry
• `update: search term | new content` - Update existing entry
• `list` or `list all` - Show all entries
• `list category_name` - Show entries in specific category
• `stats` - Show database statistics
• `help` - Show this help message

**Examples:**
• `add: HDMI 2.1 | Latest HDMI standard with 48Gbps bandwidth | technology`
• `delete: HDMI 2.1`
• `update: HDMI 2.1 | HDMI 2.1 supports 8K video and enhanced gaming features`
• `list technology`

**Categories:**
• technology, urban-planning, connectivity, infrastructure, smart-city"""
            
            return {
                "response": help_text,
                "action": "help",
                "data_modified": False
            }
        
        # Clear command (clear cache)
        elif match := re.match(self.commands['clear'], message, re.IGNORECASE):
            if self.redis:
                try:
                    await self.redis.flushdb()
                    return {
                        "response": "🧹 Cache cleared successfully.",
                        "action": "clear_cache",
                        "data_modified": False
                    }
                except Exception as e:
                    return {
                        "response": f"❌ Failed to clear cache: {e}",
                        "action": "clear_cache_failed",
                        "data_modified": False
                    }
            else:
                return {
                    "response": "ℹ️ No cache to clear (Redis not available).",
                    "action": "no_cache",
                    "data_modified": False
                }
        
        return None  # Not a command
    
    async def process_search(self, query: str, session_id: str) -> Dict[str, Any]:
        """Process search query"""
        # Check cache first
        cache_key = f"search:{hash(query.lower())}"
        cached_result = None
        
        if self.redis:
            try:
                cached_result = await self.redis.get(cache_key)
            except:
                pass
        
        if cached_result:
            return {
                "response": cached_result,
                "action": "search_cached",
                "data_modified": False
            }
        
        # Search Weaviate
        items = await self.weaviate.search(query, limit=3)
        
        if not items:
            response = f"🔍 I couldn't find any information about '{query}' in the HDMI City Dwellers knowledge base.\n\nTry:\n• Using different keywords\n• Adding information with: `add: title | content | category`\n• Type 'help' for more commands"
        else:
            response_parts = [f"🔍 **Found {len(items)} result(s) for '{query}' in HDMI City Dwellers:**\n"]
            
            for i, item in enumerate(items, 1):
                title = item.get('title', 'Untitled')
                content = item.get('content', 'No content')
                category = item.get('category', 'general')
                certainty = item.get('_additional', {}).get('certainty', 0)
                
                response_parts.append(f"**{i}. {title}** ({category}) - {certainty:.2f} match")
                response_parts.append(f"{content}\n")
            
            response = "\n".join(response_parts)
        
        # Cache result
        if self.redis:
            try:
                await self.redis.setex(cache_key, 3600, response)  # 1 hour cache
            except:
                pass
        
        return {
            "response": response,
            "action": "search",
            "data_modified": False
        }
