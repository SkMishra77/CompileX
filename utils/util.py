import hashlib
import random
import string
import time


def generateProblemId():
    # Generate a unique identifier based on epoch time
    epoch_time = str(int(time.time()))

    # Generate 12 random characters
    random_chars = ''.join(
        random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))

    # Combine all the components
    unique_string = f"{epoch_time}_{random_chars}"

    # Hash the unique string using SHA-256
    hash_object = hashlib.md5(unique_string.encode())
    hash_string = "p_" + hash_object.hexdigest()

    return hash_string
