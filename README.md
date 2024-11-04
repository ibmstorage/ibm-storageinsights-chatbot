---

<div align="center">
  <img src="./querius.png" alt="Querius Logo" width="300" height="300">
</div>
 
<h2 align="center">Querius</h2>

---

## Introduction

### What is Querius?

Querius is an open-source chatbot created by the Storage Insights team to enable natural language interactions with Storage Insights REST APIs. By leveraging large language models (LLMs) and advanced prompt engineering, it intelligently detects user intent, extracts relevant entities, and seamlessly makes API calls.

**Powered by [IBM Watsonx](https://www.ibm.com/watsonx) and utilizing both Granite and Llama (Built with Llama) LLMs,** Querius provides a conversational, intuitive approach for managing and accessing storage data and insights.


### Key Features

- **Natural Language Understanding**: Utilizes LLMs to process user queries and convert them into actionable API calls.
- **Entity Recognition**: Extracts storage-specific entities from user input to ensure accurate API interactions.
- **REST API Integration**: Directly interacts with Storage Insights APIs to retrieve storage system alerts, metrics, notifications, and more.

### Supported APIs

Querius currently supports the following APIs:

- Storage system alerts
- Storage system metrics
- Storage system notifications
- Storage system list
- Tenant alerts
- Tenant notifications
- Storage system volumes
- Storage system details

---

## Installation

### Prerequisites

Before installing Querius, ensure you have the following prerequisites:

1. **Sign up for IBM watsonx as a Service**: [Sign up for IBM watsonx as a Service](https://www.ibm.com/docs/en/watsonx/saas?topic=started-signing-up-watsonx).
    > Select `DALLAS` region as the LLM availability differs from region to region.
    
    > You get 50,000 free tokens per month with your Lite account, consider upgrading to a `pay-as-you-go` account where you get $200 free credits which are valid for 30 days. For more information, visit [Upgrading your account](https://cloud.ibm.com/docs/account?topic=account-upgrading-account)

2. **Create a watsonx API key**: Setup your watsonx machine learning instance by following Steps 1 to 9 in this document [Create a watsonx API key](https://www.ibm.com/docs/en/mas-cd/maximo-manage/continuous-delivery?topic=setup-create-watsonx-api-key) .
    > Keep note of the generated `Watsonx Project ID`.
    
    > Keep note of the generated `Watsonx API key`.

3. **Storage Insights API Key**: Refer section [Generating a REST API key](https://www.ibm.com/docs/en/storage-insights?topic=configuring-user-access-management). 
    > This Storage Insights api key will be used during login.

4. **Podman**: [Install Podman](https://podman.io/docs/installation).
    - You can then verify the installation information using:
      ```bash
      podman info
      ```
    - If podman is setup correctly, you will be able to see detailed information about your host. 

5. **Install Git**: [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
6. **Install OpenSSL** : [Install OpenSSL](https://github.com/openssl/openssl/blob/master/INSTALL.md#quick-installation-guide)
    > OpenSSL comes pre-installed on many Unix-based operating systems, such as Linux and macOS. Run below command to check if OpenSSL is already installed on your system
    ```bash
    openssl version
    ```
    > If OpenSSL is installed, this command will display the version of OpenSSL installed, like:
    `OpenSSL 3.1.1 30 May 2023 (Library: OpenSSL 3.1.1 30 May 2023)`

### Installation

1. Clone the GitHub repo:  
   [https://github.com/ibmstorage/ibm-storageinsights-chatbot.git](https://github.com/ibmstorage/ibm-storageinsights-chatbot.git)
   
     ```bash
     git clone https://github.com/ibmstorage/ibm-storageinsights-chatbot.git
     ```
2. Go to directory `ibm-storageinsights-chatbot/`.
    ```bash
    cd ibm-storageinsights-chatbot/
    ```
3. Generate a secret key using the script [generate_key.sh](./generate_key.sh). This secret is required to encrypt/decrypt the Storage Insights API key during all communications.
   - Make the script executable using the command:
        ```bash
        chmod +x generate_key.sh
        ```
   - Run the script:
        ```bash
        ./generate_key.sh
        ```
   - The key will be printed on the terminal. Copy the key as it will be used in next step.
4. To start an HTTPS server, generate self-signed certificates using the provided script [generate_certificates.sh](./generate_certificates.sh).
   - Make the script executable:
        ```bash
        chmod +x generate_certificates.sh
        ```

   - Run the script:
        ```bash
        ./generate_certificates.sh
        ```

   - The script will prompt you to enter some details. Fill in the required information to proceed.

   - The generated certificates will be stored in:
       - `frontend/certificates/`
       - `backend/certificates/`
   > **Note:** Self-signed certificates work only with Google Chrome. For other browsers, manually copy the CA-certified certificates to the `frontend/certificates/` and `backend/certificates/` directories as needed.
5. Set environment variables:

    #### 1. Setting variables for Frontend
    1. Go to `frontend/`.
        ```bash
        cd frontend/
        ```
    2. Open `dockerfile.frontend` in a text editor and add values for `REACT_APP_BACKEND_BASE_URL` and `REACT_APP_SECRET_KEY`:
        - `REACT_APP_BACKEND_BASE_URL`: Backend server URL where the backend APIs are hosted. If your are running the chatbot on a Host with IP `9.200.34.201`, the URL will be `https://9.200.34.201:9508/chatbot`. Please change the Host IP according to your infrastructure.
        - `REACT_APP_SECRET_KEY`: Refer to Step 3 for copying the newly generated secret key.

    3. After setting up the necessary variables, go pack to the parent directory using below command:
        ```bash
        cd ..
        ```

    #### 2. Setting variables for Backend
    1. Go to `backend/`.
        ```bash
        cd backend/
        ```
    2. Open `dockerfile.backend` in a text editor and add values for the following variables:
        - `WATSONX_APIKEY`: Refer to [Prerequisites, point 4](#prerequisites) for copying the API key.
        - `PROJECT_ID`: Refer to [Prerequisites, point 3](#prerequisites) for copying the Project ID.
        - `WATSONX_HOSTED_SERVICE`: This is watsonx endpoint URl and depends on the region you selected while setting up the account. Refer [Endpoint URLs](https://cloud.ibm.com/apidocs/machine-learning) section for possible values.
        - `ORIGIN`: URL where the frontend is hosted. If your are running the chatbot on a Host with IP `9.200.34.201`, the URL will be `https://9.200.34.201:9502`. Please change the Host IP according to your infrastructure.
        - `SECRET_KEY`: Refer to step 3 for copying the newly generated secret key.

6. Go back to parent directory `ibm-storageinsights-chatbot/`.
    ```bash
    cd ..
    ```
7. You will find an install script `install_si_chatbot.sh`. Some values are pre-configured but can be changed as per your infrastructure. These values are:
     - `FRONTEND_IMAGE_TAG`
     - `BACKEND_IMAGE_TAG`
     - `VOLUME_NAME`
     - `BACKEND_PORT`
     - `FRONTEND_PORT`
8. Make the script executable using the command:

      ```bash
      chmod +x install_si_chatbot.sh
      ```
9. Run the script:

      ```bash
      ./install_si_chatbot.sh
      ```
10. Access the frontend UI from the link:
      ```bash
      https://<host>:9502/querius/
      ```
---

## Common Installation Errors

1. If you encounter below error
    
    `Error: creating container storage: the container name "frontend" is already in use`
    
    Run below commands and execute `install_si_chatbot.sh` script again
    ```bash
    podman stop backend
    podman stop frontend
    podman rm backend
    podman rm frontend
    ```
  
## Helpful videos

1. Video guide for [IBM Watsonx as a service](https://www.youtube.com/watch?v=EjiVdAPd894)
2. Video guide for [Chatbot Installation](https://www.youtube.com/watch?v=-YWqxQg-N7Y)
3. User guide for [Chatbot Features Overview](https://www.youtube.com/watch?v=mgwPel1ybtM) 

## License

[Apache License (Version 2.0)](./LICENSE)

## Authors

See [AUTHORS.md](./AUTHORS.md)
