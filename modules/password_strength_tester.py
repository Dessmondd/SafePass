from zxcvbn import zxcvbn

def test_password(password):

    result = zxcvbn(password)

    return {
        "score": result["score"],  # Password strength score (0-4)
        "feedback": result["feedback"]["suggestions"],  # List of feedback suggestions
    }
