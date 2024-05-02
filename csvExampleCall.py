import csv
import requests
import time

def call_api(endpoint, data=None, headers=None):
    try:
        response = requests.post(endpoint, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()  # Parse response JSON
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return None

def main():
    # API endpoint URL
    endpoint = "https://modelservice.ml-cd558cf0-ec7.se-sandb.a465-9q4k.cloudera.site/model"

    # Request headers
    headers = {'Content-Type': 'application/json'}
    
    #Access Key
    Akey = 'mzauf1jp0ikojdizidywdfc82hhb9cvv'
    
    #Prompt 
    instart = "[INST]"
    inend = "[/INST]" 
    role1 = 'You are from Cloudera ' 
    action = 'write an email to '
    context = 'to thank them for speaking to us about '
    topics = 'GenAI and enabling your organizations success.'
   
    
    promptPart1 = instart + role1 + action 
    promptPart2 = context + topics + inend
    endofPrompt = " ** "
    endofResponse = ", 'response_time_s':"
    
    # Open CSV file
    with open('data/example.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            # Construct request data string using row information
            request_data = '{"accessKey":"'+ Akey + '","request":{"prompt":"'+ promptPart1 + row[0] + ' from ' + row[2] + promptPart2 + endofPrompt + '"}}'

            # Make API call
            response_data = call_api(endpoint, data=request_data, headers=headers)
            time.sleep(1)
            
            if response_data:
                # Process response data
                split_response_data = str(response_data).split(endofPrompt, 1)
                
                split_response_data1 = str(split_response_data[1]).split(endofResponse, 1)
                
                print("API Response: ", split_response_data1[0])
            else:
                print("Failed to fetch data from the API.")

if __name__ == "__main__":
    main()
