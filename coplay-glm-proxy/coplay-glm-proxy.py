#!/usr/bin/env python3
"""
Coplay GLM Proxy Server
Redirects Coplay's OpenAI-compatible API calls to GLM API
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
import aiohttp
from aiohttp import web, ClientSession
import sys

# Configuration
GLM_BASE_URL = "https://api.z.ai/api/coding/paas/v4"
GLM_API_KEY = "df92b900aac94a60b659c341d9054464.PkbniOA3fCgPCtlu"
DEFAULT_MODEL = "glm-4.6"
PROXY_PORT = 8080

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CoplayGLMProxy:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        
    async def start_session(self):
        """Initialize aiohttp session"""
        self.session = ClientSession()
        
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def translate_openai_to_glm(self, openai_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate OpenAI-compatible request to GLM API format
        """
        glm_request = {
            "model": openai_request.get("model", DEFAULT_MODEL),
            "messages": openai_request.get("messages", []),
            "stream": openai_request.get("stream", False),
        }
        
        # Add optional parameters if present
        if "temperature" in openai_request:
            glm_request["temperature"] = openai_request["temperature"]
        if "max_tokens" in openai_request:
            glm_request["max_tokens"] = openai_request["max_tokens"]
        if "top_p" in openai_request:
            glm_request["top_p"] = openai_request["top_p"]
            
        # Handle function calling if present
        if "functions" in openai_request:
            glm_request["functions"] = openai_request["functions"]
        if "function_call" in openai_request:
            glm_request["function_call"] = openai_request["function_call"]
            
        logger.info(f"Translated request: {json.dumps(glm_request, indent=2)}")
        return glm_request
    
    def translate_glm_to_openai(self, glm_response: Dict[str, Any], stream: bool = False) -> Dict[str, Any]:
        """
        Translate GLM API response back to OpenAI-compatible format
        """
        if stream:
            # Handle streaming response
            return glm_response
        
        openai_response = {
            "id": glm_response.get("id", "chatcmpl-" + str(hash(str(glm_response)))),
            "object": "chat.completion",
            "created": glm_response.get("created", 0),
            "model": glm_response.get("model", DEFAULT_MODEL),
            "choices": [],
            "usage": glm_response.get("usage", {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            })
        }
        
        # Translate choices
        if "choices" in glm_response:
            for choice in glm_response["choices"]:
                openai_choice = {
                    "index": choice.get("index", 0),
                    "finish_reason": choice.get("finish_reason", "stop"),
                    "message": choice.get("message", {})
                }
                openai_response["choices"].append(openai_choice)
        
        logger.info(f"Translated response: {json.dumps(openai_response, indent=2)}")
        return openai_response
    
    async def proxy_chat_completions(self, request: web.Request) -> web.Response:
        """
        Proxy chat completions endpoint
        """
        try:
            # Get request data
            openai_request = await request.json()
            logger.info(f"Received OpenAI request: {json.dumps(openai_request, indent=2)}")
            
            # Translate to GLM format
            glm_request = self.translate_openai_to_glm(openai_request)
            
            # Get authorization header
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                auth_header = f"Bearer {GLM_API_KEY}"
            else:
                # Use provided key or override with our GLM key
                auth_header = f"Bearer {GLM_API_KEY}"
            
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "User-Agent": "Coplay-GLM-Proxy/1.0"
            }
            
            # Make request to GLM API
            async with self.session.post(
                f"{GLM_BASE_URL}/chat/completions",
                json=glm_request,
                headers=headers
            ) as glm_response:
                response_text = await glm_response.text()
                logger.info(f"GLM response status: {glm_response.status}")
                logger.info(f"GLM response: {response_text}")
                
                if glm_response.status == 200:
                    # Parse GLM response
                    glm_data = json.loads(response_text)
                    
                    # Handle streaming
                    if glm_request.get("stream", False):
                        # For streaming, we need to handle SSE format
                        return web.Response(
                            body=response_text,
                            status=200,
                            headers={
                                "Content-Type": "text/event-stream",
                                "Cache-Control": "no-cache",
                                "Connection": "keep-alive"
                            }
                        )
                    else:
                        # Translate back to OpenAI format
                        openai_response = self.translate_glm_to_openai(glm_data)
                        return web.json_response(openai_response)
                else:
                    # Return error response
                    error_response = {
                        "error": {
                            "message": f"GLM API Error: {response_text}",
                            "type": "glm_api_error",
                            "code": glm_response.status
                        }
                    }
                    return web.json_response(error_response, status=glm_response.status)
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return web.json_response({
                "error": {
                    "message": f"Invalid JSON in request: {str(e)}",
                    "type": "json_decode_error"
                }
            }, status=400)
            
        except Exception as e:
            logger.error(f"Proxy error: {str(e)}")
            return web.json_response({
                "error": {
                    "message": f"Proxy server error: {str(e)}",
                    "type": "proxy_error"
                }
            }, status=500)
    
    async def proxy_models(self, request: web.Request) -> web.Response:
        """
        Proxy models endpoint to return GLM model info in OpenAI format
        """
        models_response = {
            "object": "list",
            "data": [
                {
                    "id": DEFAULT_MODEL,
                    "object": "model",
                    "created": 1677610602,
                    "owned_by": "glm"
                }
            ]
        }
        return web.json_response(models_response)
    
    async def health_check(self, request: web.Request) -> web.Response:
        """
        Health check endpoint
        """
        return web.json_response({
            "status": "healthy",
            "service": "Coplay GLM Proxy",
            "target_api": GLM_BASE_URL,
            "model": DEFAULT_MODEL
        })

async def create_app() -> web.Application:
    """
    Create and configure the aiohttp application
    """
    proxy = CoplayGLMProxy()
    await proxy.start_session()
    
    app = web.Application()
    
    # Register routes
    app.router.add_post("/v1/chat/completions", proxy.proxy_chat_completions)
    app.router.add_get("/v1/models", proxy.proxy_models)
    app.router.add_get("/health", proxy.health_check)
    
    # Add cleanup
    app.on_cleanup.append(lambda app: proxy.close_session())
    
    return app

async def main():
    """
    Main function to start the proxy server
    """
    logger.info("Starting Coplay GLM Proxy Server...")
    logger.info(f"GLM API URL: {GLM_BASE_URL}")
    logger.info(f"Default Model: {DEFAULT_MODEL}")
    logger.info(f"Proxy Port: {PROXY_PORT}")
    
    app = await create_app()
    
    # Start the server
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, "localhost", PROXY_PORT)
    await site.start()
    
    logger.info(f"Proxy server running on http://localhost:{PROXY_PORT}")
    logger.info("Configure Coplay with:")
    logger.info(f"  OpenAI Base URL: http://localhost:{PROXY_PORT}/v1")
    logger.info(f"  API Key: {GLM_API_KEY}")
    logger.info(f"  Model Name: {DEFAULT_MODEL}")
    
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down proxy server...")
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProxy server stopped.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
