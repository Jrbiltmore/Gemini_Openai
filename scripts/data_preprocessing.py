import json
import re
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    def __init__(self, raw_data_path, processed_data_path, test_size=0.2):
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path
        self.test_size = test_size

    def load_data(self):
        with open(self.raw_data_path, 'r') as file:
            data = json.load(file)
        return data

    def clean_text(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        return text.strip().lower()

    def preprocess_data(self, data):
        for entry in data:
            entry['text'] = self.clean_text(entry['text'])
        return data

    def split_data(self, data):
        texts = [entry['text'] for entry in data]
        labels = [entry['label'] for entry in data]
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=self.test_size, random_state=42)
        return X_train, X_test, y_train, y_test

    def save_processed_data(self, X_train, X_test, y_train, y_test):
        processed_data = {
            'train': {'texts': X_train, 'labels': y_train},
            'test': {'texts': X_test, 'labels': y_test}
        }
        with open(self.processed_data_path, 'w') as file:
            json.dump(processed_data, file)
        print(f"Processed data saved to {self.processed_data_path}")

    def run(self):
        data = self.load_data()
        data = self.preprocess_data(data)
        X_train, X_test, y_train, y_test = self.split_data(data)
        self.save_processed_data(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    raw_data_path = 'data/raw_data.json'  # Replace with the path to your raw dataset
    processed_data_path = 'data/processed_data.json'  # Replace with the desired path to save the processed data

    preprocessor = DataPreprocessor(raw_data_path, processed_data_path)
    preprocessor.run()
