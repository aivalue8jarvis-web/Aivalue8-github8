import time
import random

def human_like_delay(action_type: str = "email"):
    """Introduces organic human latency, reading time, and typing simulation pauses to bypass bot detectors."""
    if action_type == "email":
        # Simulate reading the incoming inquiry + thinking + typing out response (12 to 35 seconds)
        delay = random.uniform(12.0, 35.0)
    elif action_type == "whatsapp" or action_type == "message":
        # Simulate quick human chat response (4 to 12 seconds)
        delay = random.uniform(4.0, 12.0)
    elif action_type == "scan":
        # Slow, methodical turtle walk scanning pacing
        delay = random.uniform(2.0, 5.0)
    else:
        delay = random.uniform(3.0, 8.0)
        
    time.sleep(delay)
    return delay

def apply_human_pacing(func):
    """Decorator to wrap automated tasks with organic human execution rhythm."""
    def wrapper(*args, **kwargs):
        human_like_delay("scan")
        return func(*args, **kwargs)
    return wrapper
