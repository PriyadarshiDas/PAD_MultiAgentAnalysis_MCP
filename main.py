import requests

if __name__ == "__main__":
    user_activity = "User withdrew ₹5,00,000 in cash on a single day without any business justification."

    response = requests.post("http://localhost:8000/analyze", json={
        "banking_activity": user_activity
    })

    print(response.json())
