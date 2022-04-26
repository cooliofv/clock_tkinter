# pip install -m pyinstaller
# pyinstaller ./main.py -F -w

import time
import tkinter as t
from tkinter import ttk
from tkinter import font
from time import strftime
from datetime import timedelta, timezone, datetime

import params as p

millesec = 0
seconds = 0
minutes = 0
hours = 0

clock_started_state = False
window_main_after_id = 0
timer_mode = 'stopwatch'

window_main = t.Tk()
window_main.title(' ЧАСЫ ')
window_main.resizable(False, False)
window_main.wm_attributes('-fullscreen', False)
window_main.wm_attributes('-topmost', True)
# window_main.overrideredirect(True)

screen_height = window_main.winfo_screenwidth()
screen_width = window_main.winfo_screenheight()
window_height = 600
window_width = 500
x_window_main = int((screen_width / 2) - (window_width / 2))
y_window_main = int((screen_height / 2) - (window_height / 2))
window_main.geometry(
    f'{window_height}x{window_width}+{y_window_main}+{x_window_main}')
window_main.config(bg=p.WINDOW_BACKGROUND)


frame_main = t.Frame(master=window_main, bg=p.WINDOW_BACKGROUND)
frame_menu_buttons = t.Frame(
    master=frame_main, pady=10, bg=p.WINDOW_BACKGROUND)
frame_clock = t.Frame(master=frame_main, padx=50, pady=50, bg='black')
frame_buttons = t.Frame(master=frame_main, padx=20,
                        pady=20, bg=p.WINDOW_BACKGROUND)
frame_clock_time = t.Frame(master=frame_main, padx=20,
                           pady=20, bg=p.WINDOW_BACKGROUND)
frame_timer_sel = t.Frame(master=frame_main, bg=p.WINDOW_BACKGROUND, height=55)
frame_timer_sel_inner = t.Frame(master=frame_timer_sel, bg=p.WINDOW_BACKGROUND)
frame_btn_bottom = t.Frame(master=frame_main)

frame_main.pack()
frame_menu_buttons.pack()
frame_clock.pack()
frame_buttons.pack()
frame_timer_sel.pack()
frame_clock_time.pack()
frame_timer_sel_inner.pack()

btn_timer = t.Button(master=frame_menu_buttons, width=13, text='ТАЙМЕР', bg='black',
                     fg=p.COLOR_CLOCK, font=('Arial', 18, 'bold'), command=lambda: set_mode('timer'))
btn_stopwatch = t.Button(master=frame_menu_buttons, width=13, text='СЕКУНДОМЕР', bg='black',
                         fg=p.COLOR_CLOCK, font=('Arial', 18, 'bold'), command=lambda: set_mode(mode='stopwatch'))
btn_timer.grid(row=0, column=0)
btn_stopwatch.grid(row=0, column=2)


label_hour = t.Label(master=frame_clock, fg=p.COLOR_CLOCK,
                     bg='black', font=(p.FONT_FAMILY, p.FONT_SIZE), text='00')
label_min = t.Label(master=frame_clock, fg=p.COLOR_CLOCK,
                    bg='black', font=f'{p.FONT_FAMILY}, {p.FONT_SIZE}', text='00')
label_sec = t.Label(master=frame_clock, fg=p.COLOR_CLOCK,
                    bg='black', font=f'{p.FONT_FAMILY}, {p.FONT_SIZE}', text='00')
label_mils = t.Label(master=frame_clock, fg=p.COLOR_CLOCK,
                     bg='black', font=f'{p.FONT_FAMILY}, {p.FONT_SIZE}', text='000')

label_hour.pack(side='left')
t.Label(master=frame_clock,  fg=p.COLOR_CLOCK, bg='black',
        font=f'{p.FONT_FAMILY}, {p.FONT_SIZE}', text=':').pack(side='left')
label_min.pack(side='left')
t.Label(master=frame_clock,  fg=p.COLOR_CLOCK, bg='black',
        font=f'{p.FONT_FAMILY}, {p.FONT_SIZE}', text=':').pack(side='left')
label_sec.pack(side='left')
t.Label(master=frame_clock,  fg=p.COLOR_CLOCK, bg='black',
        font=f'{p.FONT_FAMILY}, {p.FONT_SIZE}', text='.').pack(side='left')
label_mils.pack(side='left')


btn_start = t.Button(master=frame_buttons, bg='green', fg='white',
                     padx=10, pady=10, text='СТАРТ', command=lambda: timer_start())
btn_start.pack(side='left')
btn_pause = t.Button(master=frame_buttons, bg='orange', fg='white',
                     padx=10, pady=10, text='ПАУЗА', command=lambda: timer_pause())
btn_pause.pack(side='left')
btn_stop = t.Button(master=frame_buttons, bg='red', fg='white',
                    padx=10, pady=10, text='СТОП', command=lambda: timer_stop())
btn_stop.pack(side='left')


cmbx_value = list(range(0, 61))
cmbx_style = ttk.Style()
cmbx_style.theme_use('clam')
cmbx_style.configure(
    "TCombobox", foreground='black', background='yellow')
cmbx_hour = ttk.Combobox(master=frame_timer_sel_inner,
                         values=cmbx_value, **p.STYLE_COMBOBOX)
