import os

JWT_SECRET_KEY_AMADEUS = os.environ.get("JWT_SECRET_KEY_AMADEUS", "")
JWT_DURATION_TOKEN_AMADEUS = os.environ.get("JWT_DURATION_TOKEN_AMADEUS", 130)
JWT_ALGORYTHM_TOKEN_AMADEUS = os.environ.get("JWT_ALGORYTHM_TOKEN_AMADEUS", "HS256")
