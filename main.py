
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from boto3 import client
import json
import os
from dotenv import load_dotenv
import threading
import queue

from typing import List, Dict

import services.textract_function as textract_function

load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_VALUE = os.getenv('AWS_ACCESS_KEY_VALUE')
S3_BUCKET = 'meayudai-files'
S3_REGION = 'oregon'
# Directory to save uploaded files
UPLOAD_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)

AWS_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='s3')
AWS_ANSWER_PARSER_AGENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='bedrock-agent-runtime', region_name='us-west-2')
AWS_BEDROCK_CLIENT = client(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY_VALUE, service_name='bedrock-runtime', region_name='us-west-2')

TEXTRACT_CLIENT = client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY_VALUE,
    region_name='us-west-2'  # Cambia por la región correcta
)

def get_correct_exam_system_prompt(guideline, answer):
    system_prompt = (
        "You are an assistant for grading exams. "
        "You need to evaluate how accurate the student's answer is based on a guideline and the answer provided as context. "
        "The guideline has a structure of a dictionary where the main key is the question number, followed by a dictionary with each question and an outline of what is expected as the student's answer. "
        "The answer is a dictionary with the same structure, but it contains the student's responses. "
        "You must evaluate the accuracy of the student's answer on a scale from 1 to 10. "
        "Provide the result only as a dictionary in the following format: "
        "Question: { score: assigned_score, feedback: a brief comment explaining the assigned score }. "
        "Example output: "
        "{\"1\": { \"score\": 10, \"feedback\": \"The student's answer is correct as it includes all the key points of the expected answer.\" }, "
        "\"2\": { \"score\": 5, \"feedback\": \"The student's answer is incomplete as it misses a valid argument.\" }, ... }"
        "The guideline and the student's answer to evaluate are as follows: "
        f"Guideline: {guideline}. "
        f"Answer: {answer}. "
        "Please ensure that the output is in Spanish."
    )
    return system_prompt

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    buckets = AWS_CLIENT.list_buckets()
    #AWS_CLIENT.upload_file(f'data/prueba lourdes completa.pdf', S3_BUCKET, f'test/test5.pdf')
    return {"message": f'buckets: {buckets}'}


@app.get("/list_files/")
async def list_files():
    """
    List all files in the S3 bucket.
    Returns:
    - List of files in the S3 bucket.
    """
    try:
        # List all files in the S3 bucket
        files = AWS_CLIENT.list_objects(Bucket=S3_BUCKET)
        files_list = [file['Key'] for file in files['Contents']]
        # Return the list of files
        return files_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/analyze/")
