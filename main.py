from tkinter import *
from random import shuffle


class TypeSpeedTest:

    def __init__(self, data):
        # Basci setup
        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.minsize(height=500, width=700)
        self.window.maxsize(height=500, width=700)
        self.BG='#b4ede9'
        self.typewriter = PhotoImage(file='typewriter.png')
        # getting words
        self.words = data
        # intro page
        self.start_page()
        # required attributes declaration
        self.word_index= 0
        self.pos=0
        self.wpm=0
        self.cpm=0
        # reading high score
        with open('high_score.txt') as f:
            value = f.read()
            self.highest_wpm = int(value)
        self.window.mainloop()


    def start_page(self):
        # Intro page setup
        self.canva = Canvas(height=500, width=700)
        self.canva.grid(row=0, column=0)
        # background image
        self.canva.create_image(350, 250, image=self.typewriter)
        # title
        self.canva.create_text(350, 80, text="TYPING SPEED TEST", fill='#c14134', font=('Arial', 29, 'bold'))
        # start button
        self.start_btn = Button(text="Start", bg="#4ac78b", font=('Arial', 29, 'bold'), fg='white', activebackground="#4ac78b", command=self.start_test)
        self.start_btn.place(x=290, y=180)
        


    def clear_widget(self):
        # to delete all widgets in the window except window widget
        for widget in self.window.winfo_children():
            if widget != self.window:
                widget.destroy()


    def timer_countdown(self, count):
    #  to make countown upto 1 min
        if count<=60:
            self.timer.config(text=f"TIME: {count}", fg='#2d6da7')
            self.type_text.config(state='normal')
            self.type_text.focus_set()  

            # if count down is within 10 seconds, turn text to red color
            if count < 10:
                self.timer.config(fg='red')

            # if countwodn ended, disbale the entering text widget and show result
            if count == 0:
                self.timer.config(text='Time up')
                self.window.after_cancel("self.window_after")
                self.calculate_score()
                self.type_text.config(state='disabled')
                self.result_page()
        # if count is greater than 0 then call window.after()
        if count > 0:
            self.window_after = self.window.after(1000, self.timer_countdown, count-1)
        # to give some time before starting the test
        if count >60:
            self.timer.config(text=f"Test starts in {count-60}", fg="#4ac78b")
        
            

    def start_test(self):
        # test page setup
        self.clear_widget()
        self.window.config(bg=self.BG, padx=10, pady=5)
        # title
        self.title = Label(text='Typing Speed Test', bg=self.BG, font=('Arial', 25, 'bold'), fg='#193148')
        self.title.grid(row=1, column=4)
        # time
        self.timer = Label(text='TIME: 0', bg=self.BG, font=('Arial', 10, 'bold'), fg='#2d6da7')
        self.timer.grid(row=0, column=4)
        # displaying words
        self.display_text = Text(font=('Arial', 20, 'normal'), height=7, width=30, padx=7, pady=7)
        self.display_text.grid(row=3, column=4, padx=10, pady=10)
        # creating tags
        self.display_text.tag_config('wrong', foreground='red')
        self.display_text.tag_config('active', background='#84A2B6', foreground='white')
        self.display_text.tag_config('correct', foreground='#8fce00')
        # inserting words in display widget
        text_to_display = ' '.join(self.words)
        self.display_text.insert(END, text_to_display)
        # making display widget non interactive
        self.display_text.config(state='disabled') 
        # creating input widget
        self.type_text = Text(width=30, height=1, font=('Arial', 20, 'normal'), state='disabled', padx=7, pady=7)
        self.type_text.grid(row=4, column=4, pady=10)
        # calling check spell method whenever the event occurs
        self.type_text.bind('<KeyRelease>', self.check_spell)
        # beginning timer countdown
        self.timer_countdown(65)
        # displaying words per minute
        self.wpm_label = Label(text='WPM', justify='left', bg=self.BG, font=('Arial', 10, 'bold'), fg='#2d6da7')
        self.wpm_label.grid(row=0, column=0, pady=10)
        self.wpm_value = Label(text=self.wpm, justify='left', bg=self.BG, font=('Arial', 10, 'bold'), fg='#c14134')
        self.wpm_value.grid(row=0, column=1, pady=10)
        # display charcters per minute
        self.cpm_label = Label(text='CPM', justify='left', bg=self.BG, font=('Arial', 10, 'bold'), fg='#2d6da7')
        self.cpm_label.grid(row=0, column=2, pady=10)
        self.cpm_value = Label(text=self.cpm, justify='left', bg=self.BG, font=('Arial', 10, 'bold'), fg='#c14134')
        self.cpm_value.grid(row=0, column=3, pady=10)
        

    def check_spell(self, event):
        # to check spell
        # getting position before cursor
        self.pos = int(self.type_text.index(INSERT).split('.')[1]) -1 
        # getting the active word to check
        word = self.words[self.word_index]
        # getting starting line.column index and ending line.column index
        start = self.display_text.search(word, f"1.0 + {self.pos - len(word)}c", f"1.0 +{self.pos + 20}c")
        end = f"{start} +{len(word)}c"
        # calculating score and updating wopm and cpm
        self.calculate_score()
        self.wpm_value.config(text=self.wpm)
        self.cpm_value.config(text=self.cpm)
      

        if start != '':
            # adding active tag to currect word
            self.display_text.tag_add('active', start, end)

            # chnaging word if user move back to correct the mistaken word
            if event.keycode == 8 or self.pos < int(start.split('.')[1])-1  and self.pos > 0:
                self.display_text.tag_remove('active', start, end)
                self.word_index-=1
            # moving to next word
            if self.pos+1 == int(start.split('.')[1] ) + len(word):
                self.display_text.tag_remove('active', start, end)
                self.word_index+=1
                
        # auto scrolling to display more words
        if self.pos > 230:
            self.display_text.see(f"1.0 + {self.pos+60}c")
        # adding red mark if wrong character
        if self.display_text.get(f"1.0 + {self.pos}c") != self.type_text.get(f"1.0 + {self.pos}c") and event.keycode != 8 and event.keycode != 16:
            self.display_text.tag_add('wrong', f"1.0 + {self.pos}c")
        # removing any tag if going backspace
        elif event.keycode == 8:
            self.display_text.tag_remove('correct', f"1.0 + {self.pos+1}c")
            self.display_text.tag_remove('wrong', f"1.0 + {self.pos+1}c")
        # adding green mark if correct
        else:
            self.display_text.tag_remove('wrong', f"1.0 + {self.pos}c")
            self.display_text.tag_add('correct', f"1.0 + {self.pos}c")
            

    def calculate_score(self):
        # calculating score by matching display widget and input widget
        self.wpm=0
        self.cpm=0
        entered_text = self.type_text.get('1.0', END)
        typed_words = entered_text.split(' ')
        self.cpm = len(entered_text)
        for i in range(len(typed_words)):
            if typed_words[i] == self.words[i]:
                    self.wpm+=1
        

    def result_page(self):
        # showing result and result page setup
        if self.wpm > self.highest_wpm:
            self.highest_wpm = self.wpm
        self.clear_widget()
        self.window.config(bg=self.BG, padx=55, pady=100)
        # title
        self.title = Label(text="Your Result", bg=self.BG, font=('Arial', 15, 'bold'), fg='#193148')
        self.title.grid(row=0, column=0)
        # display wpm
        self.wpm_res = Label(text=f"Words Per Minute: {self.wpm}", bg=self.BG, font=('Arial', 35, 'bold'), fg='#299760')
        self.wpm_res.grid(row=1, column=0)
        # displaying cpm
        self.cpm_res = Label(text=f"Character Per Minute: {self.cpm}", bg=self.BG, font=('Arial', 35, 'bold'), fg='#299760')
        self.cpm_res.grid(row=2, column=0)
        # display highscore
        self.wpm_high = Label(text=f"Highest WPM: {self.highest_wpm}", bg=self.BG, font=('Arial', 35, 'bold'), fg='#299760')
        self.wpm_high.grid(row=3, column=0)

        # retry test button
        self.retry = Button(text='Retry',bg="#c14134", font=('Arial', 29, 'bold'), fg='white', activebackground="#4ac78b", command=self.start_test)
        self.retry.grid(row=4, column=0)

        # updating hight score
        with open('high_score.txt', 'w') as file:
            file.write(str(self.highest_wpm))



# reading words from text file
with open('data.txt', 'r') as datafile:
    data = datafile.read()
    data_list = data.split(' ')
    shuffle(data_list)

# creating object and starting the test application
test = TypeSpeedTest(data_list)
