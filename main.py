from fastapi import FastAPI, HTTPException
import uvicorn


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/add/{num1}/{num2}/{num3}")
async def add(num1: float, num2: float, num3: float):
    result = num1 + num2 + num3
    return {"result": result}


@app.get("/sub")
async def sub(num1: float, num2: float):
    result = num1 - num2
    return {"result": result}


@app.get("/mul/{num1}")
async def mult(num1: float, num2: float):
    result = num1 * num2
    return {"result": result}


@app.get("/div/{num1}/{num2}")
async def div(num1: float, num2: float):
    try:
        result = num1 / num2
        return {"result": result}
    except:
        raise HTTPException(status_code=404, detail='Division by zero')


@app.get("/{a}/{b}/{c}")
async def equation(a: int, b: int, c: int):
    d = b ** 2 - 4 * a * c
    if d >= 0:
        d_sqrt = d ** 0.5
        x1 = (-b - d_sqrt)/(2 * a)
        x2 = (-b + d_sqrt)/(2 * a)
        result = {"x1": x1, "x2": x2}
        return {"result": result}
    else:
        return {"error": "d < 0"}


@app.get("/dynamic/{nums}")
async def add_dynamic(nums: str):
    numbers = [float(k) for k in nums.split(',')]

    return {'result': {'numbers': numbers, 'sum': sum(numbers)}}


if __name__ == "__main__":
    uvicorn.run(app)
