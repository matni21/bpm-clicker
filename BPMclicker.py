import tkinter as tk
from tkinter import ttk
import time
from pynput import mouse
from pynput.mouse import Listener

class BpmCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BPM Clicker")

        style = ttk.Style()
        style.theme_use("alt")  #"clam" or "default" also works

        self.root.geometry("270x220")
        self.root.configure(bg="#f0f0f0")

        self.bpm_label = ttk.Label(self.root, text="Average BPM:", font=("Helvetica", 14), foreground="black", background="#f0f0f0")
        self.bpm_label.pack(pady=10)

        self.bpm_live_var = tk.StringVar()
        self.bpm_live_label = ttk.Label(self.root, textvariable=self.bpm_live_var, font=("Helvetica", 18, "bold"), foreground="black", background="#f0f0f0")
        self.bpm_live_label.pack()

        #all this just for hover colors smh.
        self.start_button_frame = tk.Frame(self.root)
        self.start_button_frame.pack(pady=5)
        self.start_button = tk.Button(self.start_button_frame, text="Start", command=self.start_listening, foreground="white", background="grey")
        self.start_button.pack(fill='both', expand=True)
        self.start_button.bind("<Enter>", lambda event: self.start_button.configure(background='darkgreen'))
        self.start_button.bind("<Leave>", lambda event: self.start_button.configure(background='grey'))

        self.stop_button_frame = tk.Frame(self.root)
        self.stop_button_frame.pack(pady=5)
        self.stop_button = tk.Button(self.stop_button_frame, text="Stop", command=self.stop_listening, state='disabled', foreground="white", background="darkgrey")
        self.stop_button.pack(fill='both', expand=True)
        self.stop_button.bind("<Enter>", lambda event: self.stop_button.configure(background='darkred'))
        self.stop_button.bind("<Leave>", lambda event: self.stop_button.configure(background='darkgrey'))



        self.total_elapsed_time = 0
        self.total_bpm = 0
        self.clicks = 0

        self.click_label = ttk.Label(self.root, text="Based on 0 clicks", font=("Helvetica", 10), foreground="black", background="#f0f0f0")
        self.click_label.pack(pady=10)

        self.mouse_listener = None

    def start_listening(self):
        self.total_elapsed_time = 0
        self.total_bpm = 0
        self.clicks = 0
        self.mouse_listener = Listener(on_click=self.on_click)
        self.mouse_listener.start()

        #self.start_button.state(['disabled'])
        #self.stop_button.state(['!disabled'])
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_listening(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

        #self.start_button.state(['!disabled'])
        #self.stop_button.state(['disabled'])
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def on_click(self, x, y, button, pressed):
        if pressed:
            click_time = time.time()
            self.clicks += 1

            if self.clicks > 1:
                elapsed_time = click_time - self.last_click_time
                bpm = 60 / elapsed_time
                self.total_elapsed_time += elapsed_time
                self.total_bpm += bpm

                average_bpm = self.total_bpm / (self.clicks - 1)
                self.bpm_live_var.set("{:.2f}".format(average_bpm))
                self.click_label.config(text="Based on {} clicks, the BPM is: {:.2f}".format(self.clicks, average_bpm))

            self.last_click_time = click_time

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BpmCalculator()
    app.run()
