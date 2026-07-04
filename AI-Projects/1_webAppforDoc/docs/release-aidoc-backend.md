# Backend — AI-Generated Documentation

**Generated:** 2026-06-22 15:34:56
**Source:** `C:\Users\du974f\Desktop\3 Backend-Python\1_CustomScripts`
**Files Analyzed:** 89
**AI Provider:** Google Gemini (FREE)

---

This is a BACKEND project.

## 1. Project Setup

### Dependencies and Server Start

The project uses Python with Flask. Dependencies are managed by `pip` and can be installed using:

```bash
pip install -r requirements.txt
```

The server can be started using Gunicorn, as configured in `gunicorn_config.py`. A typical command to run the server would be:

```bash
gunicorn --config gunicorn_config.py app:app
```

The `app.py` file (or `run.py` in the archive) likely initializes the Flask application and registers blueprints.

### Environment Variables

The following environment variables are used:

*   `jwt_secret`: Secret key for JWT token generation and validation.
*   `JAVA_SERVER_IP`: IP address or hostname of the Java server.
*   `DB_PATH`: Path to the SQLite database file. Defaults to `./database/CRTDBNewSync.db`.
*   `BASE_PATH`: Base directory for file operations, particularly for data abstraction. Defaults to `C:/`.
*   `SINEDATACODES`: Path to the directory containing sine data codes. Defaults to `./database/sinedatacodes`.
*   `FFTDATAPOINTS`: Path to the directory containing FFT data points. Defaults to `./database/FFTDatapoints`.

### Configuration Files

*   `config.yaml`: Contains configuration for routes, potentially including paths, method types, and JWT requirements. This file is used by `app/routes/api_docs.py` to generate OpenAPI specifications.
*   `gunicorn_config.py`: Configuration for the Gunicorn web server.
*   `app/config/configuration.yaml`: App-specific configuration.

## 2. Folder Structure

*   **`app/`**: Contains the main application code.
    *   **`__init__.py`**: Initializes the Flask application.
    *   **`config/`**: Application configuration files.
        *   `configuration.yaml`: Specific application configurations.
    *   **`routes/`**: Defines the API endpoints (routes) of the application. Each file typically handles a specific set of related API calls.
        *   `api_docs.py`: Generates OpenAPI documentation.
        *   `applyAlgorithm.py`: Handles applying algorithms to data.
        *   `argoStatus.py`: Fetches Argo workflow statuses.
        *   `baselineplot.py`: Retrieves baseline plot data.
        *   `checkAuth.py`: Checks JWT authentication.
        *   `crtdbuserevents.py`: Manages CRTDB user events.
        *   `currentUserRequestTree.py`: Generates a user request tree.
        *   `customExportWorkflow.py`: Handles custom export workflow requests.
        *   `dataExportWorkflow.py`: Manages data export workflows.
        *   `dataRequests.py`: Handles data request operations.
        *   `dataRequestsUnique.py`: Retrieves unique data requests.
        *   `datacodes.py`: Manages datacode information.
        *   `datapoints.py`: Retrieves data points.
        *   `datastats.py`: Provides data statistics.
        *   `deleteCustomEvent.py`: Deletes custom events.
        *   `deleteDataRequest.py`: Deletes data requests.
        *   `deleteReqidDataAbs.py`: Deletes data abstraction requests by ID.
        *   `events.py`: Manages event data.
        *   `fftdatapoints.py`: Retrieves FFT data points.
        *   `fftmaxfrequency.py`: Retrieves maximum frequency for FFT.
        *   `importXml.py`: Imports data from XML.
        *   `listPTTDataAbs.py`: Lists PTT (Project-Tail-Test) data for abstraction.
        *   `listReqidsDataAbs.py`: Lists request IDs for data abstraction.
        *   `login.py`: Handles user login and JWT generation.
        *   `modifiedEvents.py`: Retrieves modified events.
        *   `modifyDataRequest.py`: Modifies existing data requests.
        *   `ping.py`: Simple ping endpoint for health checks.
        *   `proj_tail_test.py`: Handles project, tail, and test related operations.
        *   `rainflowExportWorkflow.py`: Manages Rainflow export workflows.
        *   `readJsonDataAbs.py`: Reads JSON data for abstraction.
        *   `revertChanges.py`: Reverts changes to data.
        *   `route_handler.py`: A general route handler.
        *   `saveDataRequest.py`: Saves data requests.
        *   `saveModifiedData.py`: Saves modified data.
        *   `saveModifiedEvents.py`: Saves modified events.
        *   `shareDataRequest.py`: Shares data requests.
        *   `sharedDataRequests.py`: Retrieves shared data requests.
        *   `spectrumScalingValues.py`: Manages spectrum scaling values.
        *   `statsExportWorkflow.py`: Manages statistics export workflows.
        *   `testStartEndTime.py`: Handles test start and end times.
        *   `uploadUserEvents.py`: Uploads user events.
        *   `userEvents.py`: Manages user events.
    *   **`services/`**: Contains business logic, utility functions, and integrations with external systems.
        *   `auth.py`: Authentication related services (e.g., JWT generation).
        *   `db.py`: Database connection management (likely for SQLite).
        *   `file_manager.py`: File management utilities.
        *   `filter_utils.py`: Utility for applying filters to queries.
        *   `mssql.py`: MSSQL database connection.
        *   `request_handler.py`: Handles request processing.
        *   `argo/`: Services related to Argo workflows.
            *   `common.py`: Common utilities for Argo workflows.
            *   `customexport_workflow.py`: Generates custom export workflows.
            *   `dataexport_workflow.py`: Generates data export workflows.
            *   `generate_yaml.py`: Generates YAML files.
            *   `rainflowexport_workflow.py`: Generates Rainflow export workflows.
            *   `statexport_workflow.py`: Generates state export workflows.
            *   `workflow.py`: General workflow service.
        *   `dll/`: Services interacting with Dynamic Link Libraries (DLLs).
            *   `cache.py`: Caching utilities.
            *   `datacodes_dll_interface.py`: Interface for datacodes DLL.
            *   `datapoints_dll_interface.py`: Interface for datapoints DLL.
            *   `events_dll_interface.py`: Interface for events DLL.
            *   `ptt_dll_interface.py`: Interface for PTT DLL.
            *   `start_end_times_interface.py`: Interface for start/end times.
*   **`tests/`**: Contains unit and integration tests for the application.
    *   `conftest.py`: Pytest configuration.
    *   `test_app.py`: Tests for the Flask application.
    *   `test_argo.py`: Tests related to Argo workflows.
*   **`z_archive/`**: Contains older or deprecated code.
*   **`.gitlab-ci.yml`**: GitLab CI/CD configuration.
*   **`Dockerfile`**: Docker configuration for building the application image.
*   **`config.yaml`**: General configuration file.
*   **`docker-compose.yml`**: Docker Compose configuration for orchestrating services.
*   **`gunicorn_config.py`**: Gunicorn server configuration.
*   **`manifest.yml`**: Cloud Foundry manifest file.
*   **`run.py`**: Script to run the application.

## 3. API Endpoints (Routes)

### `GET` `/health` - `app/server.js`

*   **Purpose:** Checks the health status of the Node.js proxy server.
*   **Request:** None
*   **Response:**
    ```json
    {
      "status": "Node.js proxy server is running",
      "port": 3001,
      "timestamp": "2023-10-27T10:00:00.000Z",
      "services": {
        "springBoot": "https://localhost:8443",
        "pythonFlask": "http://localhost:8444"
      }
    }
    ```
*   **Flow:**
    1.  The server receives a GET request to `/health`.
    2.  It constructs a JSON response containing the server's status, port, current timestamp, and the URLs of the backend services it proxies.
    3.  The JSON response is sent back to the client.
*   **Auth:** None
*   **Errors:** None

### `GET` `/api/proxy/currentuser` - `app/server.js`

*   **Purpose:** Mocks the retrieval of the current user's information.
*   **Request:** None
*   **Response:**
    ```json
    {
      "bemsid": "3704327",
      "name": "Bhavana",
      "email": "3704327@boeing.com"
    }
    ```
    Additionally, sets the `boeingdisplayname` header to "Bhavana".
*   **Flow:**
    1.  The server receives a GET request to `/api/proxy/currentuser`.
    2.  It logs a message indicating the mock request.
    3.  It sets the `boeingdisplayname` response header.
    4.  It sends a predefined JSON object containing user details.
*   **Auth:** None
*   **Errors:** None

### `GET` `/api/proxy/auth/GroupMembersBemsID` - `app/server.js`

*   **Purpose:** Mocks the retrieval of group members' BEMS IDs.
*   **Request:**
    *   `query` (optional): Parameters for the mock request.
*   **Response:**
    ```json
    {
      "data": [
        { "bemsid": "3704327", "name": "Bhavana" },
        { "bemsid": "3664671", "name": "Prakash" },
        { "bemsid": "3229755", "name": "Madhan" }
      ]
    }
    ```
*   **Flow:**
    1.  The server receives a GET request to `/api/proxy/auth/GroupMembersBemsID`.
    2.  It logs the received query parameters.
    3.  It sends a predefined JSON array of mock group members.
*   **Auth:** None
*   **Errors:** None

### `ALL` `/api/proxy/*` - `app/server.js`

