from flask import Flask, render_template, request, send_file
import calendar
import datetime
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    # 今月の情報を取得
    now = datetime.datetime.now()
    year, month = now.year, now.month
    cal = calendar.Calendar()
    days = [(day if day != 0 else None) for day in cal.itermonthdays(year, month)]
    return render_template("index.html", days=days, year=year, month=month)

@app.route("/save", methods=["POST"])
def save():
    selected_days = request.form.getlist("days")
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))

    # データをCSVに保存
    data = [{"Year": year, "Month": month, "Day": day} for day in selected_days]
    df = pd.DataFrame(data)
    file_path = "selected_days.csv"
    df.to_csv(file_path, index=False)

    return send_file(file_path, as_attachment=True, download_name="selected_days.csv")

if __name__ == "__main__":
    app.run(debug=True)