cmbx_min = ttk.Combobox(master=frame_timer_sel_inner,
                        values=cmbx_value, **p.STYLE_COMBOBOX)
cmbx_sec = ttk.Combobox(master=frame_timer_sel_inner,
                        values=cmbx_value, **p.STYLE_COMBOBOX)
lbl_cmbx_hour = ttk.Label(master=frame_timer_sel_inner,
                          text='ЧАС', background=p.WINDOW_BACKGROUND, foreground='white')
lbl_cmbx_min = ttk.Label(master=frame_timer_sel_inner,
                         text='МИНУТА', background=p.WINDOW_BACKGROUND, foreground='white')
lbl_cmbx_sec = ttk.Label(master=frame_timer_sel_inner,
                         text='СЕКУНДА', background=p.WINDOW_BACKGROUND, foreground='white')


def setTimerLabel(event):
    global seconds, minutes, hours
    seconds = int(cmbx_sec.get())
    minutes = int(cmbx_min.get())
    hours = int(cmbx_hour.get())
    change_label(label_sec, seconds)
    change_label(label_min, minutes)
    change_label(label_hour, hours)


cmbx_hour.current(0)
cmbx_min.current(0)
cmbx_sec.current(0)
cmbx_hour.bind('<<ComboboxSelected>>', setTimerLabel)
cmbx_min.bind('<<ComboboxSelected>>', setTimerLabel)
cmbx_sec.bind('<<ComboboxSelected>>', setTimerLabel)

cmbx_hour.grid(row=1, column=0)
cmbx_min.grid(row=1, column=1)
cmbx_sec.grid(row=1, column=2)
lbl_cmbx_hour.grid(row=0, column=0)
lbl_cmbx_min.grid(row=0, column=1)
lbl_cmbx_sec.grid(row=0, column=2)

btn_ext_font = font.Font(family='Courier', size=20, weight='bold')
btn_exit = t.Button(
    master=window_main,
    bg='red',
    fg='white',
    font=btn_ext_font,
    text='Выход',
    borderwidth=0,
    command=lambda: program_exit())
btn_exit.pack(side=t.BOTTOM, fill=t.BOTH)

label_clock = t.Label(master=frame_clock_time, fg=p.COLOR_CLOCK,
                      bg='black', font=f'{p.FONT_FAMILY}, {22}')
label_clock.pack()


def set_mode(mode):
    global timer_mode
    timer_mode = mode

    if mode == 'stopwatch':
        btn_stopwatch.config(state=t.DISABLED)
        btn_timer.config(state=t.NORMAL)
        frame_timer_sel_inner.forget()

    if mode == 'timer':
        setTimerLabel(event='')
        btn_stopwatch.config(state=t.NORMAL)
        btn_timer.config(state=t.DISABLED)
        frame_timer_sel_inner.pack()


def change_label(lbl, time_unit, mill=False):
    if mill:
        if time_unit < 10:
            time_unit = f'00{time_unit}'
        elif time_unit < 100:
            time_unit = f'0{time_unit}'
    else:
        if time_unit < 10:
            time_unit = f'0{time_unit}'

    lbl.config(text=f'{time_unit}')


def timer_start():
    global millesec, seconds, minutes, hours, timer_state, change_label, window_main_after_id, timer_mode

    if timer_mode == 'stopwatch':
        millesec = millesec + 1

        if millesec == 1000:
            millesec = 0
            seconds += 1

        if seconds == 60:
            seconds = 0
            minutes += 1

        if minutes == 60:
            minutes = 0
            hours += 1

    if timer_mode == 'timer':

        if millesec == 0 and seconds > 0:
            seconds -= 1
        if seconds == 0 and minutes > 0:
            seconds = 59
            minutes -= 1

        if millesec == 0:
            millesec = 1000

        print(f'HR: {hours} MIN: {minutes} SEC: {seconds} MILL: {millesec}')
        if hours == 0 and minutes == 0 and seconds == 0:
            timer_stop()
            return

        millesec -= 1

    change_label(label_sec, seconds)
    change_label(label_min, minutes)
    change_label(label_hour, hours)
    change_label(label_mils, millesec, mill=True)

    window_main_after_id = window_main.after(1, timer_start)

    btn_start.config(state=t.DISABLED)


def timer_stop():
    global millesec, seconds, minutes, hours, timer_state, change_label, window_main_after_id

    if window_main_after_id:
        window_main.after_cancel(window_main_after_id)

    millesec = 0
    seconds = 0
    minutes = 0
    hours = 0

    change_label(label_mils, millesec, mill=True)
    change_label(label_sec, seconds)
    change_label(label_min, minutes)
    change_label(label_hour, hours)
    btn_start.config(state=t.NORMAL)


def timer_pause():
    window_main.after_cancel(window_main_after_id)
    btn_start.config(state=t.NORMAL)


def program_exit():
    window_main.destroy()


def clock():
    tz_info = timezone(timedelta(hours=3.0))
    now = datetime.now(tz=tz_info)
    string = now.strftime('%H:%M:%S %p')
    label_clock.config(text=string)
    label_clock.after(1000, clock)


set_mode('stopwatch')
clock()

window_main.mainloop()
