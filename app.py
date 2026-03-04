import secrets
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
        length  = max(6,  min(int(request.args.get("length", 16)), 32))
        count   = max(1,  min(int(request.args.get("count",   1)), 1000))
    except ValueError:
        length, count = 16, 1

    # Build charset from query param, fallback to all chars
    charset_param = request.args.get("charset", "")
    pool = list(charset_param) if charset_param else all_characters

    # Always guarantee at least one char from each active set
    guaranteed = []
    if any(c in lower   for c in pool): guaranteed.append(secrets.choice([c for c in pool if c in lower]))
    if any(c in upper   for c in pool): guaranteed.append(secrets.choice([c for c in pool if c in upper]))
    if any(c in numbers for c in pool): guaranteed.append(secrets.choice([c for c in pool if c in numbers]))
    if any(c in symbols for c in pool): guaranteed.append(secrets.choice([c for c in pool if c in symbols]))

    passwords = []
    for _ in range(count):
        pwd = guaranteed[:] + [secrets.choice(pool) for _ in range(length - len(guaranteed))]
        secrets.SystemRandom().shuffle(pwd)
        passwords.append("".join(pwd))

    return {"passwords": passwords}
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)