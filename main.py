import openai
import pydantic
from EmailClass import EmailAnalysis
from dotenv import load_dotenv
import os
from Testing import EmailAnalysisTesting
import pandas as pd
from openai import OpenAI
import json
import re
import csv
def parse_openai_email_analysis(api_response: str):
    """
    Parse the OpenAI API response string and extract the email analysis JSON.
    
    Args:
        api_response (str): The full response string from OpenAI's chat completion API
        
    Returns:
        dict: The parsed email analysis JSON object
        
    Raises:
        ValueError: If no valid JSON is found in the content
        json.JSONDecodeError: If the extracted JSON is invalid
    """
    try:
        content_match = re.search(r"content='(\{.*?\})'", api_response, re.DOTALL)
        
        if not content_match:
            raise ValueError("Could not find JSON content in API response")
            
        # Extract the content (which contains our JSON)
        content = content_match.group(1)
        
        # Clean up the content
        # Replace any escaped characters
        content = content.replace('\\n', '\n')
        content = content.replace('\\"', '"')
        content = content.replace('\\\\', '\\')
        
        # Parse the JSON string
        email_analysis = json.loads(content)
        
        return email_analysis
    except (json.JSONDecodeError, AttributeError) as e:
        raise ValueError(f"Failed to parse email analysis JSON: {str(e)}")

def call_model(prompt, schema = EmailAnalysis ):
    client = OpenAI(
        # api_key= Insert your API key here
    ) 
    # I had problems getting os.getenv to work with the API key so I just hardcoded it in here.
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt}
        ],
        response_format=schema
    
    )
    return response

def batch_call_model(prompt, emails):
    responses = []
    for email in emails:
        responses.append(call_model(prompt))
    return responses

def batch_testing(predictions, ground_truths):
    """
    Test multiple predictions against their ground truths
    
    Args:
        predictions: List of prediction JSONs
        ground_truths: List of ground truth JSONs
    """
    tester = EmailAnalysisTesting(EmailAnalysis)
    
    # Calculate accuracy for each pair
    all_accuracies = []
    for pred, truth in zip(predictions, ground_truths):
        accuracy_results = tester.calculate_accuracy(pred, truth)
        all_accuracies.append(accuracy_results)
    
    # Calculate average accuracies
    overall_accuracy = sum(res['overall_accuracy'] for res in all_accuracies) / len(all_accuracies)
    
    # Calculate average field accuracies
    field_accuracies = {}
    for field in all_accuracies[0]['field_accuracies'].keys():
        field_accuracies[field] = sum(
            res['field_accuracies'][field] 
            for res in all_accuracies
        ) / len(all_accuracies)
    
    print(f"\nBatch Testing Results:")
    print(f"Overall Average Accuracy: {overall_accuracy:.2%}")
    print("\nField-wise Average Accuracies:")
    for field, accuracy in field_accuracies.items():
        print(f"{field}: {accuracy:.2%}")

def add_json_column_to_csv(existing_csv, json_data, output_csv):
    # Used to the ground truth JSON data to the existing CSV file witht he emails
    # Load the existing CSV data
    with open(existing_csv, mode='r', encoding='utf-8') as csv_file:
        reader = list(csv.DictReader(csv_file))
        
    # Check if JSON data matches the number of rows in the CSV
    if len(reader) != len(json_data):
        print("The number of JSON objects does not match the number of rows in the CSV.")
        print('reader:',len(reader))
        print('json_data:',len(json_data))
        return

    # Add a new column "ground_truth" with JSON strings
    for i, row in enumerate(reader):
        row['GroundTruth'] = json.dumps(json_data[i], indent=4, default=str)

    # Save to a new CSV file with the added column
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = reader[0].keys()  # Get headers including the new "ground_truth" column
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(reader)

def main():
    load_dotenv()
    
    # Import the prompt from the markdown file
    

    # Import the response schema
    response_schema = EmailAnalysis.schema_json()
    response_schema = json.loads(response_schema)
    json_data = []

    # Import the emails and ground truth data
    dataset = pd.read_csv('AcaiEmailsDataset.csv')
    
    emails = dataset['EmailBody']
    ground_truth = dataset['GroundTruth']
    subject = dataset['Subject']
    sender_email = dataset['Sender']
    recipient_email = dataset['Recipients']

    tester = EmailAnalysisTesting(EmailAnalysis)
    

    for email, gt, subj, sender, recipient in zip(emails, ground_truth, subject, sender_email, recipient_email):
        with open('Prompt.md', 'r') as file:
            prompt = file.read()
        formatted_prompt = prompt.format(
            subject=subj,
            sender_email=sender,
            recipient_email=recipient,
            email_body=email
        )
        
        # Get the response of the model for each email
        response = call_model(formatted_prompt)
        response_data = parse_openai_email_analysis(str(response))
        #print('response data:',response_data)
        prediction = json.dumps(response_data, indent=4, default=str)
        #print('prediction:',prediction)
        json_data.append(prediction)
        print(len(json_data))
        ground_truth = json.loads(gt)
        #print('ground truth',gt)
        #break
        # Calculate accuracy and save to a csv
        accuracy_results = tester.calculate_accuracy(response_data, ground_truth)
        
    #add_json_column_to_csv('AcaiEmailsDataset.csv', json_data, 'AcaiEmailsDataset.csv')

if __name__ == "__main__":
    main()