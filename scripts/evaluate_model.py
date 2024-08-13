import requests

class ModelEvaluator:
    def __init__(self, gemini_api_url, openai_api_url, gemini_api_key, openai_api_key):
        self.gemini_api_url = gemini_api_url
        self.openai_api_url = openai_api_url
        self.gemini_api_key = gemini_api_key
        self.openai_api_key = openai_api_key

    def evaluate_models(self, test_cases):
        results = []
        for test_case in test_cases:
            gemini_response = self.call_gemini_api(test_case)
            openai_response = self.call_openai_api(test_case)

            comparison = self.compare_responses(gemini_response, openai_response)
            results.append({
                "test_case": test_case,
                "gemini_response": gemini_response,
                "openai_response": openai_response,
                "comparison": comparison
            })

        return results

    def call_gemini_api(self, message):
        headers = {
            "Authorization": f"Bearer {self.gemini_api_key}",
            "Content-Type": "application/json"
        }
        payload = {"input": message}
        response = requests.post(self.gemini_api_url, headers=headers, json=payload)
        return response.json().get("output", "")

    def call_openai_api(self, message):
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "text-davinci-003",
            "prompt": message,
            "max_tokens": 150
        }
        response = requests.post(self.openai_api_url, headers=headers, json=payload)
        return response.json().get("choices", [{}])[0].get("text", "").strip()

    def compare_responses(self, gemini_response, openai_response):
        if gemini_response == openai_response:
            return "Identical"
        elif gemini_response in openai_response or openai_response in gemini_response:
            return "Similar"
        else:
            return "Different"

    def log_results(self, results):
        with open('evaluation_results.txt', 'w') as log_file:
            for result in results:
                log_file.write(f"Test Case: {result['test_case']}\\n")
                log_file.write(f"Gemini Response: {result['gemini_response']}\\n")
                log_file.write(f"OpenAI Response: {result['openai_response']}\\n")
                log_file.write(f"Comparison: {result['comparison']}\\n")
                log_file.write("\\n")

if __name__ == "__main__":
    gemini_api_url = "https://api.gemini.com/v1/your-endpoint"  # Replace with the actual Gemini API endpoint
    openai_api_url = "https://api.openai.com/v1/completions"  # Replace with the actual OpenAI API endpoint
    gemini_api_key = "your-gemini-api-key"  # Replace with your Gemini API key
    openai_api_key = "your-openai-api-key"  # Replace with your OpenAI API key

    test_cases = [
        "What is the capital of France?",
        "Explain the theory of relativity.",
        "How do you make a chocolate cake?",
        "What is quantum computing?",
        "Tell me a joke."
    ]

    evaluator = ModelEvaluator(gemini_api_url, openai_api_url, gemini_api_key, openai_api_key)
    results = evaluator.evaluate_models(test_cases)
    evaluator.log_results(results)
