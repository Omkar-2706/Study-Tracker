from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Progressbar, Treeview, Style
import data_store as d


points_target =0
data = d.get_today_sum()
total_tdy_seconds = data["seconds"]
total_tdy_hrs = total_tdy_seconds//3600
total_tdy_mins = (total_tdy_seconds-total_tdy_hrs*3600)//60
total_tdy_secs = (total_tdy_seconds-total_tdy_hrs*3600 - total_tdy_mins*60)
seconds = 0
minutes = 0
hours = 0
subj = []
quiz_on = False
timer_running = False
submitted = False
submission_need = False

total_seconds = total_tdy_seconds
total_sec=total_hrs=total_mins = 0
subjects = d.get_sub(subj)
print(subjects)

def ask_target_points():
    print("ask_target_points")
    popup = Toplevel(tk_root)
    popup.title("Target Points")
    popup.geometry("200x200")
    popup.transient(tk_root)
    popup.grab_set()
    target_var = IntVar()
    target_var.set(300)
    points_tar = Entry(popup, textvariable=target_var, validate="key",
                          validatecommand = (vcmd, "%P"))
    points_tar.pack()
    Label(popup, text="Target Points").pack()
    sub_tar =Button(popup, text="Submit", command=lambda :(tar_submit(points_tar),popup.destroy()))
    sub_tar.pack()

def tar_submit(points_tar):
   global points_target
   points_target = points_tar.get()
   d.save_pts_target(points_target)
#point log
def get_log():
    global submitted, submission_need,data
    submitted = True
    submission_need= False
    lec_done = lecture_done.get()
    pages_done = pages_read.get()
    ques_done = questions_done.get()
    lecture_entry.set(0)
    pages_entry.set(0)
    questions_entry.set(0)
    ses_points = int(lec_done)*30 + int(pages_done)*5 + int(ques_done)*2
    print(ses_points)
    d.save_total(total_seconds, ses_points, points_target)
    subj = drop_down.get()
    print(subj)
    d.save_session(d.get_id(subj),subj, seconds, ses_points)
    data = d.get_today_sum()
    percent = int((data["points_done"] / data["points_target"]) * 100)
    if percent>100:
        percent=100
    percent_txt.config(text=f"{percent}%")
    progress["value"] = percent
    raise_frames(subject_frame)

#raise frames
def raise_frames(frame):
    if submission_need:
        messagebox.showinfo("Required", "Submit Your Progress")
        return
    if quiz_on:
        messagebox.showwarning("Required", "Please Finish the Quiz")
        return
    else:
        if frame == subject_frame:
            if timer_running:
                timer_frame.tkraise()
            else:
                subject_frame.tkraise()
        else:
            frame.tkraise()


def add_subject():
      global subjects
      subjects= d.get_sub(subj)
      sub_entry.set("")
      drop_down.config(values=subjects)
      drop_down.set(subjects[0])
      rem_sub.config(values=subjects)
def rem_subject():
      global subjects
      subjects= d.get_sub(subj)
      r_sub_entry.set("")
      drop_down.set(subjects[0])
      drop_down.config(values=subjects)
#only number input for logging
def only_num(value):
    return value.isdigit() or value ==""

def start_timer():
    global timer_running, hours,seconds,minutes
    if timer_running:
        return
    if not timer_running:
        timer_running = True
        hours = 0
        minutes = 0
        seconds = 0
        update_timer()

def update_timer():
    global hours, minutes, seconds, total_seconds, total_sec, total_hrs, total_mins
    total_seconds +=1
    seconds +=1
    if not timer_running:
        return
    if seconds==60:
        seconds = 0
        minutes +=1
    if minutes==60:
        minutes = 0
        hours +=1
    timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    total_hrs = total_seconds//3600
    total_mins = (total_seconds-total_hrs*3600)//60
    total_sec = (total_seconds - total_hrs*3600 - total_mins*60)
    total_timer_label.config(text=f"{total_hrs:02d}:{total_mins:02d}:{total_sec:02d}")
    tk_root.after(1000, update_timer)

def stop_timer():
    global submitted, timer_running, hours, minutes, seconds,submission_need
    submission_need = True
    print("STOP TIMER")
    submitted = False
    if timer_running:
        timer_running = False

def app_close_check():
    if not submitted and submission_need:
        messagebox.showinfo("Required", "Submit Your Progress")
        return
    tk_root.destroy()