*   **Purpose:** Proxies requests to backend services (Spring Boot or Python Flask).
*   **Request:** Any HTTP method (GET, POST, PUT, DELETE, etc.) with any JSON body for methods that support it. Headers are forwarded.
*   **Response:** The response from the proxied backend service, including status code, headers, and JSON body.
*   **Flow:**
    1.  The server receives a request to `/api/proxy/*`.
    2.  It extracts the target path by removing `/api/proxy` from the original URL.
    3.  It determines the target API URL:
        *   If the `targetPath` contains `/boeing/crtdb/`, it routes to the Python Flask server (`http://localhost:8444`).
        *   Otherwise, it routes to the Spring Boot server (`https://localhost:8443`).
    4.  It constructs `axiosOptions` including the method, URL, forwarded headers, and a timeout.
    5.  For Spring Boot requests (`useSSL = true`), it attempts to load SSL certificates (`CRTDB_Client.crt`, `CRTDB_Client.key`) and configures `httpsAgent` for mutual TLS. If certificates are not found, it proceeds with `rejectUnauthorized: false`.
    6.  If the request method is POST, PUT, PATCH, or DELETE, the request body (`req.body`) is included in `axiosOptions.data`.
    7.  `axios` is used to make the request to the determined backend API.
    8.  The response headers from the backend are forwarded to the client, excluding `Content-Encoding`, `Transfer-Encoding`, and `Connection`.
    9.  The backend's status code and JSON data are sent back to the client.
*   **Auth:** None (authentication is handled by the backend services).
*   **Errors:**
    *   `503 Service Unavailable`: If the target service (Python Flask or Spring Boot) is unreachable (`ECONNREFUSED`).
    *   `502 Bad Gateway`: If the backend service is not found (`ENOTFOUND`).
    *   `500 Internal Server Error`: For other proxy request failures.
    *   Backend-specific errors (e.g., 4xx, 5xx) are forwarded.

### `OPTIONS` `*` - `app/server.js`

*   **Purpose:** Handles CORS preflight requests.
*   **Request:** `OPTIONS` method with various headers.
*   **Response:**
    *   `Access-Control-Allow-Origin`: `http://localhost:3000`
    *   `Access-Control-Allow-Methods`: `GET, POST, PUT, DELETE, OPTIONS`
    *   `Access-Control-Allow-Headers`: `Content-Type, Authorization, X-Requested-With`
    *   Status Code: `200 OK`
*   **Flow:**
    1.  The server receives an `OPTIONS` request.
    2.  It sets the necessary CORS headers to allow cross-origin requests from the specified origin and with the allowed methods and headers.
    3.  It sends a `200 OK` response.
*   **Auth:** None
*   **Errors:** None

### `ALL` `*` - `app/server.js`

*   **Purpose:** Catches all unhandled routes.
*   **Request:** Any HTTP method to any path not explicitly defined.
*   **Response:**
    ```json
    {
      "error": "Route not found",
      "method": "METHOD",
      "path": "/path",
      "availableRoutes": [
        "GET /health",
        "GET /api/proxy/currentuser",
        "GET /api/proxy/auth/GroupMembersBemsID",
        "ALL /api/proxy/boeing/crtdb/*",
        "ALL /api/proxy/*"
      ]
    }
    ```
    Status Code: `404 Not Found`.
*   **Flow:**
    1.  The server receives a request to a path that is not explicitly handled by other routes.
    2.  It logs the unhandled request.
    3.  It constructs a `404 Not Found` JSON response listing the available routes.
    4.  The response is sent back to the client.
*   **Auth:** None
*   **Errors:** `404 Not Found` with details of the unhandled route and available routes.

### `GET` `/api-docs/openapi.json` - `app/routes/api_docs.py`

*   **Purpose:** Serves the OpenAPI specification in JSON format.
*   **Request:** None
*   **Response:** OpenAPI 3.0 specification in JSON format.
*   **Flow:**
    1.  The server receives a GET request to `/api-docs/openapi.json`.
    2.  The `_build_openapi_spec()` function is called to construct the OpenAPI specification.
    3.  This function introspects MSSQL schemas (`_get_mssql_schemas`) and reads route definitions from `config.yaml` (`_build_route_paths`).
    4.  The generated OpenAPI specification (a Python dictionary) is converted to JSON.
    5.  The JSON response is sent back to the client.
*   **Auth:** None
*   **Errors:** None (errors during schema introspection are logged and fallback schemas are used).

### `GET` `/api-docs` - `app/routes/api_docs.py`

*   **Purpose:** Serves the Scalar UI for API documentation.
*   **Request:** None
*   **Response:** HTML content embedding the Scalar API Reference UI.
*   **Flow:**
    1.  The server receives a GET request to `/api-docs`.
    2.  It returns a static HTML string that includes JavaScript to load the Scalar API Reference component.
    3.  The Scalar component is configured to fetch its specification from `/api-docs/openapi.json`.
*   **Auth:** None
*   **Errors:** None

### `POST` `/applyAlgorithm` - `app/routes/applyAlgorithm.py`

