import xml
import requests
import time
import xml.etree.ElementTree as ET

def call_api(endpoint, data=None, headers=None):
    try:
        response = requests.post(endpoint, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()  # Parse response JSON
    except requests.exceptions.RequestException as e:
        print("\nError making API request:", e)
        return None

def read_xml_file(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
      
        # Function to recursively extract text content from XML elements
        def extract_text(element):
            text = element.text or ''
            for child in element:
                text += extract_text(child)
            return text

        # Extract text content from the root element
        content = extract_text(root)
        return content.strip().encode('utf-8')
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error parsing XML file '{file_path}':", e)
        return None

def break_into_sections(input_string, section_length=500):
    sections = []
    for i in range(0, len(input_string), section_length):
        section = input_string[i:i+section_length]
        sections.append(section)
    return sections
      
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
    role1 = 'You are a scientific researcher. ' 
    action = 'Read the following statement '
    context = 'and determine if it statements are not feasible : '
    
    
    promptPart1 = instart + role1 + action + context
    promptPart2 = inend
    endofPrompt = " ** "
    endofResponse = ", 'response_time_s':"
    
    #Pass XML File and Return String
    xml_string = read_xml_file('data/RAFT.xml')
    
    
    if xml_string:
      # print(xml_string)
      pdfSections = break_into_sections(xml_string)
      #print(pdfSections)
      
      for i in range(len(pdfSections)):
            #print(str(pdfSections[i].decode('ascii','replace')))
            # Construct request data string using row information
            #request_data = '{"accessKey":"'+ Akey + '","request":{"max_new_tokens": 3000, "prompt":"'+ promptPart1 + " cold fusion " +  promptPart2 + endofPrompt + '"}}'
            request_data = '{"accessKey":"'+ Akey + '","request":{"max_new_tokens": 3000, "temperature":1, "prompt":"'+ promptPart1 + str(pdfSections[i].decode('ascii','replace')) +  promptPart2 + endofPrompt + '"}}'

            #print("\n^^^^^ " + request_data)
            # Make API call
            response_data = call_api(endpoint, data=request_data, headers=headers)
            time.sleep(30)

            if response_data:
                # Process response data
                split_response_data = str(response_data).split(endofPrompt, 1)
                split_response_data1 = str(split_response_data[1]).split(endofResponse, 1)
                print("\nAPI Response: " + split_response_data1[0].replace("\\n\\n", "\n\n").replace("\\n", "\n").replace("**", ""))
            else:
                print("Failed to fetch data from the API.")

if __name__ == "__main__":
    main()
