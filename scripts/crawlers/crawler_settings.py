import httpx
from typing import Optional, Dict, Callable

def crawler_settings(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    user_agent: Optional[str] = None,  # Added user-agent
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    follow_redirects: bool = True,
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """
    Decorator to set crawler properties for a function.

    Args:
        base_url: The base URL for the website being scraped.
        headers: Default HTTP headers to use for all requests.
        user_agent: Optional user agent string.  If provided, it overrides
            any User-Agent in the headers.
        timeout: The timeout for each HTTP request in seconds.
        max_retries: Maximum number of times to retry a failed request.
        retry_delay: Delay in seconds between retries.
        follow_redirects: Whether to follow HTTP redirects.

    Returns:
        A decorator that modifies the function.
    """
    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        """
        The actual decorator function that modifies the decorated function.
        """
        async def wrapper(*args, **kwargs):
            """
            Wrapper function that adds crawler functionality.
            """
            final_headers = headers.copy() if headers else {}
            if user_agent:  # Override or set User-Agent
                final_headers["User-Agent"] = user_agent

            async with httpx.AsyncClient(
                base_url=base_url,
                headers=final_headers,
                timeout=timeout,
                follow_redirects=follow_redirects,
                ) as client:
                # Add the client and settings to the function's local scope
                # so they can be used within the decorated function.
                kwargs['client'] = client
                kwargs['crawler_settings'] = {  # Pass settings as a dict
                    'max_retries': max_retries,
                    'retry_delay': retry_delay,
                }
                await func(*args, **kwargs)  # Call the original function
        return wrapper
    return decorator