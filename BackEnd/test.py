# import secrets

# def generate_api_key(length: int = 32) -> str:
#     # Generate a secure random API key as a hexadecimal string
#     return secrets.token_hex(length)

# # Generate and print an API key
# api_key = generate_api_key(16)  # 16 bytes -> 32 hex characters
# print("Your API Key:", api_key)

def test(x):
    
    def test2(y):
        return "test2"
    
    return test2

print(test(1)(2))