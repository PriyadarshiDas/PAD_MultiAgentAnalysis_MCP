Download Ollama locally
pull ollama llm mode : ollama pull llama3
activate ollama = ollama serve

activate your env 
.\myenv\Scripts\Activate.ps1





uv init
uv add -r requirements.txt


if you want to add to docker
docker run -d -p 5000:5000 --add-host=host.docker.internal:host-gateway itsm-analysis
