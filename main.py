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
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


from pyTwistyScrambler import scrambler333

import magiccube

import re

import ast

pattern = "(([UuDdLlRrFfBbMESxyz]|[UDLRFB]w)[2']?)+"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def up_face(alg):
    
    print("*"*10)
    print(alg)
    
    #allowed = "UDLRFBudlrfbw2' "
    allowed = "UDLRFBw2' "
    
    for a in alg:
        if a not in allowed:
            return "BBBBBBBBB"
    
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

def the_main(s,index):
    if s:
        print(s)
        print(type(s))
        elements = ast.literal_eval(s)
        #elements = json.loads(s)
        print(elements)
    else:
        return False,"First you nead to generate scrambles.",None

    a_el = 0
    for a in s:
        a_el = a_el + len(a)
    print(a_el)

    if index >= len(elements) or index < 0:
        index = 0  
    el = elements[index]
    
    scrms = list_of_scrambles_to_uface(el)
    
    count = 0
    for i in range(index):
        count = count + len(elements[i])
    print(count)
    
    nums = list(range(count+1,201))
    comb = list(zip(el, scrms,nums))
    
    return True,comb,index


@app.get("/scramble", response_class=HTMLResponse)
async def scramble(request: Request, s: Optional[str] = Cookie(None)):
    index = int(request.query_params.get('index', 0))  # Get index from query params, default to 0

    succes,data,index = the_main(s,index)
    
    if not succes:
        response = templates.TemplateResponse("index.html", {"request": request, "error": data})
        return response
    
    
    return templates.TemplateResponse("scramble.html", {"request": request, "comb": data, "index": index})

@app.post("/set_index/{new_index}", response_class=HTMLResponse)
async def set_index(request: Request, new_index: int, s: Optional[str] = Cookie(None)):
   
    index = new_index
    
    succes,data,index = the_main(s,index)
    
    if not succes:
        response = templates.TemplateResponse("index.html", {"request": request, "error": data})
        return response
    
    return templates.TemplateResponse("scramble.html", {"request": request, "comb": data, "index": index})


@app.get("/userscrambles")
async def read_root(request: Request):
    response = templates.TemplateResponse("userScrambles.html", {"request": request})
    return response


@app.post("/userscrambleget")
async def handle_form(response:Response,input_text: str = Form(...)):

    input_text = input_text.replace("\r", "")
    input_text = input_text.replace("", "")
    
    inp = input_text.split("\n")
    
    pattern = r"^\d+[\.\)]\s*"

    # Filter the scrambles
    inp = [re.sub(pattern, "", scramble) for scramble in inp]
    
    print(inp)
    
    
    cubes = len(inp)
    
    width, height, rem = scale(cubes)
    
    scrambles = []
    i = 0
    for _ in range(width):
        n = []
        for _ in range(height):
            c = inp[i]
            i = i + 1
            n.append(c)
        scrambles.append(n)
    
    extra = []
    while i < len(inp):
        c = inp[i]
        i = i+1
        extra.append(c)
    
    if len(extra) != 0:
        scrambles.append(extra)
    
    print(scrambles)
    response.set_cookie(key="s", value=scrambles, httponly=True)


    return {"output": "Saved"}

@app.post("/save_scr")
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
    
    response.set_cookie(key="s", value=scrambles, httponly=True)
    