tk_root = Tk() #creates base for GUI
tk_root.title("Study Tracker")
vcmd = tk_root.register(only_num) #for num input
d.create_row()
d.check_tar_pts(ask_target_points)
tk_root.protocol("WM_DELETE_WINDOW", app_close_check)
window_width = 400
window_height = 300
button_pad=window_width/14
tk_root.geometry(f"{window_width}x{window_height}") #width, height size
tk_root.resizable(False,False)



top_bar = Frame(tk_root, bg="white")
top_bar.pack(side="top", fill="x")
container = Frame(tk_root)
container.pack(fill="both", expand=True)

#all frames
subject_frame = Frame(container)
subject_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
timer_frame = Frame(container, bg ="grey")
timer_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
quiz_frame = Frame(container)
quiz_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
logs = Frame(container, bg ="grey")
logs.place(relx=0, rely=0, relwidth=1, relheight=1)
log_container = Frame(container)
log_container.place(relx=0, rely=0, relwidth=1, relheight=1)
details_help = Frame(container)
details_help.place(relx=0, rely=0, relwidth=1, relheight=1)
add_sub_frame = Frame(container)
add_sub_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
remove_sub_frame = Frame(container)
remove_sub_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
quiz_section = Frame(container)
quiz_section.place(relx=0, rely=0, relwidth=1, relheight=1)
result_frame = Frame(container)
result_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
review_frame = Frame(container)
review_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
coming_soon_frame = Frame(container)
coming_soon_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
#frame buttons
Button(top_bar, text = "Subject", command=lambda : raise_frames(subject_frame), padx=button_pad).pack(side="left")
Button(top_bar, text = "Quiz", command=lambda : raise_frames(coming_soon_frame), padx=button_pad).pack(side="left")
Button(top_bar, text = "Logs", command=lambda : raise_frames(logs), padx=button_pad).pack(side="left")
Button(top_bar, text = "Help", command=lambda : raise_frames(details_help),padx=button_pad).pack(side="left")

#SUBJECT FRAME
total_timer_label = Label(subject_frame,
                          text=f"{total_tdy_hrs:02d}:{total_tdy_mins:02d}:{total_tdy_secs:02d}",
                          font=("Calibri",12))
total_timer_label.pack(pady=10)
subject_var = StringVar()
drop_down = Combobox(subject_frame, values=subjects,
                     state="readonly",textvariable=subject_var)
drop_down.set(subjects[0])
drop_down.pack()
h_btn_frame = Frame(subject_frame)
h_btn_frame.pack(pady=6)
sub_remove = Button(h_btn_frame, text="Remove Subject",
                    command=lambda : raise_frames(remove_sub_frame),
                    font=("Calibri",6))

sub_add = Button(h_btn_frame, text="Add Subject",
                 command=lambda :raise_frames(add_sub_frame),
                 font=("Calibri",6))
sub_add.pack(side="left")
sub_remove.pack(side="left")

#--NEW SUB
Label(add_sub_frame, text="Enter the Subject name below").pack()
sub_entry = StringVar()
new_sub = Entry(add_sub_frame, textvariable=sub_entry)
new_sub.pack()
Button(add_sub_frame, text="Submit", command= lambda : (raise_frames(subject_frame),
                                                        d.add_dat_subject(new_sub.get()),add_subject())).pack()
Button(add_sub_frame, text="Cancel", command= lambda : raise_frames(subject_frame)).pack()

#-- REMOVE SUB
Label(remove_sub_frame, text="Select the Subject",pady=10).pack()
r_sub_entry = StringVar()
rem_sub = Combobox(remove_sub_frame, textvariable=r_sub_entry,
                   values=subjects,state="readonly")
rem_sub.pack()
Button(remove_sub_frame, text="Submit", command= lambda : (raise_frames(subject_frame),
                                                        d.rem_dat_subject(rem_sub.get()),rem_subject())).pack()
Button(remove_sub_frame, text="Cancel", command= lambda : raise_frames(subject_frame)).pack()


#TIMER
timer = Button(subject_frame, text = "Timer", command=lambda : (raise_frames(timer_frame), start_timer()))
timer.place(relx=0.5,  rely=0.5, anchor="center")

if data["points_target"]==0:
    percent = 0
elif data["points_done"]==1:
    percent = 0
elif data["points_done"]>data["points_target"]:
    percent = 100
else:
    percent = int((data["points_done"] / data["points_target"]) * 100)
