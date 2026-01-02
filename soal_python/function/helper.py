import random
import string
from datetime import datetime


def generateNodeId():
    """Menghasilkan ID dengan format NODE-(5 Karakter Alphanumeric)"""
    chars = string.ascii_letters + string.digits
    random_id = "".join(random.choice(chars) for _ in range(5))
    return f"NODE-{random_id}"


def formatResponse(status, message, data=None):
    """Format standar JSON response"""
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else []
    }