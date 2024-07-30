import requests
# Patch pythons default stdout behavior
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

# TODO: Tohle jsou jenom placeholdery, zmen je na realne hodnoty aby fungovaly s tvym ollama serverem
ollama_url = "http://localhost:11434/api/generate"
model_name = "llama3"
message_for_model = "Hey I got new request for you, can you check it? Just reply with word Hello"

def parse_methods(user_method_input: str):
    if "POST" in user_method_input:
        return "POST"
    elif "GET" in user_method_input:
        return "GET"
    elif "PUT" in user_method_input:
        return "PUT"
    elif "DELETE" in user_method_input:
        return "DELETE"
    else:
        return "GET"
def firewall_check(method: str, url: str, user_data: str | None=None):
    ollama_chat = message_for_model + "->" + method + "; " + url
    if user_data != None:
        ollama_chat += "; request data: " + user_data
    
    # Send request to Ollama
    data = {
        "model": model_name,
        "prompt": ollama_chat,
        "stream": False
    }
    print("Request data: ", data)
    print("Sending request to Ollama...")
    resp = requests.post(ollama_url, json=data)
    resp_json = resp.json()
    # For debugging purposes
    print(f"Ollama server responded with: {resp_json["response"]}")
    # TODO: Naimplemetujte kontrolu zda-li Ollama povoluje request
    # Zatim placeholder, vraci True 
    return True
def send_request(method: str, url: str, user_data: str | None=None):
    if method == "GET":
        response = requests.get(url, data=user_data)
    elif method == "POST":
        response = requests.post(url, data=user_data)
    elif method == "PUT":
        response = requests.put(url, data=user_data)    
    elif method == "DELETE":
        response = requests.delete(url, data=user_data)
    else:
        response = requests.get(url, data=user_data)
    return response
def parse_input(user_input: str):
    try:
        method = parse_methods(user_input.split(" ")[0])
        url = user_input.split(" ")[1]
    except IndexError:
        print("Invalid input")
        return None, None, None
    try:
        data = user_input.split(" ")[2]
    except:
        data = None
    return method, url, data
def main():
    session = PromptSession()
    with patch_stdout():
        while True:
            try:
                user_input = session.prompt(">> ")
                if user_input == "exit":
                    break
                if user_input == "":
                    continue
                if user_input == "help":
                    print("Commands: \nexit - exit the program\nhelp - show this message\nclear - clear the screen")
                    print("Usage: [METHOD] [URL] [DATA]")
                    print("Example: GET http://localhost:8000/api/data {\"key\": \"value\"}")
                    continue
                if user_input == "clear":
                    print("\033c")
                    continue
                method, url, data = parse_input(user_input)
                if method == None or url == None:
                    continue
                firewall_result = firewall_check(method, url, data)
                if firewall_result:
                    print("Firewall cehck passed, sending request!")
                    response = send_request(method, url, data)
                    print(response.text)
                else:
                    print("Request blocked by firewall")
            except KeyboardInterrupt:
                print("Exiting...")
                break

if __name__ == "__main__":
    main()