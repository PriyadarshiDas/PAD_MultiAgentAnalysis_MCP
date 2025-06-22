import requests

if __name__ == "__main__":
    user_activity = "User uses his credit card to make a purchase of $150 at an online store."

    response = requests.post("http://localhost:8000/analyze", json={
        "banking_activity": user_activity
    })

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
