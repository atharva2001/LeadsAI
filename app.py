from fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults  
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

mcp_server = FastMCP(
    "MCP Application",
)

client = DuckDuckGoSearchResults(output_format="list")

@mcp_server.tool(name="linkedin_search", description="Search LinkedIn for professionals based on a query.")
def linkedin_search(query: str = "") -> list:
    '''  Search LinkedIn for professionals based on a query.'''

    if query == "": return "No query provided."

    res = client.invoke(query)

    result = []

    for r in res:
        result.append(r.get("link"))

    return result




if __name__ == "__main__":
    mcp_server.run("streamable-http", host="0.0.0.0", port=8080)