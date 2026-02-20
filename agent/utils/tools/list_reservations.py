from langchain_core.tools import tool

@tool
def list_reservations()->str:
    """Get all reservations available"""
    return "15:00 A, 16:00 B"