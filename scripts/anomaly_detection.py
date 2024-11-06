import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self, model_path):
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)

        self.scaler = StandardScaler()

    def load_data(self, data_path):
        data = pd.read_csv(data_path)
        data['balance_ratio'] = data['amount'] / (data['sender_balance'] + 1)  
        if 'transaction_count' not in data.columns:
            transaction_counts = data['sender'].value_counts()
            data['transaction_count'] = data['sender'].map(transaction_counts)
        features = data[['amount', 'balance_ratio', 'transaction_count']]
        features_scaled = self.scaler.fit_transform(features)
        features_scaled = pd.DataFrame(features_scaled, columns=['amount', 'balance_ratio', 'transaction_count'])
        return data, features_scaled

    def detect_anomalies(self, data_path='../database/transaction_log.csv', output_path='../database/anomalies.csv'):
        data, features_scaled = self.load_data(data_path)
        data['is_anomaly'] = self.model.predict(features_scaled)
        data['is_anomaly'] = data['is_anomaly'].apply(lambda x: 1 if x == -1 else 0)
        data['is_anomaly'] = data.apply(
            lambda row: 1 if (row['balance_ratio'] > 0.8 or row['transaction_count'] > 2) else 0,
            axis=1
        )
        data.to_csv(output_path, index=False)
        print(f"Anomaly detection completed. Results saved to {output_path}")

if __name__ == "__main__":

    detector = AnomalyDetector(model_path='../models/anomaly_model.pkl')
    detector.detect_anomalies()
