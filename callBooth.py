import csv
import requests
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def call_api(endpoint, data=None, headers=None):
    try:
        response = requests.post(endpoint, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()  # Parse response JSON
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return None

def send_email(mSubject, mPayLoad):
    
    message = Mail(
    from_email='user@cloudera.com',
    to_emails='user@cloudera.com',
    subject= mSubject,
    html_content= mPayLoad)
    
    SENDGRID_API_KEY = "PASTEHERE"
    
    try:
      sg = SendGridAPIClient(SENDGRID_API_KEY)
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
      
    except requests.exceptions.RequestException as e:
      print("Error making Email API Call:", e)
    
    
      
def main():
    # API endpoint URL
    endpoint = "https://modelservice.ml-cd558cf0-ec7.se-sandb.a465-9q4k.cloudera.site/model"

    # Request headers
    headers = {'Content-Type': 'application/json'}
    
    #Access Key
    Akey = 'paste-here'
    
    #Prompt
    instart = "[INST]"
    inend = "[/INST]" 
    role1 = 'from the Cloudera Team to ' 
    action = 'Write a 150 word email to '
    context = ' we would like to thank you for meeting us Gartner confereence last week. \
We throughly enjoyed discussing the new trends in '
    topics = 'GenAI and how Cloudera can enable your organization\'s success. Also request a follow up call '
    promptPart1 = instart + action + role1  
    promptPart2 = context + topics + inend
    endofPrompt = " ** "
    endofResponse = ", 'response_time_s':"
    
    # Open CSV file
    with open('data/example.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
          
            if(row[2] == "Cloudera"):
              continue
                
            # Construct request data string using row information
            request_data = '{"accessKey":"'+ Akey + '","request":{"max_new_tokens": 500, "prompt":"'+ action + row[0] + ' who works at ' + row[3] + ' organization ' + promptPart2 + endofPrompt + '"}}'
            
            # Make API call
            response_data = call_api(endpoint, data=request_data, headers=headers)
     
            if response_data:
              # Process response data
              split_response_data = str(response_data).split(endofPrompt, 1)
              split_response_data1 = str(split_response_data[1]).split(endofResponse, 1)
              print("LLM Response: ")
              
              text = split_response_data1[0]
              lines = text.split('\\n')
              print('\n'.join(lines))
              
              #send_email("Thank you for attending our dinner at Capa", split_response_data1[0])
            else:
              print("Failed to fetch data from the API.")
              

if __name__ == "__main__":
    main()