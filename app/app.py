from flask import Flask, render_template, request, redirect, url_for
import calendar
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    # URL パラメータで年月を取得 (デフォルトは現在の年月)
    year = request.args.get("year", type=int, default=datetime.datetime.now().year)
    month = request.args.get("month", type=int, default=datetime.datetime.now().month)

    # カレンダーの計算
    cal = calendar.Calendar()
    days = [(day if day != 0 else None) for day in cal.itermonthdays(year, month)]

    # 前月と翌月を計算
    prev_month = (month - 1) if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = (month + 1) if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template(
        "index.html",
        days=days,
        year=year,
        month=month,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month
    )

@app.route("/save", methods=["POST"])
def save():
    selected_days = request.form.getlist("days")
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))

    # CSV ファイルの生成
    data = [{"Year": year, "Month": month, "Day": day} for day in selected_days]
    file_path = "selected_days.csv"
    with open(file_path, "w") as f:
        f.write("Year,Month,Day\n")
        for row in data:
            f.write(f"{row['Year']},{row['Month']},{row['Day']}\n")

    return redirect(f"/?year={year}&month={month}")

if __name__ == "__main__":
    app.run(debug=True)