percent_txt = Label(subject_frame, text=f"{percent}%")
percent_txt.place(relx=0.5, rely=0.8, anchor="center")
style = Style()
style.theme_use("default")
style.configure(
    "Thick.Horizontal.TProgressbar",
    thickness=16
)
progress = Progressbar(
    subject_frame,
    orient="horizontal",
    length=300,
    mode="determinate",
    style="Thick.Horizontal.TProgressbar"
)
progress.pack(pady=60)
progress["maximum"]=100
progress["value"]= percent
#after timer starts
Label(timer_frame, text="FOCUSING....").pack(pady=3)
timer_label = Label(timer_frame, text="00:00:00")
timer_label.pack(pady=10)
Button(timer_frame, text = "Stop Timer", command= lambda: (raise_frames(log_container), stop_timer())).pack(side="top")

#after timer stops
pseudo_frame =  Frame(log_container,pady=20)
pseudo_frame.pack()
lb_frame = Frame(pseudo_frame)
lb_frame.pack(side="left", pady= 3)
ent_frame = Frame(pseudo_frame)
ent_frame.pack(padx=4, pady= 3)

lec_enter = Label(lb_frame, text="LECTURE DONE")
page_enter = Label(lb_frame, text="PAGE DONE")
ques_enter = Label(lb_frame, text="QUES DONE")
lec_enter.pack(anchor="w")
page_enter.pack(anchor="w")
ques_enter.pack(anchor="w")


lecture_entry = IntVar()
pages_entry = IntVar()
questions_entry = IntVar()

lecture_entry.set(0)
pages_entry.set(0)
questions_entry.set(0)

lecture_done = Entry(ent_frame, textvariable= lecture_entry, validate="key",
validatecommand = (vcmd, "%P"))
pages_read = Entry(ent_frame, textvariable= pages_entry, validate="key",
validatecommand = (vcmd, "%P"))
questions_done = Entry(ent_frame, textvariable= questions_entry, validate="key",
validatecommand = (vcmd, "%P"))
lecture_done.pack(fill="x")
pages_read.pack(fill="x",pady=4)
questions_done.pack(fill="x")

Button(log_container, text="Submit", command=lambda : get_log()).pack()

raise_frames(subject_frame)



#QUIZ FRAME
quiz_sets = []
correct_opt =[]
ques_index = 0
score = 0
wrong_set = []
wrong_index = 0
quiz_on = False
selected_opt = IntVar()

quizzes = {
    1:[("2+2?", ["10","4","6","8"],1),
       ("2 x 4?", ["10","4","6","8"],3),
       ("2+4?", ["10","4","6","8"],2)],

    2:[("5 x 10",["60","30","50","40"],2),
       ("5 x 10",["60","30","50","40"],2),
       ("5 x 10",["60","30","50","40"],2)]}




def load_questions():
    global ques_index
    sets = quiz_sets[ques_index]
    print(sets)
    question_label.config(text=f"Q{ques_index+1}: {sets[0]}")
    opt_1.config(text=f"{sets[1][0]}")
    opt_2.config(text=f"{sets[1][1]}")
    opt_3.config(text=f"{sets[1][2]}")
    opt_4.config(text=f"{sets[1][3]}")
    selected_opt.set(-1)


def start_quiz(quiz_id):
    global quiz_sets, ques_index, quiz_on, score,wrong_set
    quiz_sets = quizzes[quiz_id]
    ques_index = 0
    score=0
    wrong_set = []
    question_label.config(text="")
    opt_1.config(text="")
    opt_2.config(text="")
    opt_3.config(text="")
    opt_4.config(text="")
    raise_frames(quiz_section)
    quiz_on = True
    load_questions()


def show_wrong_ques():
    raise_frames(review_frame)
    global wrong_set,wrong_index
    print(wrong_set)

    if wrong_index < len(wrong_set):
        o.config(text = wrong_set[wrong_index]["question"])
        n.config(text=wrong_set[wrong_index]["user_"])
        k.config(text=wrong_set[wrong_index]["correct_answer"])
        wrong_index += 1
    else:
        n_btn.pack_forget()
        q_btn.pack()

def reset_frame():
    q_btn.pack_forget()


def show_result():
    global score, correct_opt, wrong_set, quiz_sets, quiz_on
    quiz_on = False
    raise_frames(result_frame)
    if score == len(quiz_sets):
        result_q_label.config(text=f"{score}/{len(quiz_sets)} \n Perfect!")
        q_btn.pack()
    else:
        result_q_label.config(text=f"{score}/{len(quiz_sets)} \n Try Hard Next Time")
        r_btn.pack()



