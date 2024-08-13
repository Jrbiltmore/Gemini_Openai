import time
import requests

class SystemMonitor:
    def __init__(self, gemini_api_url, openai_api_url, monitoring_interval=60):
        self.gemini_api_url = gemini_api_url
        self.openai_api_url = openai_api_url
        self.monitoring_interval = monitoring_interval

    def monitor_endpoints(self):
        while True:
            gemini_status = self.check_endpoint(self.gemini_api_url)
            openai_status = self.check_endpoint(self.openai_api_url)

            print(f"Gemini API Status: {gemini_status}")
            print(f"OpenAI API Status: {openai_status}")

            self.log_status(gemini_status, openai_status)
            time.sleep(self.monitoring_interval)

    def check_endpoint(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return "Healthy"
            else:
                return f"Unhealthy (Status Code: {response.status_code})"
        except requests.exceptions.RequestException as e:
            return f"Unhealthy (Exception: {str(e)})"

    def log_status(self, gemini_status, openai_status):
        with open('monitoring_log.txt', 'a') as log_file:
            log_file.write(f"Gemini API: {gemini_status}, OpenAI API: {openai_status}\\n")

if __name__ == "__main__":
    gemini_api_url = "https://api.gemini.com/v1/your-endpoint"  # Replace with the actual Gemini API endpoint
    openai_api_url = "https://api.openai.com/v1/completions"  # Replace with the actual OpenAI API endpoint

    monitor = SystemMonitor(gemini_api_url, openai_api_url)
    monitor.monitor_endpoints()
