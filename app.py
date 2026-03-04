import secrets, time
from flask import Flask, render_template, request

app = Flask(__name__)

# Character sets
lower   = list("abcdefghijklmnopqrstuvwxyz")
upper   = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numbers = list("0123456789")
symbols = list("!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
all_characters = lower + upper + numbers + symbols

@app.route("/")
def Main():
    return render_template("index.html")

@app.route("/api/batch/generate")
def batch_generate():
    try:
        length = int(request.args.get("length", 16))
        length = max(6, min(length, 32))
        count = int(request.args.get("count", 1))
        count = max(1, min(count, 1000))
    except ValueError:
        length, count = 16, 10

    passwords = []
    for _ in range(count):
        password_list = [
            secrets.choice(lower),
            secrets.choice(upper),
            secrets.choice(numbers),
            secrets.choice(symbols),
            *[secrets.choice(all_characters) for _ in range(length - 4)]
        ]
        secrets.SystemRandom().shuffle(password_list)
        passwords.append("".join(password_list))

    return {"passwords": passwords}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)