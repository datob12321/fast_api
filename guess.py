from fastapi import FastAPI, Path
from random import randint
from uvicorn import run


guess_number = randint(1, 100)


app = FastAPI()
tries = 0
guessed = False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/again')
def again():
    global guess_number
    global guessed
    global tries

    guess_number = randint(1, 100)
    guessed = False
    tries = 0

    return {'message': 'Your started again!'}


@app.get("/guess/{num}")
async def guess(num: int = Path(ge=1, le=100)):
    message = {'message': 'Guess a number between 1 and 100'}

    global guessed
    global tries

    if not guessed:
        tries += 1

    if num < guess_number:
        message.update({"message": "Your number is less than mine!"})
    elif num > guess_number:
        message.update({"message": "Your number is greater than mine"})
    else:
        guessed = True
        message.update({"message": "You guessed the number, congratulations!", 'tries': tries})
    return message


if __name__ == "__main__":
    run(app)
