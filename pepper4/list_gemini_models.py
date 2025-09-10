import google.generativeai

API_KEY = "AIzaSyC0gaUvUcl558V8OoP-g5z7AKDXvcBcHqw"

def list_models():
    google.generativeai.configure(api_key=API_KEY)
    models = google.generativeai.list_models()
    for model in models:
        print(f"Model name: {model.name}")
        print(f"  Description: {getattr(model, 'description', '')}")
        print(f"  Supported generation methods: {getattr(model, 'supported_generation_methods', '')}")
        print()

if __name__ == "__main__":
    list_models() 