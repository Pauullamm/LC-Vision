from langchain_community.tools.tavily_search import TavilySearchResults
import os

tool = TavilySearchResults()

print(tool.invoke())