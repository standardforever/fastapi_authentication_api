1. Install the requirements.txt -
    ```pip install -r requirements.txt```

2. Run the application using(you should be at the root of the directory(folder)) -
    ```python3 main.py```

3. Available Endpoints -

    1. Register api - POST REQUEST
        - requirements:
            - Link(endpoint) - http:127.0.0.1:8000/signup
            - Body
                * Payload Sample(example of payload to pass to the endpoint) :
                    {
                        "email": "testuser123@gmail.com",
                        "password": "12345",
                        "confirm_password": "12345"
                    }
                - email :- user email to register(it most be unique)
                - password :- user password
                - confirm_password :- confirm_password and user password most be same

            - Headers
                - Content-Type: "application/json"

            - Response body:
                {
                    "email": "testuser123@gmail.com",
                    "id": "71d55145-be26-44ad-8fd4-5e1a8837da64"
                }


    2. Login api - POST REQUSET
        - requirements:
            - Link(endpoint) - http:127.0.0.1:8000/login
            - Body
                * Payload Sample(example of payload to pass to the endpoint) :
                    {
                        "email": "testuser123@gmail.com",
                        "password": "12345"
                    }
            - eamil :- the user email that was registered
            - password :- the user password

        - Headers
            - Content-Type: "application/json"

        - Response body:
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTI5MDI0NjMsInN1YiI6InN0cmluZzEifQ.ZO0BwEd6AxUj2TQC663q13PTvux5qqdFYMJou2c8GGc"
                }


    3. logout api - GET REQUEST
        - requirements:
            - Link(endpoint) - http:127.0.0.1:8000/logout
            - body
                - None
            - headers
                - Content-Type: "application/json"
                - Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTI5MDI0NjMsInN1YiI6InN0cmluZzEifQ.ZO0BwEd6AxUj2TQC663q13PTvux5qqdFYMJou2c8GGc"

            - Response body:
                - "logout successfully"


    4. login_sessions api - GET REQUEST
        - requirements:
            - Link(endpoint) - http:127.0.0.1:8000/login_sessions
            - Body
                - None
            - Headers
                - Content-Type: "application/json"
                - Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTI5MDI0NjMsInN1YiI6InN0cmluZzEifQ.ZO0BwEd6AxUj2TQC663q13PTvux5qqdFYMJou2c8GGc"
            
            - Response body:
                [
                    {
                        "date": "2023-08-24 10:26:04.510635",
                        "user": "string",
                        "id": "fc33c523-2d76-4051-808a-38dde2c152f0"
                    },
                    {
                        "date": "2023-08-24 10:27:04.340755",
                        "user": "string",
                        "id": "79bf886e-d967-45d0-93e1-5fc82367ddad"
                    }
                ]
