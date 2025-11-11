# from fastapi import FastAPI
# from MCP_Application.app import mcp_server
# import uvicorn

# app = FastAPI(
#     title="Fast MCP Leader",
#     description="A FastAPI application to fetch Leads for recruiters.",
#     version="0.0.1"
# )

# mcp_app = mcp_server.http_app()

# app.mount("/mcp")

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to Fast MCP Leader!"}

# if __name__ == "__main__":
#     uvicorn.run(
#         "app:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import asyncio
import httpx

load_dotenv()

cust_client = httpx.Client(verify=False)

llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        temperature=0.0,
        api_key=os.environ["GEMINI_API_KEY"],   
    )

async def main():
    
    try:
        mcp_client = MultiServerMCPClient(
            {
                "playwright": {
                    "url": "http://localhost:8931/mcp",
                    "transport": "streamable_http",
                },

                "Linkedin_MCP": {
                    "url": "http://localhost:8080/mcp",
                    "transport": "streamable_http",
                }
            },
        )

        message = "Find me 5 Python develier."

        prompt = "You are an expert lead generator. Use the MCP tools to get leads based on user queries."

        tools = await mcp_client.get_tools()

        llm.bind_tools(tools)

        # print("Available tools:")
        # for tool in tools:
        #     print(f"  - {tool.name}: {tool.description}")

        res = llm.invoke("" + prompt + "\n" + message)

        print("Final Response: ", res)

    except Exception as e:
        print("Error: ", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    
    asyncio.run(main())