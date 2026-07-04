# File Generator — AI-Generated Documentation

**Generated:** 2026-06-22 15:47:39
**Source:** `C:\Users\du974f\Downloads\file-generator\file-generator`
**Files Analyzed:** 25
**AI Provider:** Google Gemini (FREE)

---

This is a BACKEND project.

## 1. Project Setup

### How to Install Dependencies and Start the Server

1.  **Install Dependencies:**
    *   The project uses `pipenv` for dependency management.
    *   Navigate to the project's root directory in your terminal.
    *   Run `pipenv install` to install all project dependencies.

2.  **Start the Server:**
    *   The main application entry point is `app.py`.
    *   To start the Flask development server, run:
        ```bash
        python app.py
        ```
    *   The server can be configured to run on a specific port using the `-p` or `--port` argument:
        ```bash
        python app.py -p 8000
        ```
    *   The server is configured to run on `0.0.0.0` to be accessible externally.

### Environment Variables Needed

*   `TEST_SERVICE_HOST`: The hostname for the Test Service. Defaults to `http://localhost`.
*   `TEST_SERVICE_PORT`: The port for the Test Service. Defaults to `8080`.
*   `USER_SERVICE_HOST`: The hostname for the User Service. Defaults to `http://localhost`.
*   `USER_SERVICE_PORT`: The port for the User Service. Defaults to `8085`.
*   `CELERY_BROKER_URL`: The URL for the Celery message broker (e.g., Redis).
*   `REQUESTS_CA_BUNDLE`: Path to the CA bundle for `requests` to verify SSL certificates. Used in `api/model/test_service.py` and `api/model/user_service.py`.
*   `S3_HOST`: The hostname for the S3 compatible storage. Defaults to `https://object1.cs.boeing.com:9021`.
*   `ROCS3_ACCESS_KEY_ID`: The access key ID for S3. Defaults to `pcfpre-10f90d8e-c449-4531-813d-3e637b4ed75c`.
*   `ROCS3_SECRET_KEY`: The secret access key for S3. Defaults to `ZcFX013wpi5CdJ8Q2aKCkG2vTHWEvQnkv053Flhe`.
*   `BUCKET_NAME`: The name of the S3 bucket. Defaults to `pcfpre-4fbe1846-9964-49a9-9f0a-7bb9625c5b7d`.

### Configuration Files

*   `.gitlab-ci.yml`: Defines CI/CD pipeline stages, including testing, scanning, packaging, and deployment. It also specifies environment variables and certificate handling for build environments.
*   `Dockerfile`: Defines the Docker image for the application, including base image, dependency installation, certificate setup, and command to start the Celery worker.
*   `deploy/file-generator-service-dev.yaml`: OpenShift template for deploying the development version of the service.
*   `deploy/file-generator-service.yaml`: OpenShift template for deploying the production version of the service.

## 2. Folder Structure

*   `app.py`: The main application file, responsible for creating the Flask app, configuring it, and registering blueprints.
*   `api/`: Contains the core application logic, including models, routes, and schemas.
    *   `model/`: Contains classes that interact with external services.
        *   `test_service.py`: Client for interacting with the Test Service.
        *   `user_service.py`: Client for interacting with the User Service.
        *   `welcome.py`: A simple model for welcome messages.
    *   `route/`: Contains Flask blueprints defining API endpoints.
        *   `home.py`: Defines the root API endpoint.
        *   `export.py`: Defines endpoints for file export and S3 operations.
        *   `upload.py`: Defines the endpoint for uploading CSV files.
        *   `example_route.py`: An example route blueprint.
    *   `schema/`: Contains Marshmallow schemas for request/response serialization and validation.
        *   `welcome.py`: Schema for the `WelcomeModel`.
*   `file_task.py`: Contains Celery tasks for asynchronous operations like file generation, upload, and S3 interactions.
*   `s3_bucket.py`: Contains functions for interacting with an S3-compatible object storage service.
*   `uploader.py`: A script for uploading files via the API.
*   `test/`: Contains unit and integration tests.
    *   `conftest.py`: Pytest fixtures for setting up the test environment.
    *   `route/`: Contains tests for API routes and Celery tasks.
        *   `test_celerytasks.py`: Tests for Celery tasks.
        *   `test_export.py`: Tests for export-related routes.
        *   `test_home.py`: Tests for the home route.
*   `utils/`: Contains utility functions.
    *   `logging.py`: Basic logging configuration.
*   `.gitlab-ci.yml`: CI/CD pipeline configuration.
*   `Dockerfile`: Dockerfile for building the application image.
*   `deploy/`: Contains deployment configuration files for OpenShift.

## 3. API Endpoints (Routes)

### `api/route/home.py`