*   **Purpose:** Applies a specified algorithm to baseline data.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "algorithm": {
        "type": "string", // e.g., "addition", "multiply", "spike detection"
        "parameters": {
          // Algorithm-specific parameters
        }
      },
      "baselineData": {
        "value": [number], // Array of numbers
        "dataCodeName": "string",
        "eventId": "string",
        "tStart": "string",
        "rate": "number",
        "bandwidth": "number"
      }
    }
    ```
*   **Response:**
    ```json
    {
      "success": true,
      "data": {
        "processedData": {
          "value": [number], // Processed data array
          "dataCodeName": "string",
          "eventId": "string",
          "tStart": "string",
          "rate": "number",
          "bandwidth": "number"
        },
        "metadata": {
          "project": "string",
          "tail": "string",
          "test": "string",
          "algorithmVersion": "string" // e.g., "1.0.0"
        }
      }
    }
    ```
    Or an error response:
    ```json
    {
      "success": false,
      "error": "string" // Error message
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with algorithm parameters and baseline data.
    2.  It logs the received data keys.
    3.  It extracts `project`, `tail`, `test`, `algorithm`, and `baseline` from the request.
    4.  It validates that all required fields are present.
    5.  It extracts `algo_type`, `params`, and `values` from the algorithm and baseline data.
    6.  Based on `algo_type`:
        *   **"addition"**: Adds `params.value` to each element in `values`.
        *   **"multiply"**: Multiplies each element in `values` by `params.value`.
        *   **"spike detection"**: Implements a simple moving average spike detection algorithm using `mov_avg_period`, `deviation_threshold`, and `slope_threshold` from parameters.
    7.  If an unknown `algo_type` is provided, it returns an error.
    8.  It constructs the `processed` data array.
    9.  It returns a success JSON response containing the `processedData` and `metadata`.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required fields are missing.
    *   `400 Bad Request`: If an unknown algorithm type is provided.
    *   `500 Internal Server Error`: If any other exception occurs during processing.

### `POST` `/argoStatus` - `app/routes/argoStatus.py`

*   **Purpose:** Fetches the status of Argo workflows based on provided request IDs.
*   **Request:**
    ```json
    {
      "requestIds": ["string", ...] // List of workflow names (request IDs)
    }
    ```
*   **Response:**
    ```json
    {
      "err_msg": "Success", // or error message
      "err_no": 0, // 0 for success, non-zero for errors
      "data": [
        { "workflow_name_1": { "status": "string", "request_type": "string", "parameters": {} } },
        ...
      ]
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with a JSON body containing a list of `requestIds`.
    2.  It validates that the input is a JSON object and `requestIds` is a list.
    3.  It cleans and decodes the `requestIds`, filtering out empty strings.
    4.  It connects to the MSSQL database.
    5.  It constructs and executes a SQL query to fetch `workflow_name`, `status`, `request_type`, and `parameters` from the `argo_workflow_requests` table for the given `workflow_name`s.
    6.  It processes the database results into a `data_map` where keys are workflow names and values are their details.
    7.  It iterates through the original `request_ids` to construct the final `statuses` list, ensuring that even unknown IDs are represented with "unknown" status.
    8.  It returns a JSON response containing the statuses or an error message.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If the input is not valid JSON or `requestIds` is not a list.
    *   `500 Internal Server Error`: If a database error occurs.
    *   `500 Internal Server Error`: For other unexpected exceptions.

### `POST` `/baselineplot` - `app/routes/baselineplot.py`

*   **Purpose:** Retrieves baseline data for a given event and datacode, and checks for modified data.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string",
      "start_time": "string", // Optional
      "end_time": "string",   // Optional
      "modified": false,      // Optional, defaults to false
      "owner": "string",      // Optional
      "x": "number"           // Optional
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "dataCodeName": "string",
        "eventId": "string",
        "dataCodeType": "string",
        "tStart": "string",
        "tLag": "string",
        "value": [number], // Array of float values from file
        "offset": "number",
        "rate": "number",
        "bandwidth": "number",
        "ts": "string",
        "ns": "string",
        "modifiedValue": [number], // Present if modified data exists
        "modifiedAlgo": "string",  // Present if modified data exists
        "modifiedParameters": {},  // Present if modified data exists
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an empty `data` object if no matching event is found.
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, datacode, and eventid.
    2.  It logs the request and extracts parameters.
    3.  It validates that required parameters are present.
    4.  It connects to the SQLite database.
    5.  It queries the `crtdb_sin` table to retrieve information about the specified `eventid` and `datacode`.
    6.  If a matching row is found, it reads the data values from the file specified by `file_path` using `read_data_from_file`.
    7.  It constructs a `datapoints` dictionary with the retrieved information and file data.
    8.  It then queries the `crtdb_modified_data` table to check if modified data exists for the same project, tail, test, eventid, and datacode.
    9.  If modified data is found and its `algo_type` is not "BASELINE", it adds `modifiedValue`, `modifiedAlgo`, and `modifiedParameters` to the `datapoints` dictionary.
    10. It returns a JSON response containing the `datapoints` and success status.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations or file reading.

### `GET` `/isAuthorized` - `app/routes/checkAuth.py`

*   **Purpose:** Checks if a JWT token is valid and the user session is active.
*   **Request:**
    *   `Authorization` header: `Bearer <token>`
*   **Response:**
    ```json
    {
      "status": "success",
      "message": "user session is active",
      "data": {
        "username": "string",
        "bemsid": "string",
        "token": "string"
      }
    }
    ```
    Or an error response:
    ```json
    {
      "status": "failed",
      "message": "token is missing" // or "user session is inactive"
    }
    ```
*   **Flow:**
    1.  The server receives a GET request with an `Authorization` header.
    2.  It extracts the JWT token from the header.
    3.  If no token is found, it returns a `401 Unauthorized` error.
    4.  It uses `jwt.decode` to verify the token using the `JWT_SECRET_KEY` and `JAVA_SERVER_IP` (audience).
    5.  If the token is valid and decoded successfully, it returns a success response with user details.
    6.  If the token is invalid or expired, `jwt.decode` will raise an exception, leading to an "inactive session" error.
*   **Auth:** Required (JWT token in `Authorization` header).
*   **Errors:**
    *   `401 Unauthorized`: If the token is missing.
    *   `401 Unauthorized`: If the token is invalid or the session is inactive.
    *   `500 Internal Server Error`: For other processing errors.

### `GET` `/crtdb_user` and `POST` `/crtdb_user` - `app/routes/crtdbuserevents.py`

*   **Purpose:** Manages user data in the `crtdb_user` table. `GET` retrieves users, `POST` creates a new user.
*   **Request (GET):** None
*   **Request (POST):**
    ```json
    {
      "name": "string",
      "bemsid": "string",
      "email": "string", // Optional, defaults to f"{bemsid}@boeing.com"
      "role": "string"   // Optional, defaults to "user"
    }
    ```
*   **Response (GET):**
    ```json
    {
      "status": "success",
      "users": [
        { "bemsid": "string", "name": "string", "email": "string", "role": "string" },
        ...
      ]
    }
    ```
*   **Response (POST):**
    ```json
    {
      "status": "success",
      "message": "User inserted successfully",
      "user": {
        "name": "string",
        "bemsid": "string",
        "email": "string",
        "role": "string"
      }
    }
    ```
    Or an error response.
*   **Flow (GET):**
    1.  The server receives a GET request to `/crtdb_user`.
    2.  It connects to the SQLite database.
    3.  It checks if the `crtdb_user` table exists.
    4.  It queries all `bemsid`, `name`, `email`, and `role` from the `crtdb_user` table.
    5.  It formats the results into a list of user objects.
    6.  It returns a success JSON response with the list of users.
*   **Flow (POST):**
    1.  The server receives a POST request with user data (`name`, `bemsid`, `email`, `role`).
    2.  It connects to the SQLite database.
    3.  It validates that `name` and `bemsid` are provided.
    4.  It checks if a user with the given `bemsid` or `name` already exists. If so, it returns a `409 Conflict` error.
    5.  It inserts the new user into the `crtdb_user` table.
    6.  It commits the transaction.
    7.  It returns a success JSON response with the created user's details.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: If the `crtdb_user` table is not found.
    *   `400 Bad Request`: If `name` or `bemsid` are missing in POST request.
    *   `409 Conflict`: If a user with the same `bemsid` or `name` already exists.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/currentUserRequestTree` - `app/routes/currentUserRequestTree.py`

*   **Purpose:** Generates a hierarchical tree structure of user data requests based on provided criteria.
*   **Request:**
    ```json
    {
      "dataRequestMade": integer,
      "owner": "string",
      "project": "string", // Can be "project - tail - test"
      "tail": "string",    // Optional, if not provided, parsed from project
      "test": "string",     // Optional, if not provided, parsed from project
      "req_type": "string"  // Optional, e.g., "all"
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "id": "string", // Owner ID
          "label": "string", // Owner name
          "value": "string", // Owner name
          "disabled": true,
          "child": true,
          "currentLevel": "FIRST",
          "nextLevel": "SECOND",
          "children": [
            {
              "id": "string", // Data request ID
              "previousNodeId": "string", // Owner ID
              "label": "string", // Data request ID
              "value": "{}", // JSON string
              "disabled": false,
              "child": false,
              "currentLevel": "SECOND",
              "nextLevel": "SECOND"
            },
            ...
          ]
        }
      ],
      "err_msg": "Success", // or "No data found"
      "err_no": 0 // or 2 for no data, 500 for internal error
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with user request details.
    2.  It extracts `dataRequestMade`, `owner`, `project`, `tail`, `test`, and `req_type`.
    3.  If `tail` or `test` are not provided, it parses them from the `project` string (assuming "project - tail - test" format).
    4.  It connects to the SQLite database specified by `DB_PATH`.
    5.  It constructs a SQL query to select data request content from `crtdb_data_request_content` based on the provided `owner`, `data_request_made`, `project`, `tail`, and `test`.
    6.  If `req_type` is provided and not "all", it adds a filter for `req_type`.
    7.  It executes the query and fetches all matching rows.
    8.  It calls `create_tree_data` to structure the fetched data into a hierarchical format: an owner node with children representing data requests.
    9.  It prepares and returns a JSON response with the tree data or an appropriate error message.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: If any exception occurs during database operations or processing.

### `GET` `/customExportWorkflow` and `POST` `/customExportWorkflow` - `app/routes/customExportWorkflow.py`

*   **Purpose:** Manages custom export workflows. `GET` retrieves existing workflow data, `POST` creates a new workflow.
*   **Request (GET):**
    *   `requestID` (query parameter): The ID of the workflow to retrieve.
*   **Request (POST):**
    *   `Content-Type`: `application/json` or `multipart/form-data`.
    *   **JSON Body:**
        ```json
        {
          "dataRequestID": "string",
          "req_type": "string", // e.g., "custom-export"
          "ownerID": "string",
          "project": "string",
          "tail": "string",
          "test": "string",
          "owner": "string",
          "events": [{}], // Array of event objects
          "datacodes": [{}], // Array of datacode objects
          "description": "string",
          "parameters": {}, // Object of parameters
          "files": [ // Metadata for uploaded files
            { "name": "string", "argument": "string" }
          ]
        }
        ```
    *   **Multipart Form Data:** Individual form fields for the above JSON properties, plus `files[]` for file uploads.
*   **Response (GET):**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "owner": "string",
        "ownerID": "string",
        "project": "string",
        "tail": "string",
        "test": "string",
        "description": "string",
        "parameters": {},
        "req_type": "string"
      },
      "err_no": 0,
      "err_msg": "Success"
    }
    ```
*   **Response (POST):**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "dataRequestMade": null, // Or timestamp if saved
        "datacodes": [{}],
        "description": "string",
        "events": [{}],
        "owner": "string",
        "ownerID": "string",
        "project": "string",
        "req_type": "string",
        "tail": "string",
        "test": "string"
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an error response.
*   **Flow (GET):**
    1.  The server receives a GET request with a `requestID` query parameter.
    2.  It connects to the SQLite database (`db_path`).
    3.  It queries `crtdb_data_request_content` for the given `data_requestid`.
    4.  If found, it returns the request details.
    5.  If not found, it returns a `404 Not Found` error.
*   **Flow (POST):**
    1.  The server receives a POST request, potentially with `multipart/form-data` or `application/json`.
    2.  It parses the payload, extracting workflow details and handling file uploads.
    3.  Uploaded files are saved to a directory structure based on `BASE_PATH/<bemsid>/uploads/`.
    4.  It constructs `workflow_input` dictionary with all the necessary parameters for workflow generation.
    5.  It calls `generate_custom_export_workflow` from `app.services.argo.customexport_workflow`.
    6.  It checks the response from the workflow generation service. If successful, it proceeds to save the request details into `crtdb_data_request_content`.
    7.  It returns a success response with the saved request details.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Missing `requestID` (GET), invalid content type, invalid payload, missing required fields (POST).
    *   `404 Not Found`: If `requestID` is not found (GET).
    *   `500 Internal Server Error`: For file saving errors, JSON parsing errors, or workflow generation failures.

### `GET` `/dataExportWorkflow` and `POST` `/dataExportWorkflow` - `app/routes/dataExportWorkflow.py`

*   **Purpose:** Manages data export workflows. `GET` retrieves existing workflow data, `POST` creates a new workflow.
*   **Request (GET):**
    *   `requestID` (query parameter): The ID of the workflow to retrieve.
*   **Request (POST):**
    *   `Content-Type`: `application/json`.
    *   **JSON Body:**
        ```json
        {
          "dataRequestID": "string",
          "dataRequestMade": integer, // Optional
          "datacodes": [{}],
          "description": "string",
          "events": [{}],
          "owner": "string",
          "ownerID": "string",
          "project": "string",
          "tail": "string",
          "test": "string",
          "req_type": "string",
          "parameters": { // Optional, contains various export parameters
            "lossOfLock": 0,
            "syncDiffRateParams": 0,
            // ... other parameters
          }
        }
        ```
*   **Response (GET):**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "owner": "string",
        "ownerID": "string",
        "project": "string",
        "tail": "string",
        "test": "string",
        "description": "string",
        "events": [{}],
        "datacodes": [{}],
        "parameters": {},
        "req_type": "string"
      },
      "err_no": 0,
      "err_msg": "Success"
    }
    ```
*   **Response (POST):**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "owner": "string",
        "content": null,
        "events": [{}],
        "datacodes": [{}],
        "dataRequestMade": "integer", // or null
        "ownerID": "string",
        "project": "string",
        "tail": "string",
        "test": "string",
        "description": "string",
        "parameters": {},
        "req_type": "string"
      },
      "err_no": 0,
      "err_msg": "Success"
    }
    ```
    Or an error response.
