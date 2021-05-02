from secrets import token_urlsafe


def generate_random_url(num_bytes=10):
    return token_urlsafe(nbytes=num_bytes)
