import pandas as pd
import os
from sklearn.ensemble import IsolationForest
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, classification_report, confusion_matrix
import pickle

class ModelTrainer:
    def __init__(self, data_path='../database/transaction_log.csv', model_path='../models/anomaly_model.pkl'):
        self.data_path = data_path
        self.model_path = model_path

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at {self.data_path}")

        data = pd.read_csv(self.data_path)
        print(f"Data loaded successfully from {self.data_path}")
        return data

    def preprocess_data(self, data):
        data['balance_ratio'] = data['amount'] / (data['sender_balance'] + 1)  
        transaction_counts = data['sender'].value_counts()
        data['transaction_count'] = data['sender'].map(transaction_counts)
        
        features = data[['amount', 'balance_ratio', 'transaction_count']]  
        labels = data['is_fraud']  
        return features, labels

    def train_model(self, features):
        model = IsolationForest(n_estimators=100, contamination=0.034, random_state=42)
        model.fit(features)
        print("Model training completed.")
        return model

    def evaluate_model(self, model, features, labels):
        predictions = model.predict(features)
        predictions = [1 if x == -1 else 0 for x in predictions]  

        # Calculate evaluation metrics
        f1 = f1_score(labels, predictions)
        precision = precision_score(labels, predictions)
        recall = recall_score(labels, predictions)
        roc_auc = roc_auc_score(labels, predictions)

        # Print evaluation metrics
        print("Evaluation Metrics:")
        print(f"F1 Score: {f1:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"ROC-AUC: {roc_auc:.2f}")
        print("\nClassification Report:")
        print(classification_report(labels, predictions))
        print("Confusion Matrix:")
        print(confusion_matrix(labels, predictions))

    def save_model(self, model):
        with open(self.model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved to {self.model_path}")

    def run(self):
        data = self.load_data()
        features, labels = self.preprocess_data(data)
        model = self.train_model(features)
        self.evaluate_model(model, features, labels)
        self.save_model(model)

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.run()
