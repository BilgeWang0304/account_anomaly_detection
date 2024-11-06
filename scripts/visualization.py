import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self, data_path='../database/anomalies.csv'):
        self.data_path = data_path
        self.data = self.load_data()

    def load_data(self):
        data = pd.read_csv(self.data_path)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        print(f"Data loaded successfully from {self.data_path}")
        return data

    def bar_chart(self):
        sns.countplot(data=self.data, x='is_anomaly', palette='Set2')
        plt.title('Count of Normal vs. Fraudulent Transactions')
        plt.xlabel('Transaction Type')
        plt.ylabel('Count')
        plt.xticks([0, 1], ['Normal', 'Fraudulent'])
        plt.show()
        plt.savefig('../database/normal_vs_fraudulent_transactions.png') 

    def compare_fraud_anomaly(self):
        comparison_df = self.data[['is_fraud', 'is_anomaly']].copy()
        comparison_df['Match'] = (comparison_df['is_fraud'] == comparison_df['is_anomaly']).astype(int)

        confusion_matrix = pd.crosstab(comparison_df['is_fraud'], comparison_df['is_anomaly'], rownames=['Actual'], colnames=['Predicted'])
        sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues")
        plt.title('Comparison of Actual Fraud and Anomaly Detection')
        plt.xlabel('Predicted (is_anomaly)')
        plt.ylabel('Actual (is_fraud)')
        plt.show()
        plt.savefig('../database/comparison_fraud_anomaly.png')

    def time_series_plot(self):
        grouped_data = self.data.groupby(['timestamp', 'is_anomaly'])['amount'].mean().reset_index()
        pivoted_data = grouped_data.pivot(index='timestamp', columns='is_anomaly', values='amount')

        plt.figure(figsize=(14, 7))
        plt.plot(pivoted_data.index, pivoted_data[0], label='Normal', color='blue')
        plt.plot(pivoted_data.index, pivoted_data[1], label='Fraudulent', color='red')

        plt.title('Time Series of Transactions with Anomalies Highlighted')
        plt.xlabel('Timestamp')
        plt.ylabel('Transaction Amount')
        plt.legend(title='Transaction Type', labels=['Normal', 'Fraudulent'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        plt.savefig('../database/transaction_time_series.png')


    def run_all_visualizations(self):
        self.bar_chart()
        self.compare_fraud_anomaly()
        self.time_series_plot()

if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.run_all_visualizations()
