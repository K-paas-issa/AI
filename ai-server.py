from fastapi import FastAPI, BackgroundTasks
import s3utils
from fastapi import status
from fastapi import Response
from learning_service import start_learning

app = FastAPI()
start_latitude = 37.9381943
start_longitude = 126.5877948

@app.get("/simulation-data")
def learning(path : str, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_learning, path) 
    return Response(status_code=status.HTTP_200_OK)