*   **Flow (GET):**
    1.  The server receives a GET request with a `requestID` query parameter.
    2.  It connects to the SQLite database (`DB_PATH`).
    3.  It queries `crtdb_data_request_content` for the given `data_requestid`.
    4.  If found, it parses JSON fields (`events`, `datacodes`, `parameters`) and returns the request details.
    5.  If not found, it returns a `404 Not Found` error.
*   **Flow (POST):**
    1.  The server receives a POST request with JSON data for a data export workflow.
    2.  It validates the incoming request format and required fields (`dataRequestID`, `owner`, `project`, `ownerID`).
    3.  It constructs a `workflow_input` dictionary, extracting parameters and setting defaults for description if needed.
    4.  It calls `generate_ftlist_workflow` from `app.services.argo.dataexport_workflow` to generate the workflow.
    5.  If workflow generation is successful, it inserts the request details into the `crtdb_data_request_content` table in the SQLite database.
    6.  It returns a success response with the saved request details.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Missing `requestID` (GET), invalid request format, missing required fields (POST).
    *   `404 Not Found`: If `requestID` is not found (GET).
    *   `500 Internal Server Error`: For database errors, JSON parsing errors, or workflow generation failures.

### `POST` `/dataRequests` - `app/routes/dataRequests.py`

*   **Purpose:** Retrieves data requests for a given owner, optionally filtered by a list of `requestIDs`.
*   **Request:**
    ```json
    {
      "owner": "string",
      "requestIDs": ["string", ...] // Optional list of request IDs
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "content": "default",
          "dataRequestID": "string",
          "dataRequestMade": integer,
          "datacodes": [{}],
          "description": "string",
          "events": [{}],
          "owner": "string",
          "ownerID": "string",
          "project": "string",
          "tail": "string",
          "test": "string"
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with `owner` and an optional list of `requestIDs`.
    2.  It validates the request format.
    3.  It connects to the SQLite database (`DB_PATH`).
    4.  It constructs a SQL query to select data request content from `crtdb_data_request_content` for the specified `owner`.
    5.  If `requestIDs` are provided, it adds an `IN` clause to filter by those IDs.
    6.  It executes the query and fetches the results.
    7.  It parses JSON fields (`datacodes`, `events`) from the database rows.
    8.  It formats the results into a list of data request objects.
    9.  It returns a success JSON response with the list of data requests.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If the request format is invalid.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/dataRequestsUnique` - `app/routes/dataRequestsUnique.py`

*   **Purpose:** Retrieves unique Project-Tail-Test (PTT) combinations for data requests made by a specific owner, filtered by `dataRequestMade = 1`.
*   **Request:**
    ```json
    {
      "owner": "string",
      "req_type": "string", // Not used in the query logic
      "dataRequestMade": 1 // Must be 1 for this endpoint
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        "string (e.g., 'Project - Tail - Test')",
        ...
      ],
      "err_msg": "Success", // or "No data available"
      "err_no": 0 // or 1 for no data
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with `owner`, `req_type`, and `dataRequestMade`.
    2.  It validates the request format.
    3.  It checks if `dataRequestMade` is exactly `1`. If not, it returns an empty data response.
    4.  It connects to the SQLite database (`DB_PATH`).
    5.  It queries `crtdb_data_request_content` for `project`, `tail`, and `test` where `owner` and `data_request_made` match.
    6.  It collects unique "Project - Tail - Test" strings into a set.
    7.  It converts the set to a list and returns it in a success JSON response.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If the request format is invalid.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/datacodes` - `app/routes/datacodes.py`

*   **Purpose:** Retrieves datacode information for a given Project, Tail, and Test, with optional filtering.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "owner": "string", // Optional
      "filterModel": { // Optional, for advanced filtering
        "items": [
          {
            "field": "string", // e.g., "datacode", "description"
            "operator": "string", // e.g., "contains", "equals"
            "value": "string"
          },
          ...
        ]
      },
      "filters": [ // Optional, simpler filter format
        {
          "field": "string",
          "operator": "string",
          "value": "string"
        },
        ...
      ]
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "lable": "string", // datacodeid
          "datacodeid": "string",
          "datacode": "string",
          "description": "string",
          "type": "string",
          "units": "string",
          "rate": "string"
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, and optional filtering parameters.
    2.  It parses the `filterModel` or `filters` into a unified `filter_model` structure.
    3.  If `tail` or `test` are not provided, it attempts to parse them from the `project` string.
    4.  It connects to the SQLite database.
    5.  It constructs a base SQL query to select datacode information from `crtdb_data`.
    6.  It uses `apply_filter_model` from `app.services.filter_utils` to dynamically add `WHERE` clauses and `ORDER BY` based on the provided filters.
    7.  It executes the query and fetches the results.
    8.  It formats the results into the expected JSON structure.
    9.  It returns a success JSON response with the datacode information.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: If any exception occurs during database operations or filtering.

### `POST` `/datapoints` - `app/routes/datapoints.py`

*   **Purpose:** Retrieves data points for a specific event and datacode.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string",
      "start_time": "string", // Optional
      "end_time": "string",   // Optional
      "modified": false,      // Optional, defaults to false
      "owner": "string",      // Optional
      "x": "number"           // Optional
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "dataCodeName": "string",
        "eventId": "string",
        "dataCodeType": "string",
        "tStart": "string",
        "tLag": "string",
        "value": [number], // Array of float values from file
        "offset": "number",
        "rate": "number",
        "bandwidth": "number",
        "ts": "string",
        "ns": "string"
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an empty `data` object if no matching event is found.
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, datacode, and eventid.
    2.  It logs the request and extracts parameters.
    3.  It validates that required parameters are present.
    4.  It connects to the SQLite database.
    5.  It queries the `crtdb_sin` table to retrieve information about the specified `eventid` and `datacode`.
    6.  If a matching row is found, it reads the data values from the file specified by `file_path` using `read_data_from_file`.
    7.  It constructs a `datapoints` dictionary with the extracted information and file data.
    8.  It returns a JSON response containing the `datapoints` and success status.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations or file reading.

### `POST` `/statistics` - `app/routes/datastats.py`

*   **Purpose:** Retrieves statistical data for a given event and datacode.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "eventid": "string",
      "datacode": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          // Statistics fields from crtdb_statistics table
          "Eventid": "string",
          "Datacodename": "string",
          // ... other fields
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, eventid, and datacode.
    2.  It validates that all required parameters are present.
    3.  It connects to the SQLite database.
    4.  It executes a SQL query to select all columns from `crtdb_statistics` for the given `eventid` and `datacode`.
    5.  It fetches all matching rows and their column names.
    6.  It formats the results into a list of dictionaries, where each dictionary represents a row.
    7.  It returns a success JSON response with the statistics data.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations.

### `POST` `/deleteCustomEvent` - `app/routes/deleteCustomEvent.py`

*   **Purpose:** Deletes a custom event from the `crtdb_modified_events` table.
*   **Request:**
    ```json
    {
      "id": "string", // Event ID to delete
      "project": "string",
      "tail": "string",
      "test": "string",
      "user": "string"
    }
    ```
*   **Response:**
    *   Success: `{"data": {"successResponse": 0}, "err_msg": "Success", "err_no": 0}`
    *   Not Found: `{"data": {"successResponse": 1}, "err_msg": "Event not found", "err_no": 1}` (Status 404)
    *   Error: `{"data": {"successResponse": 1}, "err_msg": "string", "err_no": 1}`
*   **Flow:**
    1.  The server receives a POST request with event details (`id`, `project`, `tail`, `test`, `user`).
    2.  It logs the deletion attempt.
    3.  It connects to the SQLite database.
    4.  It executes a `DELETE` SQL statement on `crtdb_modified_events` matching the provided `id`, `project`, `tail`, `test`, and `user`.
    5.  It commits the transaction.
    6.  If `cursor.rowcount` is greater than 0 (meaning a row was deleted), it returns a success response.
    7.  Otherwise, it returns a "Event not found" error with a 404 status.
*   **Auth:** None
*   **Errors:**
    *   `404 Not Found`: If no event matches the provided criteria.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/deleteDataRequest` - `app/routes/deleteDataRequest.py`

*   **Purpose:** Deletes one or more data requests from the `crtdb_data_request_content` table for a specific owner.
*   **Request:**
    ```json
    {
      "requestIDs": ["string", ...], // List of data request IDs to delete
      "owner": "string"
    }
    ```
*   **Response:**
    *   Success: `{"data": {"successResponse": 1}, "message": "Deleted X requests."}`
    *   Not Found: `{"data": {"successResponse": 0}, "err_msg": "No matching records found", "err_no": 2}` (Status 404)
    *   Error: `{"data": {"successResponse": 0}, "err_msg": "string", "err_no": 3}`
*   **Flow:**
    1.  The server receives a POST request with a list of `requestIDs` and an `owner`.
    2.  It validates the request format and checks for required fields.
    3.  It connects to the SQLite database (`DB_PATH`).
    4.  It constructs a `DELETE` SQL statement for `crtdb_data_request_content`, filtering by `data_requestid` (using `IN` clause) and `owner`.
    5.  It executes the delete statement with the provided IDs and owner.
    6.  It commits the transaction.
    7.  If `cursor.rowcount` is 0, it returns a "No matching records found" error (404).
    8.  Otherwise, it returns a success message indicating the number of requests deleted.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Invalid request format or missing required fields.
    *   `404 Not Found`: If no records match the deletion criteria.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/deleteReqidDataAbs` - `app/routes/deleteReqidDataAbs.py`

