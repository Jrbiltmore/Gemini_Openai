import joblib
from flask import Flask, request, jsonify

class ModelDeployer:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
        self.app = Flask(__name__)

    def predict(self, text):
        prediction = self.model.predict([text])[0]
        return prediction

    def create_app(self):
        @self.app.route('/predict', methods=['POST'])
        def predict_route():
            data = request.get_json()
            text = data.get('text', '')
            prediction = self.predict(text)
            return jsonify({'prediction': prediction})

        return self.app

if __name__ == "__main__":
    model_path = 'models/trained_model.pkl'  # Replace with the path to your trained model
    deployer = ModelDeployer(model_path)
    app = deployer.create_app()

    app.run(host='0.0.0.0', port=5000)
