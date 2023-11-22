# map_prediction_by_parish
## 1. Create venv file
```python -m venv venv```


#### Linux and MacOS
```source venv/bin/activate```
#### Windows
```source venv\scripts\activate```

### Install the necessary dependencies
```python.exe -m pip install --upgrade pip```
```pip install -r requirements.txt```

### Running flask
```flask run```
```python app.py```

#

## Running the model with Docker
### Build the image
```  ```

### Run the image

```  ```

* This is a CRON job only thus it does not require any ports to be exposed.


## 
The .env file


### 1. Create a .env file


### 2. Add the API key
In the .env file the API used 
https://platform.airqo.net/api/v2/predict/search?latitude={}&longitude={}&token{}


Get the token from https://platform.airqo.net >> settings >> Register client >> Generate API key