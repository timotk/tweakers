class RateLimitException(Exception):
    """HTTP 429: Too Many Requests. This is a rate limit problem."""