#### `GET` `/` — `home.py`
-   **Purpose:** Provides a welcome message from the file generator service.
-   **Request:** None
-   **Response:**
    ```json
    {
      "message": "Hello from file generator service"
    }
    ```
-   **Logic Flow:**
    1.  Create an instance of `WelcomeModel` with a predefined message.
    2.  Serialize the `WelcomeModel` instance using `WelcomeSchema`.
    3.  Return the serialized JSON response with a 200 OK status.
-   **Authentication:** None
-   **Errors:**
    *   `400 Bad Request`
    *   `500 Internal Server Error`

### `api/route/example_route.py`

#### `GET` `/` — `example_route.py`
-   **Purpose:** Provides a generic welcome message.
-   **Request:** None
-   **Response:**
    ```json
    {
      "message": "Hello from the example service"
    }
    ```
-   **Logic Flow:**
    1.  Create an instance of `WelcomeModel`.
    2.  Serialize the `WelcomeModel` instance using `WelcomeSchema`.
    3.  Return the serialized JSON response with a 200 OK status.
-   **Authentication:** None
-   **Errors:**
    *   `HTTPStatus.OK.value` (200) is the only documented response.

### `api/route/export.py`

#### `GET` `/export` — `export.py`
-   **Purpose:** Initiates the creation of a CSV file for download based on provided test point IDs and uploads it to S3.
-   **Request:** Query Parameters
    *   `testPointIds` (array of strings, optional): IDs of test points to include in the file.
    *   `bemsid` (number, required): User's BEMS ID for S3 upload.
    *   `filename` (string, required): The desired name for the exported file.
-   **Response:**
    *   `200 OK`: A string indicating the Celery task ID for file generation.
-   **Logic Flow:**
    1.  Retrieve `testPointIds`, `bemsid`, and `filename` from query parameters.
    2.  Call `file_task.create_csv.delay()` to start an asynchronous Celery task for CSV generation and upload.
    3.  Return the Celery task ID.
-   **Authentication:** None explicitly mentioned, but `bemsid` implies user context.
-   **Errors:**
    *   `404 Not Found`: If `FileNotFoundError` occurs during task creation.
    *   `500 Internal Server Error`: General server error.

#### `GET` `/getuserbucketinfo` — `export.py`
-   **Purpose:** Retrieves information about files stored in the S3 bucket for a given BEMS ID.
-   **Request:** Query Parameters
    *   `bemsid` (number, required): The BEMS ID to query for.
-   **Response:**
    *   `200 OK`: A JSON array of objects, each containing `filename`, `date`, and `expiration` for files associated with the `bemsid`.
-   **Logic Flow:**
    1.  Retrieve `bemsid` from query parameters.
    2.  Call `s3_bucket.get_folder_info()` to fetch file details from S3.
    3.  Return the JSON response.
-   **Authentication:** None explicitly mentioned.
-   **Errors:**
    *   `400 Bad Request`: If the user is not found or other issues occur.
    *   `500 Internal Server Error`: General server error.

#### `DELETE` `/delete-file` — `export.py`
-   **Purpose:** Deletes a file from the S3 bucket.
-   **Request:** Query Parameters
    *   `bemsid` (number, required): The BEMS ID associated with the file.
    *   `filename` (string, required): The name of the file to delete.
-   **Response:**
    *   `200 OK`: A JSON object with a success message (`{"message":"File deleted"}`).
-   **Logic Flow:**
    1.  Retrieve `bemsid` and `filename` from query parameters.
    2.  Construct the full S3 key by prepending `bemsid/` to the `filename`.
    3.  Call `file_task.delete_file_from_s3()` to initiate the deletion process.
    4.  Return the result from `delete_file_from_s3`.
-   **Authentication:** None explicitly mentioned.
-   **Errors:**
    *   `400 Bad Request`: If an unexpected error occurs.
    *   `404 Not Found`: If the file is not found in S3.
    *   `500 Internal Server Error`: General server error.

#### `GET` `/download` — `export.py`
-   **Purpose:** Downloads a file from the S3 bucket.
-   **Request:** Query Parameters
    *   `bemsid` (number, required): The BEMS ID associated with the file.
    *   `filename` (string, required): The name of the file to download.
-   **Response:**
    *   `200 OK`: The requested file as a download.
-   **Logic Flow:**
    1.  Retrieve `bemsid` and `filename` from query parameters.
    2.  Construct the full S3 key by prepending `bemsid/` to the `filename`.
    3.  Call `file_task.download_file()` to initiate the download from S3.
    4.  Return the result from `download_file`.
