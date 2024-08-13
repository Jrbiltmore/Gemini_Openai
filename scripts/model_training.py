model_training_script = """
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

class ModelTrainer:
    def __init__(self, dataset_path, model_save_path):
        self.dataset_path = dataset_path
        self.model_save_path = model_save_path

    def load_data(self):
        with open(self.dataset_path, 'r') as file:
            data = json.load(file)
        texts = [entry['text'] for entry in data]
        labels = [entry['label'] for entry in data]
        return texts, labels

    def train_model(self, texts, labels):
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

        pipeline = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)

        print(f"Accuracy: {accuracy}")
        print(f"Classification Report:\\n{report}")

        return pipeline

    def save_model(self, model):
        joblib.dump(model, self.model_save_path)
        print(f"Model saved to {self.model_save_path}")

    def run(self):
        texts, labels = self.load_data()
        model = self.train_model(texts, labels)
        self.save_model(model)

if __name__ == "__main__":
    dataset_path = 'data/training_data.json'  # Replace with the actual path to your dataset
    model_save_path = 'models/trained_model.pkl'  # Replace with the desired path to save the trained model

    trainer = ModelTrainer(dataset_path, model_save_path)
    trainer.run()
