from idlelib.pyshell import restart_line
from os import remove
from random import weibullvariate
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import data_store as d

points_target = 0
total_tdy_seconds = d.get_total_seconds()
total_tdy_hrs = total_tdy_seconds//3600
total_tdy_mins = (total_tdy_seconds-total_tdy_hrs*3600)//60
total_tdy_secs = (total_tdy_seconds-total_tdy_hrs*3600 - total_tdy_mins*60)
seconds = 0
minutes = 0
hours = 0
subj = []
timer_running = False
submitted = False
submission_need = False

total_seconds = total_tdy_seconds
total_sec=total_hrs=total_mins = 0
subjects = d.get_sub(subj)
print(subjects)

#point log
def get_log():
    global submitted, submission_need
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
    raise_frames(subject_frame)

#raise frames
def raise_frames(frame):
    if submission_need:
        messagebox.showinfo("Required", "Submit Your Progress")
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
def rem_subject():
      global subjects
      subjects= d.get_sub(subj)
      r_sub_entry.set("")
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
tk_root.protocol("WM_DELETE_WINDOW", app_close_check)
window_width = 400
window_height = 300
button_pad=window_width/22
tk_root.geometry(f"{window_width}x{window_height}") #width, height size
tk_root.minsize(window_width, window_height)
tk_root.maxsize(window_width, window_height)

tk_root.title("Study Tracker")
quotes = Label(text="Quotes", relief="raised")
quotes.pack()

vcmd = tk_root.register(only_num) #for num input

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
books = Frame(container)
books.place(relx=0, rely=0, relwidth=1, relheight=1)
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

#frame buttons
Button(top_bar, text = "Subject", command=lambda : raise_frames(subject_frame), padx=button_pad).pack(side="left")
Button(top_bar, text = "Quiz", command=lambda : raise_frames(quiz_frame), padx=button_pad).pack(side="left")
Button(top_bar, text = "Logs", command=lambda : raise_frames(logs), padx=button_pad).pack(side="left")
Button(top_bar, text = "Book", command=lambda : raise_frames(books), padx=button_pad).pack(side="left")
Button(top_bar, text = "Help", command=lambda : raise_frames(details_help),padx=button_pad).pack(side="left")

#SUBJECT FRAME
total_timer_label = Label(subject_frame,
                          text=f"{total_tdy_hrs:02d}:{total_tdy_mins:02d}:{total_tdy_secs:02d}")
total_timer_label.pack()
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

#QUIZ FRAME

#BOOKS

#LOGS

#HELP

Label(details_help, text='''Points rule: \n Per Lecture :  30pts 
      \n Per Pages: 5 \n Per Questions:5''').place(relx=0.1, rely=0)

#TIMER
timer = Button(subject_frame, text = "Timer", command=lambda : (raise_frames(timer_frame), start_timer()))
timer.place(relx=0.5,  rely=0.5, anchor="center")

#after timer starts
Label(timer_frame, text="FOCUSING....").pack()
timer_label = Label(timer_frame, text="00:00:00")
timer_label.pack()
Button(timer_frame, text = "Stop Timer", command= lambda: (raise_frames(log_container), stop_timer())).pack(side="top")

#after timer stops

lec_enter = Label(log_container, text="LECTURE DONE")
page_enter = Label(log_container, text="PAGE DONE")
ques_enter = Label(log_container, text="QUES DONE")

lec_enter.grid(row=0, column=0)
page_enter.grid(row=1, column=0)
ques_enter.grid(row=2, column=0)

lecture_entry = IntVar()
pages_entry = IntVar()
questions_entry = IntVar()

lecture_entry.set(0)
pages_entry.set(0)
questions_entry.set(0)

lecture_done = Entry(log_container, textvariable= lecture_entry, validate="key",
validatecommand = (vcmd, "%P"))
pages_read = Entry(log_container, textvariable= pages_entry, validate="key",
validatecommand = (vcmd, "%P"))
questions_done = Entry(log_container, textvariable= questions_entry, validate="key",
validatecommand = (vcmd, "%P"))

lecture_done.grid(row=0, column=1)
pages_read.grid(row=1, column=1)
questions_done.grid(row=2, column=1)

Button(log_container, text="Submit", command=lambda : get_log()).grid(row=5, column=2)
raise_frames(subject_frame)

tk_root.mainloop()