from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "temporary_secret_key"


# -------------------------
# Database helper functions
# -------------------------

def get_db_connection():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            cash REAL NOT NULL DEFAULT 10000
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            price REAL NOT NULL,
            type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# -------------------------
# Small helper functions
# -------------------------

def usd(value):
    return f"${value:,.2f}"


app.jinja_env.filters["usd"] = usd


def lookup(symbol):
    stocks = {
        "AAPL": {
            "name": "Apple Inc.",
            "symbol": "AAPL",
            "price": 190.50
        },
        "MSFT": {
            "name": "Microsoft Corporation",
            "symbol": "MSFT",
            "price": 420.25
        },
        "TSLA": {
            "name": "Tesla Inc.",
            "symbol": "TSLA",
            "price": 175.80
        },
        "NFLX": {
            "name": "Netflix Inc.",
            "symbol": "NFLX",
            "price": 436.61
        }
    }

    symbol = symbol.upper()

    if symbol in stocks:
        return stocks[symbol]

    return None


def login_required():
    if "user_id" not in session:
        return False

    return True


# -------------------------
# Routes
# -------------------------

@app.route("/")
def index():
    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    owned_stocks = conn.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, (session["user_id"],)).fetchall()

    user = conn.execute("""
        SELECT cash
        FROM users
        WHERE id = ?
    """, (session["user_id"],)).fetchone()

    conn.close()

    portfolio = []
    total_stock_value = 0

    for stock_row in owned_stocks:
        stock = lookup(stock_row["symbol"])

        if stock is not None:
            shares = stock_row["total_shares"]
            total_value = shares * stock["price"]

            portfolio.append({
                "symbol": stock["symbol"],
                "name": stock["name"],
                "shares": shares,
                "price": stock["price"],
                "total": total_value
            })

            total_stock_value += total_value

    cash = user["cash"]
    grand_total = cash + total_stock_value

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash=cash,
        grand_total=grand_total
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return "Missing username"

        if not password:
            return "Missing password"

        if password != confirmation:
            return "Passwords do not match"

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """, (username, hashed_password))

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return "Missing username"

        if not password:
            return "Missing password"

        conn = get_db_connection()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,)).fetchone()

        conn.close()

        if user is None:
            return "Invalid username"

        if not check_password_hash(user["password"], password):
            return "Invalid password"

        session["user_id"] = user["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
def quote():
    if not login_required():
        return redirect("/login")

    quote_data = None

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return "Missing symbol"

        quote_data = lookup(symbol)

        if quote_data is None:
            return "Invalid symbol"

    return render_template("quote.html", quote=quote_data)


@app.route("/buy", methods=["GET", "POST"])
def buy():
    if not login_required():
        return redirect("/login")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return "Missing symbol"

        if not shares:
            return "Missing shares"

        if not shares.isdigit():
            return "Shares must be a whole number"

        shares = int(shares)

        if shares <= 0:
            return "Shares must be greater than 0"

        stock = lookup(symbol)

        if stock is None:
            return "Invalid stock symbol"

        total_price = shares * stock["price"]

        conn = get_db_connection()

        user = conn.execute("""
            SELECT cash
            FROM users
            WHERE id = ?
        """, (session["user_id"],)).fetchone()

        if user["cash"] < total_price:
            conn.close()
            return "Not enough cash"

        conn.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            stock["symbol"],
            shares,
            stock["price"],
            "BUY"
        ))

        conn.execute("""
            UPDATE users
            SET cash = cash - ?
            WHERE id = ?
        """, (total_price, session["user_id"]))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
def sell():
    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    owned_stocks = conn.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, (session["user_id"],)).fetchall()

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            conn.close()
            return "Missing symbol"

        if not shares:
            conn.close()
            return "Missing shares"

        if not shares.isdigit():
            conn.close()
            return "Shares must be a whole number"

        shares = int(shares)

        if shares <= 0:
            conn.close()
            return "Shares must be greater than 0"

        owned = conn.execute("""
            SELECT SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ?
            AND symbol = ?
            GROUP BY symbol
        """, (session["user_id"], symbol)).fetchone()

        if owned is None or owned["total_shares"] < shares:
            conn.close()
            return "Not enough shares"

        stock = lookup(symbol)

        if stock is None:
            conn.close()
            return "Invalid symbol"

        total_sale = shares * stock["price"]

        conn.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            symbol,
            -shares,
            stock["price"],
            "SELL"
        ))

        conn.execute("""
            UPDATE users
            SET cash = cash + ?
            WHERE id = ?
        """, (total_sale, session["user_id"]))

        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()

    return render_template("sell.html", stocks=owned_stocks)


@app.route("/history")
def history():
    if not login_required():
        return redirect("/login")

    conn = get_db_connection()

    transactions = conn.execute("""
        SELECT symbol, shares, price, type, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template("history.html", transactions=transactions)


# -------------------------
# Start app
# -------------------------

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)