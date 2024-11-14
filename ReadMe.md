# Email Analysis Toolkit
## Acai Interview project

This is a comprehensive toolkit for analyzing email data using machine learning models. It includes the following components:

## Prompt Markdown

The prompt used to generate the email analysis is defined in a Markdown file. This allows for easy editing and version control of the prompt.

## Dataset

The email dataset is stored in a CSV file called Dataset.csv. Each row in the CSV contains the email body and the ground truth analysis in JSON format.

## EmailAnalysis Pydantic Class

The EmailAnalysis class, defined in EmailClass.py, is a Pydantic model that represents the structure of the email analysis. It defines the various fields that will be analyzed, such as primary_purpose, secondary_purposes, booking_type, etc. This class is used to ensure that the model output conforms to a specific schema.

## Email Analysis Testing

The EmailAnalysisTesting class, defined in testing.py, is responsible for evaluating the accuracy of the model's predictions. It has the following features:

1. Automatic Enum Handling: The class automatically discovers all enum fields in the EmailAnalysis model and handles them using a "soft" accuracy metric. This means that if the predicted value is off by one step in the enum, it will receive a partial score instead of a complete miss.
2. Field-level Accuracy: The class calculates the accuracy for each individual field in the EmailAnalysis model, providing detailed feedback on which areas the model is performing well or poorly.
3. Overall Accuracy: In addition to field-level accuracy, the class also calculates an overall accuracy score, representing the average accuracy across all fields.
4. CSV Logging: The accuracy results are saved to a CSV file, allowing for easy tracking and analysis of the model's performance over time.

# Usage

### 1. Prepare the Dataset:

Ensure that the Dataset.csv file is in the correct format, with email bodies and ground truth analyses in JSON format.

### 2. Define the Prompt:

Edit the Markdown file containing the prompt used to generate the email analyses.

### 3. Run the Analysis:

In your main script (e.g., main.py), load the email dataset and prompt, then call the model to generate predictions for each email.
Pass the predictions and ground truth to the EmailAnalysisTesting class to evaluate the accuracy.

### 4. Review the Results:

The accuracy results, including field-level metrics and the overall score, will be logged to a CSV file.

By using this toolkit, you can easily test and improve the performance of your email analysis model, track its progress over time, and gain valuable insights into its strengths and weaknesses.