-   **Authentication:** None explicitly mentioned.
-   **Errors:**
    *   `400 Bad Request`: If an unexpected error occurs.
    *   `404 Not Found`: If the file is not found in S3.
    *   `500 Internal Server Error`: General server error.

#### `GET` `/export-esb` — `export.py`
-   **Purpose:** Initiates the creation of an ESB file for download given test point IDs and uploads it to S3.
-   **Request:** Query Parameters
    *   `testPointIds` (array of strings, optional): IDs of test points to include in the file.
    *   `bemsid` (number, optional, defaults to 123): User's BEMS ID for S3 upload.
    *   `filename` (string, required): The desired name for the exported file.
-   **Response:**
    *   `200 OK`: A string indicating the Celery task ID for file generation.
-   **Logic Flow:**
    1.  Retrieve `testPointIds`, `bemsid`, and `filename` from query parameters.
    2.  Call `file_task.create_esb.delay()` to start an asynchronous Celery task for ESB generation and upload.
    3.  Return the Celery task ID.
-   **Authentication:** None explicitly mentioned.
-   **Errors:**
    *   `404 Not Found`: If `FileNotFoundError` occurs during task creation.
    *   `500 Internal Server Error`: General server error.

#### `GET` `/export-esa` — `export.py`
-   **Purpose:** Initiates the creation of an ESA file for download given test point IDs and uploads it to S3.
-   **Request:** Query Parameters
    *   `testPointIds` (array of strings, optional): IDs of test points to include in the file.
    *   `bemsid` (number, optional, defaults to 123): User's BEMS ID for S3 upload.
    *   `filename` (string, required): The desired name for the exported file.
-   **Response:**
    *   `200 OK`: A string indicating the Celery task ID for file generation.
-   **Logic Flow:**
    1.  Retrieve `testPointIds`, `bemsid`, and `filename` from query parameters.
    2.  Call `file_task.create_esa.delay()` to start an asynchronous Celery task for ESA generation and upload.
    3.  Return the Celery task ID.
-   **Authentication:** None explicitly mentioned.
-   **Errors:**
    *   `404 Not Found`: If `FileNotFoundError` occurs during task creation.
    *   `500 Internal Server Error`: General server error.

### `api/route/upload.py`

#### `POST` `/upload-csv` — `upload.py`
-   **Purpose:** Uploads a CSV file, processes it, and initiates an S3 upload.
-   **Request:** Form Data
    *   `bemsid` (number, required): The BEMS ID for S3 upload.
    *   `file` (file, required): The CSV file to upload.
    *   `autoincrement` (boolean, optional): Flag to enable autoincrement for tags.
    *   `tags` (string, optional): Comma-separated list of tags.
-   **Response:**
    *   `200 OK`: A success message string: `"file is ready to be exported!! "`.
-   **Logic Flow:**
    1.  Retrieve the uploaded file and form data (`bemsid`, `autoincrement`, `tags`).
    2.  Save the uploaded file locally using `secure_filename`.
    3.  Call `file_task.get_tags()` to parse and process the provided tags.
    4.  Call `file_task.read_file()` to process the CSV content, extract data and tags, and post to the Test Service.
    5.  Call `file_task.upload_csv.delay()` to asynchronously upload the file to S3.
    6.  Return a success message.
-   **Authentication:** None explicitly mentioned, but `bemsid` implies user context.
-   **Errors:**
    *   `404 Not Found`: If `FileNotFoundError` occurs.
    *   `500 Internal Server Error`: General server error.

## 4. Services

### `api/model/test_service.py`

-   **What it does:** Provides a client for interacting with an external Test Service API.
-   **Functions:**
    *   `__init__(self, base_url="http://localhost:8080", insecure=True)`: Initializes the service client with a base URL and an option for insecure connections.
    *   `get_test_points(self, test_point_ids, include_data)`: Makes a GET request to the `/api/v1/test-points` endpoint to retrieve test point data.
        *   **Connects to:** External Test Service API.
    *   `post_test_points(self, test_point_data)`: Makes a POST request to the `/api/v1/test-points` endpoint to send test point data.
        *   **Connects to:** External Test Service API.
-   **Connects to:** External Test Service API.

### `api/model/user_service.py`

-   **What it does:** Provides a client for interacting with an external User Service API, specifically for sending notifications.
-   **Functions:**
    *   `__init__(self, base_url="http://localhost:8085", insecure=True)`: Initializes the service client with a base URL and an option for insecure connections.
    *   `post_notification(self, bemsid="123456", message="No Message", status="failure")`: Makes a POST request to the `/api/v1/users/{bemsid}/user-notification` endpoint to send a notification to a user.
        *   **Connects to:** External User Service API.
-   **Connects to:** External User Service API.

### `api/model/welcome.py`