def next_question():
    global ques_index, score, correct_opt, wrong_set
    correct_opt = quiz_sets[ques_index][2]
    if selected_opt.get()== -1:
        messagebox.showerror("Error", "Select a correct option")
        return
    if selected_opt.get() == correct_opt:
        score += 1
    else:
        wrong_set.append({
            "question":quiz_sets[ques_index][0],
            "user_":quiz_sets[ques_index][1][selected_opt.get()],
            "correct_answer":quiz_sets[ques_index][1][correct_opt],
        })
    ques_index += 1
    if ques_index >= len(quiz_sets):
           print(wrong_set)
           show_result()
    load_questions()

#COMING SOON
Label(coming_soon_frame, pady=20, text='''This module is currently under development.
Will be added in future updates.''').pack()
question_label = Label(quiz_section, text="")
question_label.pack()
opt_1 = Radiobutton(quiz_section, text="", variable=selected_opt, value=0)
opt_1.pack()
opt_2 = Radiobutton(quiz_section, text="", variable=selected_opt, value=1)
opt_2.pack()
opt_3 = Radiobutton(quiz_section, text="", variable=selected_opt, value=2)
opt_3.pack()
opt_4 = Radiobutton(quiz_section, text="", variable=selected_opt, value=3)
opt_4.pack()
Button(quiz_frame, text="Start", command=lambda : start_quiz(1)).pack()
submit_opt = Button(quiz_section, text="Next", command=next_question)
submit_opt.pack()

result_q_label = Label(review_frame, text="")
result_q_label.pack()
o = Label(review_frame, text="")
n= Label(review_frame, text="")
k = Label(review_frame, text="")
o.pack()
n.pack()
k.pack()
r_btn = Button(result_frame, text="Review", command=show_wrong_ques)
q_btn = Button(review_frame, text="Quit", command=lambda: (raise_frames(subject_frame), reset_frame()))

n_btn=Button(review_frame, text="Next", command=show_wrong_ques)
n_btn.pack()



#LOGS FRAME
l_btn_frame = Frame(logs, width=50,height=50, bg="grey")
l_btn_frame.place(relx=0.07, rely=0.5, anchor="center")
Button(l_btn_frame, text="Daily", command=lambda : show_daily_log(), font=("Arial", 9), width="7").pack()
Button(l_btn_frame, text="Session", command=lambda : show_ses_log(),font=("Arial", 9), width="7").pack()

log_details = Frame(logs, relief=SUNKEN, borderwidth=2, width=320, height=220)
log_details.place(relx=0.55, rely=0.5, anchor="center")
log_table = Treeview(log_details, columns=("1", "2", "3", "4"), show="headings")
log_table.column("1", width=90)
log_table.column("2", width=70)
log_table.column("3", width=80)
log_table.column("4", width=80)
def show_daily_log():
    daily_data = d.get_daily_total()
    log_table.heading("1", text="Date")
    log_table.heading("2", text="Time")
    log_table.heading("3", text="Pts Earned")
    log_table.heading("4", text="Pts Target")
    log_table.place(relx=0.5, rely=0.5, anchor="center")
    for content in daily_data:
        date = content["date"]
        time = int(content["time"])
        h = time // 3600
        m = (time - h * 3600) // 60
        s = (time - h*3600 - m*60)
        gen_time = f"{h:02d}:{m:02d}:{s:02d}"
        pts_earned = content["points_done"]
        pts_target = content["points_target"]
        log_table.insert(parent='',index=0, values=((date),(gen_time),(pts_earned),(pts_target)))



def show_ses_log():
    ses_data = d.get_ses()
    print(ses_data)
    log_table.heading("1", text="Date")
    log_table.heading("2", text="Subject")
    log_table.heading("3", text="Seconds")
    log_table.heading("4", text="Points")
    log_table.place(relx=0.5, rely=0.5, anchor="center")
    for content in ses_data:
        date = content["date"]
        subject = content["subjects"]
        time = int(content["seconds"])
        h = time // 3600
        m = (time - h * 3600) // 60
        s = (time - h * 3600 - m * 60)
        gen_time = f"{h:02d}:{m:02d}:{s:02d}"
        points = content["points"]
        log_table.insert(parent='',index=0, values=((date),(subject),(gen_time),(points)))
#HELP
Label(details_help, text='''Points rule: \n Per Lecture :  30pts 
      \n Per Pages: 5 \n Per Questions:5''').place(relx=0.1, rely=0)
tk_root.mainloop()