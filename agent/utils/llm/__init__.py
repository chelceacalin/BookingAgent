from .llm import baseLLM
from ..tools import *

llm = baseLLM.bind_tools(tools)
__all__ = ["llm"]