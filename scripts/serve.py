#deep learning libraries
from fastai.vision import load_learner, Path, defaults
import torch
defaults.device = torch.device('cpu')

#web frameworks
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
import uvicorn
import aiohttp
import asyncio

import os
import sys
import base64 
from PIL import Image

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

app = Starlette()
path = Path('/tmp')
learner = load_learner(path)

@app.route("/upload", methods = ["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_image_from_bytes(bytes)

@app.route("/classify-url", methods = ["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_image_from_bytes(bytes)

def predict_image_from_bytes(bytes):
    #load byte data into a stream
    img_file = io.BytesIO(bytes)
    #encoding the image in base64 to serve in HTML
    img_pil = Image.open(img_file)
    img_pil.save("img.jpg", format="JPEG")
    img_uri = base64.b64encode(open("img.jpg", 'rb').read()).decode('utf-8')
    
    #make inference on image and return an HTML response
    img = open_image(img_file)
    pred_class, pred_idx, outputs = learner.predict(img)
    formatted_outputs = ["{:.1f}%".format(value) for value in [x * 100 for x in torch.nn.functional.softmax(outputs, dim = 0)]]
    pred_probs = sorted(zip(learner.data.classes, map(str, formatted_outputs)),
                        key = lambda p: p[1],
                        reverse = True
                       )
    return HTMLResponse(
        """
        <html>
            <body>
                <p> Prediction: <b> %s </b> </p>
                <p> Confidence: <b> %s </b> </p>
            </body>
        <figure class = "figure">
            <img src="data:image/png;base64, %s" class = "figure-img">
        </figure>
        </html>
        """ %(pred_class, pred_probs, img_uri))
        
@app.route("/")
def form(request):
        return HTMLResponse(
            """
            <h1> Greenr </h1>
            <p> Is your picture of a dandelion or grass? </p>
            <form action="/upload" method = "post" enctype = "multipart/form-data">
                <u> Select picture to upload: </u> <br> <p>
                1. <input type="file" name="file"><br><p>
                2. <input type="submit" value="Upload">
            </form>
            <br>
            <br>
            <u> Submit picture URL </u>
            <form action = "/classify-url" method="get">
                1. <input type="url" name="url" size="60"><br><p>
                2. <input type="submit" value="Upload">
            </form>
            """)
        
@app.route("/form")
def redirect_to_homepage(request):
        return RedirectResponse("/")
        
if __name__ == "__main__":
    if "serve" in sys.argv:
        port = int(os.environ.get("PORT", 8008)) 
        uvicorn.run(app, host = "0.0.0.0", port = port)
