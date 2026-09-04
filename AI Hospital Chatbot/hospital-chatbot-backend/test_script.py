import requests
import sys
import uuid

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def print_step(msg):
    print(f"--- {msg} ---")

def run_tests():
    try:
        # Generate random user credentials
        random_id = str(uuid.uuid4())[:8]
        username = f"user_{random_id}"
        email = f"user_{random_id}@example.com"
        
        # 1. Register user
        print_step("Registering User")
        user_data = {"username": username, "email": email, "password": "password123", "full_name": "Test User"}
        r = requests.post(f"{API_URL}/auth/register", json=user_data)
        print(f"Status: {r.status_code}")
        
        # 2. Login
        print_step("Login User")
        login_data = {"username": username, "password": "password123"}
        r = requests.post(f"{API_URL}/auth/login", data=login_data)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            token = r.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # 3. Create conversation
            print_step("Create Conversation")
            conv_data = {"title": "Test Chat"}
            r = requests.post(f"{API_URL}/chatbot/conversations", json=conv_data, headers=headers)
            print(f"Status: {r.status_code}")
            
            if r.status_code in [200, 201]:
                conv_id = r.json().get("id")
                
                # 4. Send message
                print_step("Send Message")
                msg_data = {"conversation_id": conv_id, "message": "What is HealthSync?"}
                r = requests.post(f"{API_URL}/chatbot/chat", json=msg_data, headers=headers)
                print(f"Status: {r.status_code}")
                # We expect a streaming response, let's just read it all
                print(r.text)

                # 5. Retrieve history
                print_step("Retrieve History")
                r = requests.get(f"{API_URL}/chatbot/conversations/{conv_id}", headers=headers)
                print(f"Status: {r.status_code}")
                print(r.text[:200] + "...") # truncate
                
                # 6. Create second conversation to ensure no duplicate error
                print_step("Create Second Conversation")
                conv_data_2 = {"title": "Second Chat"}
                r = requests.post(f"{API_URL}/chatbot/conversations", json=conv_data_2, headers=headers)
                print(f"Status: {r.status_code}")
        else:
            print("Login failed, skipping chat tests.")

    except Exception as e:
        print(f"Error during tests: {e}")

if __name__ == "__main__":
    run_tests()
