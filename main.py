from scripts.generate_data import DataGenerator
from scripts.model_training import ModelTrainer
from scripts.anomaly_detection import AnomalyDetector

def main():
    # Step 1: Generate data
    print("Starting data generation...")
    generator = DataGenerator(num_accounts=1000, num_transactions=5000, fraud_percentage=0.05)
    generator.generate_data()

    # Step 2: Train the model
    print("Training anomaly detection model...")
    trainer = ModelTrainer(data_path='../database/transactions.csv', model_output_path='../models/anomaly_model.pkl')
    trainer.train_model()

    # Step 3: Run anomaly detection
    print("Running anomaly detection...")
    detector = AnomalyDetector(model_path='../models/anomaly_model.pkl')
    detector.detect_anomalies()

    print("Process completed!")

if __name__ == "__main__":
    main()
