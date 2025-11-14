from fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults  
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "MCP Application",
)

client = DuckDuckGoSearchResults(output_format="list")

class QueryStruct(BaseModel):
    query: str

@mcp.tool(name="linkedin_search", description="Search LinkedIn for professionals based on a query.")
def linkedin_search(query: QueryStruct) -> list:
    '''  Search LinkedIn for professionals based on a query. '''

    print(f"Received query: {query}")

    if query == "": return "No query provided."

    res = client.invoke(query)

    result = []

    for r in res:
        result.append(r.get("link"))

    return result




if __name__ == "__main__":
    mcp.run("streamable-http", host="0.0.0.0", port=8080)