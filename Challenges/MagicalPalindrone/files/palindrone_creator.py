import random
import string

random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=500))
palindrone = random_string + random_string[::-1]
print(palindrone)