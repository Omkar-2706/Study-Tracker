import csv
from datetime import date

DATE_FILE = "daily_summary.csv"
SES_FILE="sessions.csv"
SUB_FILE="subjects.csv"
def get_ses():
    with open(SES_FILE, "r", newline="") as f:
        rows = list(csv.reader(f))
        ses_data = []
        for row in rows[1:]:
            dict = {
                "date": row[0],
                "subjects": row[2],
                "seconds": int(row[3]),
                "points": int(row[4])}
            ses_data.append(dict)
        return ses_data


def get_daily_total():
    with open(DATE_FILE, "r", newline="") as f:
        rows = list(csv.reader(f))
        daily_data =[]
        for row in rows[1:]:
            dict = {
                "date": row[0],
                "time": row[1],
                "points_done": int(row[2]),
                "points_target": int(row[3])}
            daily_data.append(dict)
        return daily_data

def get_today_sum():
    today = date.today().isoformat()
    with open(DATE_FILE, "r", newline="") as f:
        rows = list(csv.reader(f))
        for row in rows[1:]:
            if row[0]== today:
                return{
                    "seconds": int(row[1]),
                    "points_done": int(row[2]),
                    "points_target": int(row[3])}
        return {
            "seconds": 0,
            "points_done": 0,
            "points_target": 0
        }

def save_total(seconds, ses_points, target_points):
    today = date.today().isoformat()

    with open(DATE_FILE, newline="") as f:
        rows = list(csv.reader(f))
        # found = False
        for row in rows[1:]:
            if row[0]== today:
                row[1]=str(seconds)
                row[2]=str(ses_points+int(row[2]))



    with open(DATE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def save_session(sub_id, sub_name,ses_seconds, points):
    today = date.today().isoformat()
    with open(SES_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, sub_id, sub_name, ses_seconds, points])

def get_id(sub):
    with open(SUB_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[1]== sub:
                return row[0]

def get_sub(subj):
    subj = []
    with open(SUB_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for rows in reader:
            print(rows)
            if rows[2]=="1":
                subj.append(rows[1])
        return subj

def add_dat_subject(new_sub):
    if new_sub!="":
        with open(SUB_FILE, newline="") as f:
            rows = list(csv.reader(f))
        if len(rows)==1:
            next_id = 1
        else :
            last_id = (rows[-1][0])
            next_id = int(last_id)+1
        rows.append([str(next_id),new_sub, "1"])
        with open(SUB_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    else:
        return

def rem_dat_subject(rem_sub):
    id = get_id(rem_sub)
    print(id)
    with open(SUB_FILE, newline="") as f:
         rows = list(csv.reader(f))
         run = 1
         for row in rows[1:]:
            if row[0] == id :
                     rows[run][2]=0
            run+=1
    with open(SUB_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
def create_row():
    today = date.today().isoformat()
    with open(DATE_FILE, newline="") as f:
        rows = list(csv.reader(f))
        found = False
        for row in rows[1:]:
            if row[0]== today:
              found = True
              return
        if not found:
            rows.append([today, "0", "1", "1"])
    with open(DATE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def check_tar_pts(func):
    print("check_tar_pts")
    today = date.today().isoformat()
    with open(DATE_FILE, "r", newline="") as f:
        rows = list(csv.reader(f))
        for row in rows[1:]:
            if row[0]== today and row[3]=="1":
                print("called")
                func()
                return

def save_pts_target(points_target):
    today = date.today().isoformat()
    with open(DATE_FILE, newline="") as f:
        rows = list(csv.reader(f))
        print("cal")
        for row in rows[1:]:
            if row[0]== today and row[3]=="1":
                row[3]=str(points_target)

    with open(DATE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

