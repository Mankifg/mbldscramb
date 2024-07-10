from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, Cookie
from typing import Optional

from fastapi import FastAPI, Request, Response, Cookie, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
import json

from pyTwistyScrambler import scrambler333

import magiccube
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def up_face(alg):
    cube = magiccube.Cube(
        3, "YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")
    
    cube.reset()
    cube.rotate("Z Z")
    cube.rotate(alg)

    c = str(cube)
    c = c[:100]
    c = c.replace(" ","")
    c = c.replace("\n","")
    return c


def scale(n):
    sq = int(n**0.5)
    rem = n - sq * (sec := n // sq)
    sq1, sec2, rem2 = sq + 1, n // (sq + 1), n - (sq + 1) * (n // (sq + 1))
    width, height, rem = (sq, sec, rem) if rem < rem2 else (sq1, sec2, rem2)
    print(f"{n}={width}x{height}+{rem}")
    
    return width, height, rem

def list_of_scrambles_to_uface(scrambles):
    ret = []
    
    for elem in scrambles:
        ret.append(up_face(elem))
    
    return ret


@app.get("/")
async def root(request: Request):
     
    
    return templates.TemplateResponse("index.html", {"request": request,})


@app.get("/scramble", response_class=HTMLResponse)
async def scramble(request: Request, s: Optional[str] = Cookie(None)):
    index = int(request.query_params.get('index', 0))  # Get index from query params, default to 0
    
    elements = json.loads(s)
    if index > len(elements) or index < 0:
        index = 0  
    el = elements[index]
    scrms = list_of_scrambles_to_uface(el)
    comb = list(zip(el, scrms,list(range(1,len(scrms)+1))))
    
    
    return templates.TemplateResponse("scramble.html", {"request": request, "comb": comb, "index": index,})

@app.post("/set_index/{new_index}", response_class=HTMLResponse)
async def set_index(request: Request, new_index: int, s: Optional[str] = Cookie(None)):
   
    index = new_index
   
    elements = json.loads(s)
    if index > len(elements) or index < 0:
        new_index = 0  
    el = elements[new_index]
    scrms = list_of_scrambles_to_uface(el)    
    comb = list(zip(el, scrms,list(range(1,len(scrms)+1))))
    

    response = templates.TemplateResponse("scramble.html", {"request": request, "comb": comb, "index": new_index,})
    response.set_cookie(key="s", value=json.dumps(elements))
    return response

@app.get("/random")
async def read_root(request: Request):
    
    scr = scrambler333.get_3BLD_scramble()
    
    return {"scr":scr}


@app.post("/save_scr/")
async def save_scr(response: Response,cubes: int = 2):
    print(cubes)
    scrambles = []
    
    width, height, reaminder = scale(cubes)
    
    for _ in range(width):
        n = []
        for _ in range(height):
            n.append(scrambler333.get_3BLD_scramble())
        scrambles.append(n)
        
    extra = []
    for _ in range(reaminder):
        extra.append(scrambler333.get_3BLD_scramble())
    scrambles.append(extra)
    
    print(scrambles)
    
    response.set_cookie(key="s", value=scrambles, httponly=True)
    