-   **What it does:** A simple data model for holding a welcome message.
-   **Functions:**
    *   `__init__(self, message)`: Initializes the model with a message string.
-   **Connects to:** No external systems.

### `file_task.py` (Celery Tasks)

-   **What it does:** Defines asynchronous tasks executed by Celery workers for background processing, including file generation, S3 operations, and service interactions.
-   **Functions:**
    *   `get_test_service()`: Factory function to get an instance of `TestService`.
    *   `get_user_service()`: Factory function to get an instance of `UserService`.
    *   `get_filename(filename="_RocData.csv")`: Generates a timestamped filename.
    *   `get_data_frame(test_service_client, test_point_ids=None)`: Retrieves data from the Test Service and returns it as a DataFrame.
    *   `post_notification(user_service_client, bemsid, message, status)`: Helper to post notifications via the User Service.
    *   `get_data_map(test_point_ids=None)`: Retrieves test point data and structures it into a map suitable for ESB/ESA generation.
    *   `create_csv(test_point_ids=None, userid="example", filename="_RocData.csv")`: Celery task to create a CSV file, upload it to S3, and send a success notification.
    *   `create_esb(test_point_ids=None, userid="example", filename="_RocData.esb")`: Celery task to create an ESB file, upload it to S3, and send a success notification.
    *   `create_esa(test_point_ids=None, userid="example", filename="_RocData.esa")`: Celery task to create an ESA file, upload it to S3, and send a success notification.
    *   `upload_csv(userid="example", filename="example.csv")`: Celery task to upload a CSV file to S3 and send a notification.
    *   `download_file(local_filename, filename)`: Calls `s3_bucket.download_from_s3` to download a file.
    *   `delete_file_from_s3(filename)`: Calls `s3_bucket.delete_file_from_s3` to delete a file.
    *   `get_tags(request)`: Parses tags from an incoming request.
    *   `to_numeric(inp_str)`: Helper to convert strings to numeric types.
    *   `has_empty_tags(entry)`: Checks if a tag entry is empty.
    *   `read_file(csv_file, tags, inc_csv_tags, use_csv_tags, num_key_list)`: Reads a CSV file, processes its content, and posts data to the Test Service.
-   **Connects to:**
    *   External Test Service API (via `TestService` client).
    *   External User Service API (via `UserService` client).
    *   S3-compatible object storage (via `s3_bucket` module).
    *   Celery broker (e.g., Redis) for task queuing.

### `s3_bucket.py`

-   **What it does:** Handles interactions with an S3-compatible object storage service.
-   **Functions:**
    *   `set_s3_lifecycle(client, bucket, userid)`: Configures lifecycle rules for a bucket to expire objects after a specified number of days for a given user prefix.
    *   `get_connection()`: Establishes and returns a boto3 S3 client connection using environment variables for endpoint and credentials.
    *   `upload_file(userid, file_name)`: Uploads a local file to the specified S3 bucket with a user-specific prefix.
    *   `get_dictionary(name, last_modified, days=30)`: Helper function to format S3 object metadata into a dictionary.
    *   `get_folder_info(bemsid)`: Lists objects in the S3 bucket under a given BEMS ID prefix and returns their metadata.
    *   `download_from_s3(local_filename, filename)`: Downloads a file from S3 to a local path and returns it as a Flask response for streaming.
    *   `delete_file_from_s3(filename)`: Deletes a file from the S3 bucket.
-   **Connects to:** S3-compatible object storage service.

## 5. Database & External Connections

*   **Database:** No explicit database (like SQL or NoSQL) is directly managed or connected to by this Flask application. Data persistence is handled via S3 object storage and interactions with external services.
*   **Connection Management:**
    *   **Test Service:** Connections are managed by the `TestService` class in `api/model/test_service.py`, using `requests`. Connection details (host, port) are configurable via environment variables.
    *   **User Service:** Connections are managed by the `UserService` class in `api/model/user_service.py`, using `requests`. Connection details (host, port) are configurable via environment variables.
    *   **S3-Compatible Storage:** Connections are managed by the `get_connection()` function in `s3_bucket.py`, using `boto3`. Connection details (host, credentials, bucket name) are configurable via environment variables.
    *   **Celery:** Uses a message broker (e.g., Redis) for task queuing. The broker URL is configured via `CELERY_BROKER_URL` environment variable.
*   **External Services Called:**
    *   **Test Service:** An external API providing test point data.
    *   **User Service:** An external API for user notifications.
    *   **S3-Compatible Object Storage:** For storing and retrieving generated files.
    *   **Celery Workers:** For asynchronous task execution.

---

*AI-generated documentation — 2026-06-22 15:47:39*
*Review for accuracy. AI may misinterpret complex logic.*
