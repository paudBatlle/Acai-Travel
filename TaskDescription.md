# Acai Travel Interview Challenge
### Pau de Batlle Juan 13/11/2024

This is an interview project for Acai Travel.

## Briefing

You task is to create an LLM driven solution that solves a real problem in the travel industry.

As with any ML/AI task, the accuracy and reliability of the solution is of highest importance and as such, your solution should focus on - 

- Prompting
- Evaluating the prompt
- Pipelines to test major version changes of the prompt.

## Context

Our clients - Travel Agencies are the backbone of Travel Operations, most of these Travel Agencies use **email** as the primary means of communication to interact with the traveler.

Your goal is to **analyze with prompts every incoming email** that a Travel Agency receives to perform the following tasks - 

- Purpose Detection / Classification - The purpose of the email, for eg. “flight change”, “new booking”, “invoice request”, etc. This is just a small list, put yourself in the context of a travel agency and think of different possibilities.
- Sentiment analysis - The sentiment that the traveler expresses with that email, let’s say “negative”, “neutral” & “positive”
- Think of any other feature/data that you would like to extract using LLMs. Feel free to use your imagination in solving the problem for the industry.

## Task

### 1. Prompting

Define a prompt that takes an email as input and outputs a valid JSON. Think of the output of the prompt as something we could store on a database or serve over an API (not a chatbot response, for example).

The output of the prompt must **detect the purpose of the email** and the **sentiment** as explained earlier.

Based on your understandings of LLMs, JSON and the given context, it is expected of you to determine the fields inside the JSON. Think of yourself as a product-driven engineer using AI to solve an issue or improve a process.

You can use the patterns and best-practices you think are needed for the scope of the task. Accuracy is the most important metric here. We don’t care about latency, cost or token optimization. RAG is out-of-scope for this challenge.

The prompt should work a a `system` message and delivered as a templated file, avoid crafting prompts dynamically. Ideally is a Markdown file with Python template strings for the inputs (e.g `{name}`)

Summary of requirements:

1. **Inputs:** email subject, email recipients, email sender and email body
    1. Email attachments are out-of-scope.
2. **Output**: a valid JSON.

### 2. System Diagram

Prompt Engineers also develop pipelines to develop, test and evaluate prompt accuracy. We want you to develop a system diagram of how would you test the prompt for every change. Prompts are extremely sensitive to changes and we need to ensure we test them intensively before releasing them to production.

Use any tool you are comfortable with - diagramming software like Miro, Lucidchart, MermaidJS, pen + paper, whiteboard.

The goals of this exercise is for you to be able to explain systematically how would you build a pipeline to evaluate your prompt changes before that prompt change is propagated to Production Codebase.

### 3. Dataset & Testing

We also expect you to a create a dataset to validate accuracy and be able to iterate with the prompt as we add more features. You determine how many datapoints are enough to ensure reliability.

For this submission, you can also use/create synthetic data sets as long as they make sense contextually.

To validate the prompt using the dataset, you could write your own script or use any LLMOps tool (you could try [Latitude](https://latitude.so/), a Barcelona-based startup with a free tier). Determine meaningful metrics to be tested and tracked based on the features you defined.

## Deliverable

1. A github repository that should contain - 
    1. Prompt in a Markdown file with Python template string.
    2. A system diagram of the testing workflow. 
    3. A dataset to validate the prompt in CSV.
    4. A script to validate the prompt **or** screenshots of workflow in the LLMOps tool.
    5. Any additional files/documentation you’d like/need to submit

*We can provide OpenAI or Claude API keys if needed.*

## Evaluation Criteria

We are going to evaluate based on:

1. Overall submission adherence to the context & background.
2. Features defined in the prompt.
3. Best-practices applied to the prompt.
4. Data generated for testing.
5. Workflow definition for testing
6. Overall use of AI to accomplish the task.
    1. We are firm believers of enhancing us with AI, don’t be shy to use it!