async def analyze_file_s3(file_key: str):
    try:
        # Construct the S3 object URL
        s3_object_url = f"s3://{S3_BUCKET}/{file_key}"
        # Call AWS Textract to analyze the file in S3
        response = TEXTRACT_CLIENT.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': S3_BUCKET,
                    'Name': file_key
                }
            }
        )
        # Get the JobId from the response
        job_id = response.get('JobId')

        # Wait for Textract to process the document
        result = None
        while True:
            status = TEXTRACT_CLIENT.get_document_text_detection(JobId=job_id)
            if status['JobStatus'] in ['SUCCEEDED', 'FAILED']:
                result = status
                break
        if status['JobStatus'] == 'FAILED':
            raise HTTPException(status_code=500, detail="Textract failed to analyze the document.")
        # Return the analysis result
        textract_result = textract_function.open_textract_json(result)
        return {"job_status": status['JobStatus'], "result": textract_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/parseOcr/")
async def parse_ocr_answer(ocr_answer: List[str]):
    try:
        response = AWS_ANSWER_PARSER_AGENT.invoke_agent(
            agentId='REMJZIU22D',
            agentAliasId='G5ECOLYTGP',
            sessionId='session-6',
            inputText='\n'.join(ocr_answer)
        )

        event_stream = response['completion']

        for event in event_stream:

            if 'chunk' in event:
                chunk_data = event['chunk']['bytes'].decode('utf-8')
                response = json.loads(chunk_data)
                return response

    except Exception as e:
        print(f"Error al invocar el modelo: {str(e)}")
        return {"error": str(e)}

@app.post("/correctExam/")
async def correct_exam(guideline: Dict, answer: Dict):
    # Print input parameters for verification
    print("Input Guideline:", json.dumps(guideline, indent=2))
    print("Input Answer:", json.dumps(answer, indent=2))

    try:
        # Prepare the system prompt
        system_prompt = get_correct_exam_system_prompt(guideline, answer)
        print("System Prompt:", system_prompt)

        # Print client and model details
        print("Using AWS Bedrock Client:", AWS_BEDROCK_CLIENT)
        print("Model ID: anthropic.claude-3-haiku-20240307-v1:0")

        # Make the API call
        print("Attempting to invoke Bedrock Converse API...")
        response = AWS_BEDROCK_CLIENT.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Corrige la prueba en base a la pauta y respuesta de tu system prompt"}]
                }
            ],
            system=[{"text": get_correct_exam_system_prompt(guideline, answer)}],
            inferenceConfig={
                "temperature": 0.8  # Optional: Set a max token limit
            }
        )

        # Print full raw response for inspection
        print("Raw Response:", json.dumps(response, indent=2))

        # Extract and print the content
        if 'output' in response and 'message' in response['output']:
            content = response['output']['message']['content'][0]['text']
            print("Extracted Content:", content)

            # Attempt to parse the content (if it's expected to be JSON)
            try:
                parsed_content = json.loads(content)
                print("Parsed Content:", json.dumps(parsed_content, indent=2))
                return parsed_content
            except json.JSONDecodeError:
                print("Content is not JSON, returning as string")
                return {"result": content}

        # If no content found
        print("No content found in the response")
        return {"error": "No content in response"}

    except Exception as e:
        # Comprehensive error logging
        print("Error occurred:")
        print("Error Type:", type(e).__name__)
        print("Error Message:", str(e))

        # Print full traceback for detailed debugging
        # traceback.print_exc()

        # Return error details
        # return {
        #     "error": str(e),
        #     "error_type": type(e).__name__,
        #     "traceback": traceback.format_exc()
        # }

@app.post("/pauta/")
async def upload_file(file: UploadFile = File(...)):
    AWS_CLIENT.upload_fileobj(
            Fileobj=file.file,  # Streamed file-like object
            Bucket=S3_BUCKET,
            Key=f'data/{file.filename}',
            ExtraArgs={"ContentType": file.content_type}  # Optional: preserve MIME type
        )

    # Construct a public file URL (if your S3 bucket is public)
    file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file.filename}"

    return {
        "filename": file.filename,
        "url": file_url,
        "message": "File uploaded successfully to S3!"
    }


# Worker function
def upload_worker(file_queue):
    while True:
        file = file_queue.get()
        if file is None:  # Exit signal
            break
        try:
            AWS_CLIENT.upload_fileobj(
                Fileobj=file.file,  # Streamed file-like object
                Bucket=S3_BUCKET,
                Key=f"data/{file.filename}",
                ExtraArgs={"ContentType": file.content_type}  # Preserve MIME type
            )
            print(f"Uploaded: {file.filename}")
        except Exception as e:
            print(f"Error uploading {file.filename}: {e}")
        finally:
            file_queue.task_done()

# FastAPI endpoint for file upload
@app.post("/prueba/")
async def upload_file(files: List[UploadFile] = File(...)):
    file_queue = queue.Queue()
    NUM_WORKERS = 4  # Number of worker threads
    threads = []

    # Start worker threads dynamically
    for _ in range(NUM_WORKERS):
        t = threading.Thread(target=upload_worker, args=(file_queue,), daemon=True)
        t.start()
        threads.append(t)

    # Add files to the queue (producer)
    file_urls = []
    for file in files:
        file_queue.put(file)
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/data/{file.filename}"
        file_urls.append(file_url)
    # Wait for all tasks in the queue to be processed
    file_queue.join()

    # Stop the worker threads
    for _ in range(NUM_WORKERS):
        file_queue.put(None)  # Signal workers to exit
    for t in threads:
        t.join()

    return {
        "message": "Files uploaded successfully to S3!",
        "files": file_urls
    }
