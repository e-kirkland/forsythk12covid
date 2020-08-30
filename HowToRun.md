# Installing Pre-requisites

1. Download and install python from https://www.python.org/downloads/

2. Upgrade pip - as pip shipped along with python install may be outdated.

    ```
    python -m pip install --upgrade pip
    ```

    

3. On the command prompt execute following commands in sequence

    ```
    pip install wheel
    
    pip install dash pandas plotly_express bs4 requests
    ```

    Installing wheel is not a requirement, but it may become a preferred way to manage.

# Running App

1.  Navigate to folder and execute following command

```
python app.py
```

2. App will start with output on console.  one of the line will print as below if the app is running successfully.

```
Dash is running on http://127.0.0.1:8050/
```

3. Open browser and navigate to http://127.0.0.1:8050/ 