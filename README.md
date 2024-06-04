### Deploy Mistral 7B as a model within CML
This project walks through a deployment and hosting of a Large Languge Model (LLM) within CML. The project can be cloned into CML directly,  It can be launched as an Applied Machine Learning Prototype (AMP) as well. 

### Model EULA Acceptance
Navigate to https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2 and accept the terms of the model. Then save the HF key by navigating to your profile and clicking "Settings", then "Access Tokens" and copy the key to your clipboard.

### Site settings prerequisites
1. Go to Site Administration > Settings > Ephemeral Storage Limit (in GB) and set to 20GB minimum.
2. g4dn.4xlarge is the minimum recommended GPU type on AWS. It has 8 vCPUs and accounts for any overhead on top of 4 vCPUs that the model deployment needs.

### Deploy the model manually
Deploy the model by:
- Navigate to  Model Deployments
- Click `New Model`
- Give it a Name and Description
- Disable Authentication (for convenience)
- Select File `launch_model.py`
- Set Function Name `api_wrapper`
  - This is the function implemented in the python script which wraps text inference with the mistral7b model
- Set sample json payload
   ```
    {
    "prompt": "test prompt hello"
    }
   ```
- Pick Runtime
  - PBJ Workbench -- Python 3.9 -- Nvidia GPU -- 2023.08
- Set Resource Profile
  - At least 4CPU / 16MEM
  - 1 GPU
- Click `Deploy Model`
- Wait until it is Deployed

Test the Model.


## Use Case Examples

### Email Generator
- With the model deployed and runnning, open a new session
- In a running session, select the Python 'callBooth.py' and edit the model end point URL and API key.  These values can be found in the model testing UI on CML. 
    ```
        # API endpoint URL
        endpoint = "https://YOUR MODEL ENDPOINT"
        
        #Access Key
        Akey = 'paste-here'
    ```
- Once you have updated these values, just run the script. It will access the file located in /data/CSVExample.csv

### Document Feasiblity Tester

- With the model deployed and runnning, open a new session
- In a running session, select the Python 'PDFRip.py' and edit the model end point URL and API key.  These values can be found in the model testing UI on CML. 
    ```
        # API endpoint URL
        endpoint = "https://YOUR MODEL ENDPOINT"
        
        #Access Key
        Akey = 'paste-here'
    ```
- Once you have updated these values, just run the script. It will access the file located in /data/DPO.xml
- To work with a new PDF, using the tool GROBRID to convert a PDF to XML, which can used online using this following link.  https://huggingface.co/spaces/kermitt2/grobid
- This newly converted PDF document can be used after modifing the following code section:
    ```
        #Pass XML File and Return String
        xml_string = read_xml_file('data/YOUR_NEW_DOC.xml')
    ```


Copyright (c) 2023 - 2024 - Cloudera, Inc. All rights reserved.