*   **Purpose:** Deletes a JSON file associated with a specific request ID within a data abstraction path.
*   **Request:**
    ```json
    {
      "bemsid": "string",
      "ptt": "string", // Format: "project - tail - test"
      "reqid": "string" // The name of the JSON file (without extension)
    }
    ```
*   **Response:**
    *   Success: `{"err_no": 0, "err_msg": "success", "data": {"deleted": "reqid"}}`
    *   Error: `{"err_no": NNN, "err_msg": "failed: message"}`
*   **Flow:**
    1.  The server receives a POST request with `bemsid`, `ptt`, and `reqid`.
    2.  It validates the input parameters.
    3.  It constructs the target directory path: `${BASE_PATH}/${bemsid}/outputs/${project}/${tail}/${test}/`.
    4.  It performs path validation to ensure the target path is within the allowed `BASE_PATH`.
    5.  It checks if the target directory exists and is a directory.
    6.  It constructs the full path to the JSON file: `${target_dir}/${reqid}.json`.
    7.  It verifies that the file exists and is a file, and that it's within the expected directory structure.
    8.  If all checks pass, it deletes the JSON file using `unlink()`.
    9.  It returns a success response.
*   **Auth:** None
*   **Errors:**
    *   `1003 Invalid Input`: Missing or invalid `bemsid`, `ptt`, or `reqid`.
    *   `1001 Access Denied`: If the target path is outside the allowed `BASE_PATH`.
    *   `1004 Not Found`: If the directory or file does not exist.
    *   `1005 Not a Directory`: If the target path is not a directory.
    *   `1006 Not a File`: If the target path is not a file.
    *   `1099 Internal Error`: For other exceptions (e.g., permission errors).

### `POST` `/events` - `app/routes/events.py`

*   **Purpose:** Retrieves event information for a given Project, Tail, and Test, with optional filtering.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "owner": "string", // Optional
      "filterModel": { // Optional, for advanced filtering
        "items": [
          {
            "field": "string", // e.g., "id", "description"
            "operator": "string", // e.g., "contains", "equals"
            "value": "string"
          },
          ...
        ]
      },
      "filters": [ // Optional, simpler filter format
        {
          "field": "string",
          "operator": "string",
          "value": "string"
        },
        ...
      ]
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "id": "string",
          "date": "string",
          "begin": "string",
          "end": "string",
          "description": "string"
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, and optional filtering parameters.
    2.  It parses the `filterModel` or `filters` into a unified `filter_model` structure.
    3.  If `tail` or `test` are not provided, it attempts to parse them from the `project` string.
    4.  It connects to the SQLite database.
    5.  It constructs a base SQL query to select event information from `crtdb_event`.
    6.  It uses `apply_filter_model` from `app.services.filter_utils` to dynamically add `WHERE` clauses and `ORDER BY` based on the provided filters.
    7.  It executes the query and fetches the results.
    8.  It formats the results into the expected JSON structure.
    9.  It returns a success JSON response with the event information.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: If any exception occurs during database operations or filtering.

### `POST` `/fftdatapoints` - `app/routes/fftdatapoints.py`

*   **Purpose:** Retrieves FFT data points (frequency, average, std dev, etc.) for a specific event and datacode.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string",
      "windowType": "string", // Optional
      "maxFrequency": "number", // Optional
      "cyclicParameter": "string", // Optional
      "spectrum": "string", // Optional
      "spectrum_scaling": "string", // Optional
      "NFFT": "number", // Optional
      "compute": "string", // Optional
      "acf": "boolean", // Optional
      "ecf": "boolean", // Optional
      "owner": "string", // Optional
      "check1": "boolean", // Optional
      "check2": "boolean", // Optional
      "check3": "boolean", // Optional
      "check4": "boolean"  // Optional
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "xLabel": "string",
        "yLabel": "string",
        "axis": "string",
        "frequencyValue": [number], // Array of float values from file
        "averageValue": [number],   // Array of float values from file
        "stdDevPositiveValue": [number], // Array of float values from file
        "stdDevNegativeValue": [number], // Array of float values from file
        "peakHoldValue": [number], // Array of float values from file
        "maxFrequency": "number",
        "p": [number], // Array of float values from file
        "g": [number], // Array of float values from file
        "NFFT": "number"
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an empty `data` object if no matching record is found.
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, datacode, and eventid.
    2.  It logs the request and extracts parameters.
    3.  It validates that required parameters are present.
    4.  It connects to the SQLite database.
    5.  It queries the `crtdb_FFT` table for the specified project, tail, test, datacode, and eventid.
    6.  If a matching row is found, it retrieves file paths for frequency, average, standard deviation, and peak hold data.
    7.  It uses `read_data_from_file` to read the data from these files.
    8.  It constructs a `datapoints` dictionary with the extracted information and file data.
    9.  It returns a JSON response containing the `datapoints` and success status.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations or file reading.

### `POST` `/fftmaxfrequency` - `app/routes/fftmaxfrequency.py`

