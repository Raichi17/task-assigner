import csv
from ortools.sat.python import cp_model

# CSVからデータを読み込む関数
def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        days = []
        data = {}
        for i, row in enumerate(reader):
            days.append(i + 1)  # 日付は行のインデックス（1から始める）
            for j, value in enumerate(row):
                user = header[j]
                if user not in data:
                    data[user] = []
                data[user].append(value)
        return header[1:], days, data  # ユーザーリスト、日付、担当可能日情報

# 最適化問題を定義する関数
def create_schedule(users, days, availability, interval, weights):
    model = cp_model.CpModel()

    # 変数：各ユーザーが各日に担当するかどうか
    x = {}
    for i, user in enumerate(users):
        for j, day in enumerate(days):
            x[(i, j)] = model.NewBoolVar(f'x_{user}_{day}')

    # 制約1: 各日の担当は1人だけ
    for j in range(len(days)):
        model.Add(sum(x[(i, j)] for i in range(len(users))) == 1)

    # 制約2: ユーザーが✕の日には担当しない
    for i, user in enumerate(users):
        for j, day in enumerate(days):
            if availability[user][j] == '✕':
                model.Add(x[(i, j)] == 0)

    # 目的関数: ◯の日には担当、△の日には避ける、担当日を均等に配置
    total_cost = 0
    for i, user in enumerate(users):
        for j, day in enumerate(days):
            if availability[user][j] == '◯':
                total_cost += weights['prefer'] * x[(i, j)]  # ◯に割り当てる
            elif availability[user][j] == '△':
                total_cost -= weights['avoid'] * x[(i, j)]  # △を避ける

    model.Maximize(total_cost)

    # 解を求める
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 結果を取得
    schedule = {}
    print("status: ", status)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i, user in enumerate(users):
            schedule[user] = [solver.Value(x[(i, j)]) for j in range(len(days))]
    return schedule

# スケジュールをCSVに出力する関数
def output_schedule_to_csv(schedule, users, days, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['日付'] + users)
        for j, day in enumerate(days):
            row = [day] + [schedule[user][j] for user in users]
            writer.writerow(row)

# 標準出力用の関数
def print_schedule(schedule, users, days):
    print("担当スケジュール")
    print(f"{'日付':<5}", end="")
    for user in users:
        print(f"{user:<10}", end="")
    print()
    for j, day in enumerate(days):
        print(f"{day:<5}", end="")
        for user in users:
            print(f"{'◯' if schedule[user][j] == 1 else '×':<10}", end="")
        print()

# 実行例
if __name__ == "__main__":
    # 入力ファイル名とタスク実施間隔
    input_file = 'input.csv'
    output_file = 'schedule_output.csv'
    interval = 3  # 例えば、タスクは3日に1回行う
    weights = {'prefer': 10, 'avoid': 5}  # 目的関数の重み（◯を優先し、△を避ける）

    # CSVファイルからデータを読み込み
    users, days, availability = read_csv(input_file)

    # スケジュールを作成
    print(users, days, availability)
    schedule = create_schedule(users, days, availability, interval, weights)

    # 結果をCSVに出力
    output_schedule_to_csv(schedule, users, days, output_file)

    # 標準出力に結果を表示
    print_schedule(schedule, users, days)
