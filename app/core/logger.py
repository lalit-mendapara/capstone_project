# Implements Decorators and Logging. It logs how long the AI takes to think.
import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AI_APP")

def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"Function {func.__name__} took {duration:.4f}s")
        return result
    return wrapper