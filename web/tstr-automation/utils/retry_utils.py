import time
import logging
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    **kwargs: Any
) -> Any:
    """
    Execute a function with exponential backoff retry logic.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Factor to multiply delay by each retry
        **kwargs: Arguments to pass to the function
    
    Returns:
        The result of the function if successful
    
    Example:
        def fetch_page(url):
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        
        # Retry up to 5 times with exponential backoff
        content = retry_with_backoff(fetch_page, max_retries=5, url="https://example.com")
    """
    for attempt in range(max_retries):
        try:
            return func(**kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                # Final attempt failed, raise the exception
                logging.error(f"Final retry failed: {e}")
                raise
            # Calculate delay with exponential backoff
            delay = min(max_delay, initial_delay * (backoff_factor ** attempt))
            logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s.")
            time.sleep(delay)