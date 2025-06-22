import requests
import json

if __name__ == "__main__":
    user_activity = "User sent 5,000,000,000 USD multiple times to a foreign account."

    try:
        response = requests.post("http://localhost:8000/analyze", json={
            "banking_activity": user_activity
        })

        print("Status Code:", response.status_code)

        # If response is JSON and status code is 200
        if response.status_code == 200:
            result = response.json()
            print("\n--- Analysis Result ---")
            print("Activity Summary:\n", result.get("activity_summary", "N/A"))
            print("\nRelevant Policy:\n", result.get("relevant_policy", "N/A"))
            print("\nDecision:\n", result.get("decision", "N/A"))
        else:
            print("Error Response:\n", response.text)

    except requests.exceptions.RequestException as e:
        print("HTTP Request failed:", e)
    except json.JSONDecodeError:
        print("Response was not valid JSON:\n", response.text)
