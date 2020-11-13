class RateLimitException(Exception):
    """HTTP 429: Too Many Requests. This is a rate limit problem."""


class InvalidCredentialsException(Exception):
    """Invalid username or password."""


class CaptchaRequiredException(Exception):
    """Captcha warning triggered, unable to login."""
