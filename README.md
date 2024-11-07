# Comparative Analysis of Rule-Based Fraud Detection and Anomaly Detection Model in Financial Transactions

## Introduction

This analysis assesses the effectiveness of an anomaly detection system applied to bank account transactions by comparing is_fraud (ground-truth labels based on transaction amount and count) with is_anomaly (model-flagged labels based on transaction count and balance ratio). By examining the alignment and temporal patterns of these labels, we aim to identify discrepancies and potential improvements in feature selection and threshold tuning, enhancing the model’s accuracy in identifying fraudulent transactions within the financial dataset.

## Brief Result

Based on the provided images and labeling criteria within the bank account system, the following is an academic analysis of the anomaly detection model's performance and the alignment between is_fraud and is_anomaly classifications.

### Image 1: Confusion Matrix Analysis of Fraud vs. Anomaly Detection

![1](https://github.com/user-attachments/assets/f330d103-244f-43fe-83a2-b76a892f6ebc)


#### Analysis of True and False Classifications:

The confusion matrix reveals a significant number of true negatives (7894), indicating that the model effectively avoids labeling non-fraudulent transactions as anomalies in most cases.

However, the presence of 430 false positives indicates that a subset of non-fraudulent transactions were erroneously classified as anomalous. This may suggest that the criteria defining is_anomaly (transaction count and balance ratio) do not fully align with those for is_fraud (transaction amount and transaction count), resulting in discrepancies.

True positives (156) demonstrate the model’s capability to detect genuinely fraudulent transactions, though 130 false negatives highlight that some fraudulent transactions were not flagged as anomalies. This might indicate that some fraud patterns were not sufficiently captured by the features used for anomaly detection.

#### Insights:

The misalignment between is_fraud and is_anomaly criteria may account for the observed false positive and false negative rates. Since is_anomaly uses balance ratio as a feature rather than transaction amount, the model may capture anomalies that fall outside the is_fraud definition, thereby causing mismatches in classification.

The confusion matrix suggests a need for fine-tuning feature selection or thresholds within the anomaly detection model to achieve better alignment with the fraud criteria.

### Image 2: Time Series Analysis of Transactions with Anomalies Highlighted

![2](https://github.com/user-attachments/assets/5be49273-38e8-42cf-bff9-c3c8f0bb8334)


#### Analysis of Temporal Patterns:

The time series graph illustrates that anomalous transactions (marked in red) generally exhibit significantly higher transaction amounts compared to normal transactions, which remain relatively stable in the lower range.

This suggests that the model is sensitive to variations in transaction values, which aligns with the balance ratio criterion of is_anomaly. However, the higher sensitivity might also explain the higher number of false positives, as any high-balance transaction, even if not fraudulent, may be flagged as an anomaly.

#### Insights:

The time series plot effectively visualizes the model’s capability to detect transactions deviating from the norm. However, it also implies that the balance ratio criterion could be overly sensitive, flagging legitimate high-value transactions as anomalies.

These findings point to potential improvements in anomaly detection by refining the balance ratio threshold or incorporating additional temporal features that consider transaction frequency or consistency over time.

## Summary and Recommendations

### Model Alignment:

The partial alignment between is_fraud and is_anomaly reflects the differing feature sets used for labeling each category. While is_fraud depends on transaction amount and transaction count, is_anomaly incorporates balance ratio and transaction count. The inconsistency in criteria is likely contributing to the false positives observed in the confusion matrix.

### Suggested Enhancements:

To reduce discrepancies, consider harmonizing the feature selection process by incorporating transaction amount into the anomaly detection model or refining the balance ratio threshold to be less sensitive to high-value but legitimate transactions.

Implementing temporal aggregation features, such as average transaction amount or frequency over defined time intervals, may provide additional insights and reduce false positive rates.

In summary, enhancing feature engineering and refining thresholds could significantly improve the congruence between fraud detection and anomaly detection, thus reducing classification errors and strengthening the robustness of the anomaly detection model.