*   **Purpose:** Retrieves the maximum frequency for a given event and datacode from the `crtdb_FFT` table.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string",
      "owner": "string" // Optional
    }
    ```
*   **Response:**
    *   Success: `{"data": number, "err_msg": "Success", "err_no": 0}`
    *   No Data: `{"data": null, "err_msg": "No data found", "err_no": 0}`
    *   Error: `{"data": null, "err_msg": "string", "err_no": 1}`
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, datacode, and eventid.
    2.  It logs the request and extracts parameters.
    3.  It validates that required parameters are present.
    4.  It connects to the SQLite database.
    5.  It queries the `crtdb_FFT` table for the `Maxfrequency` corresponding to the provided project, tail, test, datacode, and eventid.
    6.  If a row is found, it returns the `Maxfrequency` value in a success response.
    7.  If no row is found, it returns `null` for data in a success response.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations.

### `POST` `/importxml` - `app/routes/importXml.py`

*   **Purpose:** Imports event and datacode information from an XML structure provided in a JSON list.
*   **Request:** A JSON list, where each item represents an XML document:
    ```json
    [
      {
        "FileId": "string",
        "Document": {
          "Export": {
            "Project": "string",
            "Aircraft": "string", // Corresponds to 'tail'
            "Test": "string",
            "Events": "string", // Comma-separated event IDs
            "Datacodes": "string" // Comma-separated datacode names
          }
        }
      },
      ...
    ]
    ```
*   **Response:**
    ```json
    {
      "status": "success",
      "message": "xml imported successfully",
      "data": {
        "file_id_1": {
          "status": "success" | "partial success" | "failed",
          "events": [{}], // Found events
          "datacodes": [{}], // Found datacodes
          "failed_records": {
            "events": ["string", ...], // Missing event IDs
            "datacodes": ["string", ...], // Missing datacode names
            "reason": "string" // Reason for failure
          }
        },
        ...
      }
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with a JSON list of XML data structures.
    2.  It iterates through each item in the list.
    3.  For each item, it extracts `FileId` and the `Export` details (`Project`, `Aircraft`, `Test`, `Events`, `Datacodes`).
    4.  It validates that required fields are present and not empty.
    5.  It splits the `Events` and `Datacodes` strings into lists.
    6.  It connects to the SQLite database.
    7.  It checks if a record exists in `crtdb_data_request_content` for the given `Project`, `Test`, and `Tail` (Aircraft). If not, it marks the import as failed for this file.
    8.  It queries `crtdb_event` for the provided event IDs and `crtdb_data` for the provided datacode names, filtering by Project, Tail, and Test.
    9.  It identifies missing events and datacodes.
    10. It determines the status ("success", "partial success", or "failed") based on whether all, some, or none of the requested events/datacodes were found.
    11. It populates the `response_data` dictionary with the results for each `FileId`.
    12. It returns a final JSON response summarizing the import status.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If the input is not a list or if required fields are missing/empty.

### `POST` `/listPTTDataAbs` - `app/routes/listPTTDataAbs.py`

*   **Purpose:** Lists Project-Tail-Test (PTT) directory structures under a user's `outputs` directory for data abstraction.
*   **Request:**
    ```json
    {
      "bemsid": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "err_no": 0,
      "err_msg": "success",
      "data": [
        "string (e.g., 'Project - Tail - Test')",
        ...
      ]
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with a `bemsid`.
    2.  It validates the `bemsid`.
    3.  It constructs the path to the user's `outputs` directory: `${BASE_PATH}/${bemsid}/outputs/`.
    4.  It performs path validation to ensure the path is within `BASE_PATH`.
    5.  It checks if the `outputs` directory exists and is a directory.
    6.  It iterates through the `outputs` directory, looking for three levels of subdirectories (Project, Tail, Test).
    7.  For each valid PTT structure found, it creates a formatted string "Project - Tail - Test".
    8.  It returns a success JSON response with the list of PTT strings.
*   **Auth:** None
*   **Errors:**
    *   `1003 Invalid Input`: Missing or invalid `bemsid`.
    *   `1001 Access Denied`: If the target path is outside the allowed `BASE_PATH`.
    *   `1004 Not Found`: If the `outputs` directory does not exist or is not a directory.
    *   `1002 Read Dir`: For errors during directory traversal.

### `POST` `/listReqidsDataAbs` - `app/routes/listReqidsDataAbs.py`

*   **Purpose:** Lists request IDs (filenames without extension) within a specific PTT directory for data abstraction.
*   **Request:**
    ```json
    {
      "bemsid": "string",
      "ptt": "string" // Format: "project - tail - test"
    }
    ```
*   **Response:**
    ```json
    {
      "err_no": 0,
      "err_msg": "success",
      "data": [
        "string (request ID, e.g., filename stem)",
        ...
      ]
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with `bemsid` and `ptt`.
    2.  It validates the input parameters.
    3.  It parses the `ptt` string into `project`, `tail`, and `test`.
    4.  It constructs the target directory path: `${BASE_PATH}/${bemsid}/outputs/${project}/${tail}/${test}/`.
    5.  It performs path validation to ensure the target path is within `BASE_PATH`.
    6.  It checks if the target directory exists and is a directory.
    7.  If the directory is valid, it lists all files within it and extracts their names without extensions (stems).
    8.  It returns a success JSON response with the list of request IDs.
*   **Auth:** None
*   **Errors:**
    *   `1003 Invalid Input`: Missing or invalid `bemsid` or `ptt`.
    *   `1001 Access Denied`: If the target path is outside the allowed `BASE_PATH`.
    *   `1004 Not Found`: If the directory does not exist.
    *   `1099 Internal Error`: For other exceptions during directory listing.

### `POST` `/login` - `app/routes/login.py`

*   **Purpose:** Handles user login, validates credentials against `crtdb_user` table, and generates a JWT.
*   **Request:**
    ```json
    {
      "bemsid": "string",
      "username": "string",
      "email": "string", // Optional
      "role": "string"   // Optional
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "token": "string", // JWT token
        "bemsid": "string",
        "username": "string",
        "role": "string"
      },
      "status": "success"
    }
    ```
    Or an error response.
*   **Flow:**
    1.  The server receives a POST request with login credentials (`bemsid`, `username`, etc.).
    2.  It connects to the SQLite database.
    3.  It checks if the `crtdb_user` table exists.
    4.  It queries the `crtdb_user` table for a user matching the provided `bemsid`.
    5.  **If user exists:**
        *   It retrieves the user's `name` and `role`.
        *   It generates a JWT token using `generate_service_jwt`.
        *   It returns a success response with the token and user details.
    6.  **If user does not exist:**
        *   It inserts the new user into the `crtdb_user` table.
        *   It commits the transaction.
        *   It generates a JWT token.
        *   It returns a success response with the token and user details, indicating user creation.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: If the `crtdb_user` table is not found.
    *   `401 Unauthorized`: If credentials are invalid (though this implementation primarily creates new users if not found).
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/modifiedEvents` - `app/routes/modifiedEvents.py`

*   **Purpose:** Retrieves modified events for a specific project, tail, test, and user.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "user": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "id": "string",
          "description": "string",
          "date": "string",
          "begin": "string",
          "end": "string",
          "project": "string",
          "tail": "string",
          "test": "string",
          "user": "string"
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, and user details.
    2.  It logs the request.
    3.  It connects to the SQLite database.
    4.  It executes a SQL query to select modified events from `crtdb_modified_events` matching the provided project, tail, test, and user.
    5.  It fetches all matching rows and their column names.
    6.  It formats the results into a list of dictionaries.
    7.  It returns a success JSON response with the list of modified events.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/modifyDataRequest` - `app/routes/modifyDataRequest.py`

*   **Purpose:** Modifies an existing data request in the `crtdb_data_request_content` table.
*   **Request:**
    ```json
    {
      "dataRequestID": "string",
      "dataRequestMade": "string", // Timestamp or identifier
      "datacodes": [{}], // Array of datacode objects
      "events": [{}],    // Array of event objects
      "owner": "string",
      "req_type": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "dataRequestMade": "string",
        "datacodes": [{}],
        "events": [{}],
        "owner": "string",
        "req_type": "string"
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an error response.
*   **Flow:**
    1.  The server receives a POST request with data request modification details.
    2.  It validates the request format and checks for required fields (`dataRequestID`, `owner`).
    3.  It connects to the SQLite database (`DB_PATH`).
    4.  It constructs an `UPDATE` SQL statement for `crtdb_data_request_content`, setting `dataRequestMade`, `datacodes`, `events`, and `req_type` for the specified `dataRequestID` and `owner`.
    5.  It executes the update statement, converting JSON fields to strings.
    6.  It commits the transaction.
    7.  It returns a success JSON response with the modified request details.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Invalid request format or missing required fields.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `GET` `/ping` - `app/routes/ping.py`

*   **Purpose:** A simple endpoint to test if the Python Flask service is running and accessible.
*   **Request:** None
*   **Response:**
    ```json
    {
      "status": "success",
      "message": "pong"
    }
    ```
*   **Flow:**
    1.  The server receives a GET request to `/ping`.
    2.  It immediately returns a JSON response with status "success" and message "pong".
*   **Auth:** None
*   **Errors:** None

### `POST` `/readJsonDataAbs` - `app/routes/readJsonDataAbs.py`

*   **Purpose:** Reads a JSON file from a specific data abstraction path.
*   **Request:**
    ```json
    {
      "bemsid": "string",
      "ptt": "string", // Format: "project - tail - test"
      "req_id": "string" // The name of the JSON file (without extension)
    }
    ```
*   **Response:**
    ```json
    {
      "err_no": 0,
      "err_msg": "success",
      "data": {
        // Content of the JSON file
      }
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with `bemsid`, `ptt`, and `req_id`.
    2.  It validates the input parameters.
    3.  It parses the `ptt` string into `project`, `tail`, and `test`.
    4.  It constructs the target directory path: `${BASE_PATH}/${bemsid}/outputs/${project}/${tail}/${test}/`.
    5.  It performs path validation to ensure the target path is within `BASE_PATH`.
    6.  It checks if the target directory exists and is a directory.
    7.  It constructs the full path to the JSON file: `${target_dir}/${req_id}.json`.
    8.  It verifies that the file exists and is a file, and that it's within the expected directory structure.
    9.  If the file is valid, it reads its content, parses it as JSON, and returns it in a success response.
*   **Auth:** None
*   **Errors:**
    *   `1003 Invalid Input`: Missing or invalid `bemsid`, `ptt`, or `req_id`.
    *   `1001 Access Denied`: If the target path is outside the allowed `BASE_PATH`.
    *   `1004 Not Found`: If the directory or file does not exist.
    *   `1005 Not a Directory`: If the target path is not a directory.
    *   `1006 Not a File`: If the target path is not a file.
    *   `1099 Internal Error`: For errors during file reading or JSON parsing.

### `POST` `/revertChanges` - `app/routes/revertChanges.py`

*   **Purpose:** Reverts modified data for a specific event and datacode back to its baseline state.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string"
    }
    ```
*   **Response:**
    *   Success: `{"data": {"successResponse": 0}, "err_msg": "Success", "err_no": 0}`
    *   Error: `{"data": {"successResponse": 1}, "err_msg": "string", "err_no": 1}`
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, datacode, and eventid.
    2.  It validates that all required parameters are present.
    3.  It connects to the SQLite database.
    4.  It executes a `DELETE` SQL statement on `crtdb_modified_data` to remove entries matching the provided project, tail, test, eventid, and datacode.
    5.  It commits the transaction.
    6.  It returns a success response.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/saveDataRequest` - `app/routes/saveDataRequest.py`

*   **Purpose:** Saves or updates a data request in the `crtdb_data_request_content` table.
*   **Request:**
    ```json
    {
      "dataRequestID": "string",
      "dataRequestMade": "string", // Timestamp or identifier
      "datacodes": [{}], // Array of datacode objects
      "description": "string",
      "events": [{}],    // Array of event objects
      "owner": "string",
      "ownerID": "string",
      "project": "string",
      "tail": "string",
      "test": "string",
      "req_type": "string",
      "parameters": {} // Object of parameters
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "dataRequestMade": "string",
        "datacodes": [{}],
        "description": "string",
        "events": [{}],
        "owner": "string",
        "ownerID": "string",
        "project": "string",
        "tail": "string",
        "test": "string",
        "req_type": "string",
        "parameters": {}
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an error response.
*   **Flow:**
    1.  The server receives a POST request with data request details.
    2.  It validates the request format and checks for required fields (`dataRequestID`, `owner`, `project`, `tail`, `test`, `ownerID`).
    3.  It connects to the SQLite database (`DB_PATH`).
    4.  It checks if a data request with the given `dataRequestID` already exists.
    5.  **If it exists:** It constructs an `UPDATE` SQL statement to modify the existing record.
    6.  **If it does not exist:** It constructs an `INSERT` SQL statement to create a new record.
    7.  It executes the appropriate SQL statement, converting JSON fields (`datacodes`, `events`, `parameters`) to strings.
    8.  It commits the transaction.
    9.  It returns a success JSON response with the saved/updated request details.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Invalid request format or missing required fields.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/saveModifiedData` - `app/routes/saveModifiedData.py`

*   **Purpose:** Saves modified data for a specific event and datacode, or reverts to baseline if `algo_type` is "BASELINE".
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string",
      "modified_data": [number], // Array of modified data values
      "algo_type": "string",     // e.g., "add", "multiply", "BASELINE"
      "parameters": {}           // Algorithm parameters
    }
    ```
*   **Response:**
    *   Success: `{"data": {"successResponse": 0}, "err_msg": "Success", "err_no": 0}`
    *   Error: `{"data": {"successResponse": 1}, "err_msg": "string", "err_no": 1}`
*   **Flow:**
    1.  The server receives a POST request with modified data details.
    2.  It validates that required parameters (`project`, `tail`, `test`, `datacode`, `eventid`, `modified_data`, `algo_type`) are present.
    3.  It connects to the SQLite database.
    4.  It checks if a record already exists in `crtdb_modified_data` for the given project, tail, test, eventid, and datacode.
    5.  **If `algo_type` is "BASELINE":**
        *   It deletes any existing record for this combination.
    6.  **Otherwise:**
        *   If a record exists, it updates the existing record with the new `modified_data`, `algo_type`, and `parameters`.
        *   If no record exists, it inserts a new record.
    7.  It commits the transaction.
    8.  It returns a success response.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/saveModifiedEvents` - `app/routes/saveModifiedEvents.py`

*   **Purpose:** Saves or updates modified events in the `crtdb_modified_events` table.
*   **Request:**
    ```json
    [
      {
        "id": "string", // Event ID
        "description": "string",
        "date": "string",
        "begin": "string",
        "end": "string"
      },
      ...
    ]
    ```
    (The request body is expected to be a list of event objects).
*   **Response:**
    *   Success: `{"data": {"successResponse": 0}, "err_msg": "Success", "err_no": 0}`
    *   Error: `{"data": {"successResponse": 1}, "err_msg": "string", "err_no": 1}`
*   **Flow:**
    1.  The server receives a POST request with a list of modified event objects.
    2.  It extracts `project`, `tail`, `test`, and `user` from the request JSON body (implicitly, as these are likely part of the context or passed via other means not shown in the snippet). **Note:** The provided snippet for `saveModifiedEvents.py` is truncated, so the exact extraction of `project`, `tail`, `test`, and `user` is assumed.
    3.  It connects to the SQLite database.
    4.  It iterates through the list of modified events.
    5.  For each event, it constructs an `INSERT OR REPLACE` SQL statement to save or update the event in the `crtdb_modified_events` table. The `id`, `project`, `tail`, `test`, `user`, `description`, `date`, `begin`, and `end` fields are used.
    6.  It executes the statement for each event.
    7.  It commits the transaction.
    8.  It returns a success response.
*   **Auth:** None
*   **Errors:**
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/shareDataRequest` - `app/routes/shareDataRequest.py`

*   **Purpose:** Shares a data request with another user.
*   **Request:**
    ```json
    {
      "owner": "string",
      "dataRequestID": "string",
      "sharedTo": "string", // The user to share with
      "req_type": "string"
    }
    ```
*   **Response:**
    *   Success: `{"data": {"successResponse": 1}, "message": "Data request shared successfully."}`
    *   Error: `{"data": {"successResponse": 0}, "err_msg": "string", "err_no": N}`
*   **Flow:**
    1.  The server receives a POST request with sharing details (`owner`, `dataRequestID`, `sharedTo`, `req_type`).
    2.  It validates the request and checks for required fields.
    3.  It connects to the SQLite database (`DB_PATH`).
    4.  It constructs an `INSERT` SQL statement to add an entry into a sharing table (likely `crtdb_data_request_sharing` or similar, though the table name is not explicitly shown in the snippet). The statement would record the `dataRequestID`, `owner`, `sharedTo`, and `req_type`.
    5.  It executes the insert statement.
    6.  It commits the transaction.
    7.  It returns a success response.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Invalid request format or missing required fields.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/sharedDataRequests` - `app/routes/sharedDataRequests.py`

*   **Purpose:** Retrieves data requests that have been shared with the current user.
*   **Request:**
    ```json
    {
      "dataRequestMade": integer,
      "owner": "string", // The user requesting to see shared data
      "project": "string",
      "tail": "string",
      "test": "string",
      "req_type": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "content": "default",
          "dataRequestID": "string",
          "dataRequestMade": integer,
          "datacodes": [{}],
          "description": "string",
          "events": [{}],
          "owner": "string", // Original owner of the shared request
          "ownerID": "string",
          "project": "string",
          "tail": "string",
          "test": "string"
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with criteria to find shared data requests.
    2.  It validates the request format.
    3.  It connects to the SQLite database (`DB_PATH`).
    4.  It constructs a SQL query to join `crtdb_data_request_content` with a sharing table (e.g., `crtdb_data_request_sharing`) to find requests where the `sharedTo` field matches the `owner` provided in the request.
    5.  It filters the results based on `dataRequestMade`, `project`, `tail`, `test`, and `req_type`.
    6.  It executes the query and fetches the results.
    7.  It parses JSON fields (`datacodes`, `events`).
    8.  It formats the results into a list of data request objects.
    9.  It returns a success JSON response with the list of shared data requests.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Invalid request format.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/spectrumScalingValues` - `app/routes/spectrumScalingValues.py`

*   **Purpose:** Retrieves spectrum scaling values for a given event and datacode.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "datacode": "string",
      "eventid": "string",
      "owner": "string" // Optional
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "spectrum_scaling": "string" // The spectrum scaling value
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an empty `data` object if no matching record is found.
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, datacode, and eventid.
    2.  It logs the request and extracts parameters.
    3.  It validates that required parameters are present.
    4.  It connects to the SQLite database.
    5.  It queries the `crtdb_FFT` table for the `spectrum_scaling` value corresponding to the provided project, tail, test, datacode, and eventid.
    6.  If a row is found, it returns the `spectrum_scaling` value in a success response.
    7.  If no row is found, it returns an empty `data` object.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations.

### `POST` `/statsExportWorkflow` - `app/routes/statsExportWorkflow.py`

*   **Purpose:** Manages statistics export workflows.
*   **Request:**
    ```json
    {
      "dataRequestID": "string",
      "owner": "string",
      "ownerID": "string",
      "project": "string",
      "tail": "string",
      "test": "string",
      "req_type": "string",
      "parameters": {} // Workflow specific parameters
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "dataRequestID": "string",
        "owner": "string",
        "ownerID": "string",
        "project": "string",
        "tail": "string",
        "test": "string",
        "req_type": "string",
        "parameters": {}
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an error response.
*   **Flow:**
    1.  The server receives a POST request with statistics export workflow details.
    2.  It validates the request and checks for required fields (`dataRequestID`, `owner`, `ownerID`, `project`, `tail`, `test`, `req_type`).
    3.  It constructs a `workflow_input` dictionary.
    4.  It calls `generate_stats_export_workflow` from `app.services.argo.statexport_workflow` to generate the workflow.
    5.  If workflow generation is successful, it inserts the request details into `crtdb_data_request_content`.
    6.  It returns a success response with the saved request details.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: Invalid request format or missing required fields.
    *   `500 Internal Server Error`: For database errors, JSON parsing errors, or workflow generation failures.

### `POST` `/testStartEndTime` - `app/routes/testStartEndTime.py`

*   **Purpose:** Retrieves start and end times for a given project, tail, and test.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "owner": "string" // Optional
    }
    ```
*   **Response:**
    ```json
    {
      "data": {
        "start_time": "string", // ISO format timestamp
        "end_time": "string"    // ISO format timestamp
      },
      "err_msg": "Success",
      "err_no": 0
    }
    ```
    Or an empty `data` object if no matching record is found.
*   **Flow:**
    1.  The server receives a POST request with project, tail, and test.
    2.  It logs the request and extracts parameters.
    3.  It validates that required parameters are present.
    4.  It connects to the SQLite database.
    5.  It queries the `crtdb_test` table for the `start_time` and `end_time` corresponding to the provided project, tail, and test.
    6.  If a row is found, it returns the `start_time` and `end_time` in a success response.
    7.  If no row is found, it returns an empty `data` object.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: If any exception occurs during database operations.

### `POST` `/uploadUserEvents` - `app/routes/uploadUserEvents.py`

*   **Purpose:** Uploads user-defined events for a specific project, tail, and test.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "owner": "string",
      "userEventsTitle": "string",
      "userEvents": [ // Array of event objects
        {
          "id": "string",
          "description": "string",
          "date": "string",
          "begin": "string",
          "end": "string"
        },
        ...
      ]
    }
    ```
*   **Response:**
    *   Success: `{"data": {"successResponse": 0}, "err_msg": "Success", "err_no": 0}`
    *   Error: `{"data": {"successResponse": 1}, "err_msg": "string", "err_no": 1}`
*   **Flow:**
    1.  The server receives a POST request with user event data.
    2.  It validates that required fields (`project`, `tail`, `test`, `owner`, `userEventsTitle`, `userEvents`) are present.
    3.  It connects to the SQLite database.
    4.  It iterates through the `userEvents` array.
    5.  For each event, it constructs an `INSERT OR REPLACE` SQL statement to save the event into `crtdb_modified_events`, associating it with the project, tail, test, owner, and title.
    6.  It executes the insert statement for each event.
    7.  It commits the transaction.
    8.  It returns a success response.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `POST` `/userEvents` - `app/routes/userEvents.py`

*   **Purpose:** Retrieves user-defined events for a specific project, tail, and test.
*   **Request:**
    ```json
    {
      "project": "string",
      "tail": "string",
      "test": "string",
      "user": "string" // The user whose events to retrieve
    }
    ```
*   **Response:**
    ```json
    {
      "data": [
        {
          "id": "string",
          "description": "string",
          "date": "string",
          "begin": "string",
          "end": "string",
          "project": "string",
          "tail": "string",
          "test": "string",
          "user": "string"
        },
        ...
      ],
      "err_msg": "Success",
      "err_no": 0
    }
    ```
*   **Flow:**
    1.  The server receives a POST request with project, tail, test, and user details.
    2.  It validates that required parameters are present.
    3.  It connects to the SQLite database.
    4.  It executes a SQL query to select user events from `crtdb_modified_events` matching the provided project, tail, test, and user.
    5.  It fetches all matching rows and their column names.
    6.  It formats the results into a list of dictionaries.
    7.  It returns a success JSON response with the list of user events.
*   **Auth:** None
*   **Errors:**
    *   `400 Bad Request`: If required parameters are missing.
    *   `500 Internal Server Error`: For database errors or other exceptions.

### `GET` `/ping` - `tests/test_app.py` (This is a test file, not an API endpoint)

*   **Purpose:** (Test) Simulates a GET request to the `/ping` endpoint to verify its functionality.
*   **Request:** Simulated GET request.
*   **Response:** Asserts that the response status code is 200 and the JSON body is `{"status": "success", "message": "pong"}`.
*   **Flow:** (Within test context)
    1.  The `client` fixture (provided by pytest) simulates a GET request to `/ping`.
    2.  Assertions check the `status_code` and `json` content of the response.
*   **Auth:** N/A (Test context)
*   **Errors:** N/A (Test context)

### `POST` `/login` - `tests/test_app.py` (This is a test file, not an API endpoint)

*   **Purpose:** (Test) Simulates a POST request to the `/login` endpoint with sample data to verify token generation.
*   **Request:** Simulated POST request with JSON body `{"bemsid": "123", "client": "testclient"}`.
*   **Response:** Asserts that the response status code is 200 and that the JSON response contains a `token` key.
*   **Flow:** (Within test context)
    1.  The `client` fixture simulates a POST request to `/login` with JSON data.
    2.  Assertions check the `status_code` and the presence of a `token` in the `response.json`.
*   **Auth:** N/A (Test context)
*   **Errors:** N/A (Test context)

## 4. Services

### `app/services/auth.py`

*   **What it does:** Provides authentication-related utilities, specifically JWT generation.
*   **Functions:**
    *   `generate_service_jwt(bemsid, username)`: Generates a JWT token for a user. It encodes the `bemsid` and `username` into the token, signs it with `JWT_SECRET_KEY`, and sets the audience to `JAVA_SERVER_IP`.
*   **Connects to:** `os` (for environment variables), `jwt` (for token encoding), `datetime` (for token expiration).

### `app/services/db.py`

*   **What it does:** Manages database connections, primarily for SQLite.
*   **Functions:**
    *   `get_db()`: Returns a connection to the SQLite database specified by `DB_PATH`. It ensures that the database file exists and creates it if necessary.
*   **Connects to:** `sqlite3` (for database operations), `os` (for environment variables), `pathlib.Path` (for path manipulation).

### `app/services/file_manager.py`

*   **What it does:** Provides utility functions for file operations.
*   **Functions:** (Specific functions are not detailed in the provided snippets, but would likely include operations like reading, writing, deleting files, and managing directories.)
*   **Connects to:** `os`, `pathlib`.

### `app/services/filter_utils.py`

*   **What it does:** Provides utility functions for dynamically building SQL `WHERE` clauses based on filter models.
*   **Functions:**
    *   `apply_filter_model(query, params, filter_model, column_map)`: Takes a base SQL query, parameters, a filter model (containing filter items), and a column map. It constructs the `WHERE` clause based on the filter items and appends them to the query and parameters. It supports various operators like "contains", "equals", etc.
*   **Connects to:** None directly, operates on input data.

### `app/services/mssql.py`

*   **What it does:** Manages connections to an MSSQL database.
*   **Functions:**
    *   `get_mssql_db()`: Establishes and returns a connection to the MSSQL database. (Details of connection string/credentials are not provided in the snippet but would typically come from environment variables or a config file).
*   **Connects to:** `pyodbc` or similar MSSQL driver.

### `app/services/request_handler.py`

*   **What it does:** Likely contains generic logic for handling incoming requests, possibly for parsing, validation, or error handling. (Specific functions are not detailed in the provided snippets).
*   **Connects to:** Flask's `request` object.

### `app/services/argo/common.py`

*   **What it does:** Provides common utilities for interacting with Argo workflows.
*   **Functions:**
    *   `load_config_for_block(block_name)`: Loads configuration specific to an Argo workflow block from `config.yaml`.
    *   `build_path(*args)`: Constructs a file path by joining path segments.
    *   `get_base_path()`: Retrieves the base path for Argo workflow artifacts.
*   **Connects to:** `os`, `pathlib`, `yaml`.

### `app/services/argo/customexport_workflow.py`

*   **What it does:** Generates Argo workflows for custom data exports.
*   **Functions:**
    *   `generate_custom_export_workflow(workflow_input, req_type, parameters)`: Orchestrates the creation of a custom export Argo workflow based on the provided input parameters. It likely uses templates and populates them with specific data.
*   **Connects to:** `app.services.argo.common`, `app.services.argo.generate_yaml`, `os`, `pathlib`, `json`.

### `app/services/argo/dataexport_workflow.py`

*   **What it does:** Generates Argo workflows for data exports (specifically FTList workflows).
*   **Functions:**
    *   `generate_ftlist_workflow(workflow_input, req_type, parameters)`: Creates an Argo workflow for FTList data exports. It likely uses templates and populates them with export parameters.
*   **Connects to:** `app.services.argo.common`, `app.services.argo.generate_yaml`, `os`, `pathlib`, `json`.

### `app/services/argo/generate_yaml.py`

*   **What it does:** Handles the generation of YAML files, likely for Argo workflow definitions.
*   **Functions:** (Specific functions are not detailed in the provided snippets, but would involve templating and writing YAML content.)
*   **Connects to:** `yaml`, `os`, `pathlib`.

### `app/services/argo/rainflowexport_workflow.py`

*   **What it does:** Generates Argo workflows for Rainflow analysis exports.
*   **Functions:** (Specific functions are not detailed in the provided snippets, but would involve creating Rainflow export workflows.)
*   **Connects to:** `app.services.argo.common`, `app.services.argo.generate_yaml`.

### `app/services/argo/statexport_workflow.py`

*   **What it does:** Generates Argo workflows for state exports (e.g., statistics exports).
*   **Functions:**
    *   `generate_stats_export_workflow(...)`: Creates an Argo workflow for statistics exports.
*   **Connects to:** `app.services.argo.common`, `app.services.argo.generate_yaml`.

### `app/services/argo/workflow.py`

*   **What it does:** Contains general logic for Argo workflow management.
*   **Functions:** (Specific functions are not detailed in the provided snippets, but could include submitting workflows, checking status, etc.)
*   **Connects to:** Argo API or CLI.

### `app/services/dll/cache.py`

*   **What it does:** Implements caching mechanisms, likely for DLL function calls to improve performance.
*   **Functions:** (Specific functions are not detailed, but would involve cache storage, retrieval, and invalidation.)
*   **Connects to:** In-memory data structures or external caching systems.

### `app/services/dll/datacodes_dll_interface.py`

*   **What it does:** Provides an interface to interact with a DLL that handles datacode-related operations.
*   **Functions:** (e.g., `read_insts_info` is mentioned in a comment but not defined, suggesting functions to call DLLs.)
*   **Connects to:** A native DLL.

### `app/services/dll/datapoints_dll_interface.py`

*   **What it does:** Provides an interface to interact with a DLL for datapoint operations.
*   **Functions:** (Specific functions are not detailed.)
*   **Connects to:** A native DLL.

### `app/services/dll/events_dll_interface.py`

*   **What it does:** Provides an interface to interact with a DLL for event-related operations.
*   **Functions:**
    *   `read_flight_data`: (Commented out) Likely a function to read flight data via a DLL.
*   **Connects to:** A native DLL.

### `app/services/dll/ptt_dll_interface.py`

*   **What it does:** Provides an interface to interact with a DLL for Project-Tail-Test (PTT) related operations.
*   **Functions:** (Specific functions are not detailed.)
*   **Connects to:** A native DLL.

### `app/services/dll/start_end_times_interface.py`

*   **What it does:** Provides an interface to interact with a DLL for retrieving start and end times.
*   **Functions:** (Specific functions are not detailed.)
*   **Connects to:** A native DLL.

## 5. Database & External Connections

### Databases Used

*   **SQLite:** Used extensively for storing application data, including user information (`crtdb_user`), data requests (`crtdb_data_request_content`), events (`crtdb_event`, `crtdb_modified_events`), datacodes (`crtdb_data`), sine data (`crtdb_sin`), FFT data (`crtdb_FFT`), statistics (`crtdb_statistics`), and modified data (`crtdb_modified_data`). The database file path is configurable via the `DB_PATH` environment variable.
*   **MSSQL:** Used for `argo_workflow_requests` table, as indicated by `app.services.mssql.get_mssql_db()`. This suggests that workflow tracking or metadata might be stored in a separate MSSQL database.

### Connection Management

*   **SQLite:** Managed by `app/services/db.py`'s `get_db()` function, which returns a `sqlite3.Connection` object. Connections are typically opened and closed within the scope of a request handler or explicitly managed.
*   **MSSQL:** Managed by `app/services/mssql.py`'s `get_mssql_db()` function.

### External Services Called

*   **Argo Workflows:** The application interacts with Argo Workflows to manage and execute data processing pipelines. Services in `app/services/argo/` are responsible for generating workflow definitions (YAML) and potentially submitting them.
*   **Native DLLs:** The `app/services/dll/` directory indicates interactions with native Dynamic Link Libraries for specific functionalities like datacode lookups, event data reading, and PTT operations.
*   **Spring Boot Backend:** The Node.js proxy (`app/server.js`) forwards requests to a Spring Boot application running on `https://localhost:8443`. This backend likely handles core business logic and data access.
*   **Python Flask Backend:** The Node.js proxy also forwards requests to a Python Flask application running on `http://localhost:8444`, specifically for paths containing `/boeing/crtdb/`. This Flask application appears to be the primary backend for many of the API routes documented here.
*   **JWT Authentication:** The `checkAuth.py` route and `app/services/auth.py` service indicate the use of JWT for securing API endpoints, with tokens validated against a secret key and audience.

---

*AI-generated documentation — 2026-06-22 15:34:56*
*Review for accuracy. AI may misinterpret complex logic.*
