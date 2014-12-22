#!/usr/bin/python3

# szymon version 12/03/2014
# modules used by workout101 program

from tkinter import *
import tkinter.font as tkFont
import shelve
from time import *
from calendar import monthcalendar

############################################################## BACKGROUND ######
class Background(Frame):
    '''This object shows background image on the screen'''
    def __init__(self, frame):
        Frame.__init__(self, frame)
#        self.grid()
        picture = PhotoImage(file = 'components/img/workout_600x550.gif')
        pic = Label(self, image = picture, bg = 'green')
        pic.image = picture
        pic.grid()

##############################################################BACKGROUND END ###
################################################################## STATUS ######
class Status(Frame):
    '''This object serves messages which appear on status line.'''
    def __init__(self, vc, frame, msg = 'Welcome to Workout 101', color = 'gray20'):
        Frame.__init__(self, frame)
        self.vc = vc
        self.grid(sticky = W+E)
        self.msg = StringVar()
        self.color = StringVar()
        self.msg.set(msg)
        self.color.set(color)
        Label(self, font = ('Times', '10', 'italic'),
              textvariable = self.msg, fg = self.color.get()).grid(sticky = W+E)

    def set(self, msg, color = 'gray'):
        self.msg.set(msg)
        self.color.set(color)
################################################################## STATUS END###
############################################################### ABOUTVIEW ######
class AboutView(Frame):
    '''Widget 'about' '''
    def __init__(self, vc, frame):
        Frame.__init__(self, frame)
        self.grid()
        self.configure(bg = 'grey60', width = 300, height = 230, bd = 10)
        self.grid_propagate(0)
        self.vc = vc
        self.make_widget()
        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_about_view_delegate) # Exit action when x (top right corner) pressed

    def make_widget(self):
        Label(self, fg = 'white', bg = 'grey60', text = 'WORKOUT 101',font = ('Droid Sans', 16, 'bold')).grid(row = 0, column = 0, sticky = W)
        Label(self, fg = 'white', bg = 'grey60', text = '\n\nPersonal workout planner',font = ('Droid Sans', 12, 'bold')).grid(row = 1, column = 0, sticky = W)
        Label(self, fg = 'white', bg = 'grey60', text = '\n\n\nemail: person@xxxxx.xxx',font = ('Droid Sans', 10)).grid(row = 2, column = 0, sticky = W)
        Label(self, fg = 'white', bg = 'grey60', text = 'www: www.xxxxx.xxx',font = ('Droid Sans', 10)).grid(row = 3, column = 0, sticky = W)

        b_close = Button(self, text = 'close', command = self.vc._exit_on_about_view_delegate)
        b_close.grid(row = 5, column = 1, sticky = E+S)
############################################################### ABOUTVIEW END###
############################################################### HELPVIEW #######
class HelpView(Frame):
    '''Widget 'help' '''
    def __init__(self, vc, frame, mode = 'view'):
        Frame.__init__(self, frame)
        self.grid()
        self.vc = vc
        self.mode = mode
        self.make_widget()
        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_help_view_delegate) # Exit action when x (top right corner) pressed

    def make_widget(self):
        text__01 = Text(self, font = ('Droid Sans', 10), width = 70, height = 30)
        text__01.insert('1.0', self.vc.model._get_help_text())
        if self.mode == 'view':
            text__01.config(state = DISABLED)
        scr___01 = Scrollbar(self, command = text__01.yview)
        text__01.config(yscrollcommand=scr___01.set)

        text__01.grid(row = 0, column = 0, columnspan = 2, sticky = W, padx = 5, pady = 5)
        scr___01.grid(row = 0, column = 2, sticky = N+S)
        
        if self.mode == 'edit':
            b_save = Button(self, text = 'save', command = lambda: self.vc.model._save_help(text__01.get(1.0, END)))
            b_save.grid(row = 1, column = 0, sticky = W)

        b_close = Button(self, text = 'close', command = self.vc._exit_on_help_view_delegate)
        b_close.grid(row = 1, column = 1, columnspan = 2, sticky = E)


############################################################### HELPVIEW END####
############################################################### FAQVIEW ########
class FAQView(Frame):
    '''Widget 'help' '''
    def __init__(self, vc, frame, mode = 'view'):
        Frame.__init__(self, frame)
        self.grid()
        self.vc = vc
        self.mode = mode
        self.make_widget()
        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_FAQ_view_delegate) # Exit action when x (top right corner) pressed

    def make_widget(self):
        text__01 = Text(self, width = 70, height = 30)
        text__01.insert('1.0', self.vc.model._get_FAQ_text())
        if self.mode == 'view':
            text__01.config(state = DISABLED)
        scr___01 = Scrollbar(self, command = text__01.yview)
        text__01.config(yscrollcommand=scr___01.set)

        text__01.grid(row = 0, column = 0, columnspan = 2, sticky = W, padx = 5, pady = 5)
        scr___01.grid(row = 0, column = 2, sticky = N+S)
        
        if self.mode == 'edit':
            b_save = Button(self, text = 'save', command = lambda: self.vc.model._save_FAQ(text__01.get(1.0, END)))
            b_save.grid(row = 1, column = 0, sticky = W)

        b_close = Button(self, text = 'close', command = self.vc._exit_on_FAQ_view_delegate)
        b_close.grid(row = 1, column = 1, columnspan = 2, sticky = E)


############################################################### FAQVIEW END ####
############################################################### EXCERCISES #####
class Excercises(Frame):
    '''Widget 'exercises'. Shows a list of exercises for particular body part on the screen. '''
    def __init__(self, vc, frame, BP_ID, ex_IDs, mode):
        Frame.__init__(self, frame)
        self.vc = vc
        self.mode = mode
        self.grid()
        self.ex_IDs = ex_IDs
        self.bp_ID = BP_ID
        
      # buttons - list of buttons
        chk_buttons = []
        sel_buttons = []
        state = []
      # buttons definitions loop 
        for i, exercise_ID in enumerate(self.ex_IDs):
            state.append(IntVar())
            t_tmp = self.vc.model._get_exercise_name(exercise_ID)
            t_tmp = t_tmp + (30 - len(t_tmp))*'_'
            if self.mode == 'new_workout':
                cb_tmp = Checkbutton(self,
                        bd = 0,
                        activeforeground='Red',
                        font = ('Courier', 10),
                        variable = state[i],
                        command = lambda b = self.ex_IDs[i], a = self.bp_ID, c = i: self.vc._exercise_selected(a, b, c))
                if [self.bp_ID, exercise_ID] in self.vc.model.cart.get_content(): # turn on checkbox if was 
                    cb_tmp.select()                                               # previously selected
                chk_buttons.append(cb_tmp)
            sb_tmp = Button(self,
                     bd = 0,
                     text = t_tmp,
                     activeforeground='Red',
                     font = ('Courier', 10),
                     command = lambda a = self.bp_ID, b = self.ex_IDs[i], c = self.mode: self.vc._exercise_record(a, b, c))
            sel_buttons.append(sb_tmp)

            if self.mode == 'new_workout':
                chk_buttons[i].grid(row = i,column = 0, sticky = W)
            sel_buttons[i].grid(row = i, column = 1, sticky = W)
            self.vc.state_1 = state
############################################################### EXCERCISES END##
############################################################### EXERCISE #######
class ExcerciseView(Frame):
    '''Widget exercise. Shows one, choosed exercise record on the screen '''
    def __init__(self, vc, frame, EX_ID, BO_ID, mode):
        Frame.__init__(self, frame)
        self.vc = vc
        self.mode = mode
        self.grid()
        self.bo_key = BO_ID     # <--- actual BO-ID
        self.ex_key = EX_ID     # <--- actual EX-ID
        self.img_path = 'components/img/exercises/'
        self.make_widget()
        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_exercise_view_delegate) # Exit action when x (top right corner) pressed
     
    def make_widget(self):
        self.exercise_name = StringVar()
        self.exercise_image_filename = StringVar()
        if self.mode == 'new_exercise':
            self.exercise_name.set(self.vc.model._get_exercise_name('EX-NEW')) # assign name from database
            self.exercise_info = self.vc.model._get_exercise_info('EX-NEW')    # assign info from database
            self.exercise_image_filename.set(self.img_path + self.vc.model._get_exercise_img_file_name('EX-NEW')) # assign image file name from database
            self.exercise_image = PhotoImage(file = self.exercise_image_filename.get(), width=390, height=200) # create PhotoImage object
        else:
            self.exercise_name.set(self.vc.model._get_exercise_name(self.ex_key)) # assign name from database
            self.exercise_info = self.vc.model._get_exercise_info(self.ex_key)    # assign info from database
            self.exercise_image_filename.set(self.img_path + self.vc.model._get_exercise_img_file_name(self.ex_key)) # assign image file name from database
            try:
                img_file = self.exercise_image_filename.get()
                self.exercise_image = PhotoImage(file = self.exercise_image_filename.get(), width=390, height=200) # create PhotoImage object
            except:
                messagebox.showerror('Error', 'Image file is missing.\nSubstitution with blank image.')
                img_file = self.img_path + self.vc.model._get_exercise_img_file_name('EX-NEW')
                self.exercise_image_filename.set(img_file)
                self.exercise_image = PhotoImage(file = self.exercise_image_filename.get(), width=390, height=200) # create PhotoImage object

        label_01 = Label(self, font = ('Courier', 10), text = 'Body part ID:_____ ' + self.bo_key)
        label_02 = Label(self, font = ('Courier', 10), text = 'Body part name:___ ' + self.vc.model._get_body_part_name(self.bo_key))
        label_03 = Label(self, font = ('Courier', 10), text = 'Excercise ID:_____ ' + self.ex_key)
        label_04 = Label(self, font = ('Courier', 10), text = 'Excercise name:___ ' + self.exercise_name.get())
        entry_04 = Entry(self, font = ('Courier', 10), textvariable = self.exercise_name, width = 40)
        label_05 = Label(self, image = self.exercise_image, height = 200, width = 390)
        label_05.image = self.exercise_image
        self.button05 = Button(self, image = self.exercise_image, height = 200, width = 390, command = self._load_image)
        self.button05.image = self.exercise_image
        label_06 = Label(self, font = ('Courier', 10), text = '\nExcercise description:')
        self.text__01 = Text(self,  font = ('Courier', 8), width = 62, height = 22)
        self.text__01.insert('1.0', self.exercise_info)
        scr___01 = Scrollbar(self, command = self.text__01.yview)
        self.text__01.config(yscrollcommand=scr___01.set)
        label_01.grid(row = 0, column = 0, columnspan = 2, sticky = W, padx = 5)
        label_02.grid(row = 1, column = 0, columnspan = 2,  sticky = W, padx = 5)
        label_03.grid(row = 2, column = 0, columnspan = 2,  sticky = W, padx = 5)
        button06 = Button(self, text = 'save', command = self._save)
        button07 = Button(self, text = 'delete', command = self._delete)
        
        label_05.grid(row = 4, column = 0, columnspan = 2,  sticky = W, padx = 5)
        label_06.grid(row = 5, column = 0, columnspan = 2,  sticky = W, padx = 5)
        self.text__01.grid(row = 6, column = 0, sticky = W, padx = 5, pady = 5)
        scr___01.grid(row = 6, column = 1, sticky = N+S)
        if self.mode == 'new_workout':
            self.text__01.config(state = DISABLED)
            label_04.grid(row = 3, column = 0, columnspan = 2,  sticky = W, padx = 5)
            label_05.grid(row = 4, column = 0, columnspan = 2,  sticky = W, padx = 5)
        elif self.mode == 'new_exercise':
            self.text__01.config(height = 18)
            entry_04.grid(row = 3, column = 0, columnspan = 2,  sticky = W, padx = 5)
            self.button05.grid(row = 4, column = 0, columnspan = 2,  sticky = W, padx = 5)
            button06.grid(row = 7, column = 0, sticky = E, padx = 5, pady = 5)
        elif self.mode == 'edit_exercise':
            self.text__01.config(height = 18)
            entry_04.grid(row = 3, column = 0, columnspan = 2,  sticky = W, padx = 5)
            self.button05.grid(row = 4, column = 0, columnspan = 2,  sticky = W, padx = 5)
            button06.grid(row = 7, column = 0, sticky = E, padx = 5, pady = 5)
            button07.grid(row = 7, column = 0, sticky = W, padx = 5, pady = 5)
            
    def _delete(self):
        decision = messagebox.askokcancel('Confirm', 'Are you sure to delete\nthis exercise from database.')
        if decision:
            self.vc._exercise_delete(self.bo_key, self.ex_key)

    def _save(self):
        BO_ID   = self.bo_key
        EX_ID   = self.ex_key
        EX_NAME = self.exercise_name.get()
        EX_INFO = self.text__01.get(1.0, END)
        EX_IMG  = self.exercise_image_filename.get()
        self.vc._exercise_save(BO_ID, EX_ID, EX_NAME, EX_INFO, EX_IMG)

    def _load_image(self):
        '''set new image for actual excercise'''
        tmp = filedialog.askopenfilename(filetypes = [('GIF', '*.gif')])
        self.exercise_image_filename.set(tmp)
        self.exercise_image = PhotoImage(file = self.exercise_image_filename.get(), width=390, height=200)
        self.button05['image'] = self.exercise_image
        self.button05.image = self.exercise_image
                
############################################################## EXCERCISE END ###
############################################################### BODYPARTS ######
class BodyParts(Frame):
    '''Widget body parts. Shows human body for choosing particular body part from. '''
    def __init__(self, vc, frame, bp_IDs, mode):
        Frame.__init__(self, frame)
        self.vc = vc
        self.mode = mode
        self.grid()
        self.bp_IDs = bp_IDs
        self.body_part_ID_selected = None  # selected body part by pressing body part button
        img_path = 'components/img/body/'
        canv = Canvas(self, width = 220, height = 500)
        canv.grid()

        img_00 = PhotoImage(file = img_path + 'body_new.gif')
        body = Label(canv, image = img_00, width = 200, height = 500)
        body.image = img_00
        body.place(x = 10, y = 10)

        img_02 = PhotoImage(file = img_path + 'shoulder_58x50.gif')
        schoulder = Button(self, image = img_02, width = 48-10, height = 50-10, activebackground = 'blue')
        schoulder.config(command = lambda a = self.bp_IDs[0]: self.set_body_part_ID(a))
        schoulder.image = img_02
        schoulder.place(x = 20, y = 65+10)

        img_03 = PhotoImage(file = img_path + 'biceps_58x50.gif')
        biceps = Button(self, image = img_03, width = 48-10, height = 50-10, activebackground = 'blue')
        biceps.config(command = lambda a = self.bp_IDs[1]: self.set_body_part_ID(a))
        biceps.image = img_03
        biceps.place(x = 20, y = 10+65+50)

        img_04 = PhotoImage(file = img_path + 'chest_47x50.gif')
        chest = Button(self, image = img_04, width = 47-10, height = 50-10, activebackground = 'blue')
        chest.config(command = lambda a = self.bp_IDs[2]: self.set_body_part_ID(a))
        chest.image = img_04
        chest.place(x = 10+58, y = 10+65+25)

        img_05 = PhotoImage(file = img_path + 'abs_47x75.gif')
        abs_1 = Button(self, image = img_05, width = 47-10, height = 75-10, activebackground = 'blue')
        abs_1.config(command = lambda a = self.bp_IDs[3]: self.set_body_part_ID(a))
        abs_1.image = img_05
        abs_1.place(x = 10+58, y = 10+65+25+50)

        img_06 = PhotoImage(file = img_path + 'quads_47x85.gif')
        quads = Button(self, image = img_06, width = 47-10, height = 85-10, activebackground = 'blue')
        quads.config(command = lambda a = self.bp_IDs[4]: self.set_body_part_ID(a))
        quads.image = img_06
        quads.place(x = 10+58, y = 10+65+25+50+50+75)

        img_07 = PhotoImage(file = img_path + 'Triceps_50x75.gif')
        triceps = Button(self, image = img_07, width = 50-20, height = 75-10, activebackground = 'blue')
        triceps.config(command = lambda a = self.bp_IDs[5]: self.set_body_part_ID(a))
        triceps.image = img_07
        triceps.place(x = 10+150, y = 10+90)

        img_08 = PhotoImage(file = img_path + 'Glutes_45x50.gif')
        glutes = Button(self, image = img_08, width = 45-10, height = 50-10, activebackground = 'blue')
        glutes.config(command = lambda a = self.bp_IDs[6]: self.set_body_part_ID(a))
        glutes.image = img_08
        glutes.place(x = 10+58+47, y = 10+65+25+50+75)

        img_09 = PhotoImage(file = img_path + 'Hamstrings_45x85.gif')
        hams = Button(self, image = img_09, width = 45-10, height = 85-10, activebackground = 'blue')
        hams.config(command = lambda a = self.bp_IDs[7]: self.set_body_part_ID(a))
        hams.image = img_09
        hams.place(x = 10+58+47, y = 10+65+25+50+75+50)

        img_10 = PhotoImage(file = img_path + 'calves_45x150.gif')
        calves = Button(self, image = img_10, width = 45-10, height = 150-70, activebackground = 'blue')
        calves.config(command = lambda a = self.bp_IDs[8]: self.set_body_part_ID(a))
        calves.image = img_10
        calves.place(x = 10+58+47, y = 10+65+25+50+75+50+85)

        img_11 = PhotoImage(file = img_path + 'back_45x125.gif')
        back = Button(self, image = img_11, width = 45-10, height = 125-10, activebackground = 'blue')
        back.config(command = lambda a = self.bp_IDs[9]: self.set_body_part_ID(a))
        back.image = img_11
        back.place(x = 10+58+47, y = 10+65+25)

        others = Button(self, text = 'o\nt\nh\ne\nr\ns', width = 1, height = 6, bg = 'white', activebackground = 'grey90')
        others.config(command = lambda a = self.bp_IDs[10]: self.set_body_part_ID(a))
        others.place(x = 10+160, y = 10+65+25+50+50+75+115)

      # b000 - exit button           
        self.b000 = Button(self,
                    bd = 0,
                    text = '______exit______',
                    fg = 'Red',
                    activeforeground='Black',
                    font = ('Courier', 10),
                    command = self.vc._exit_on_new_workout_delegate)
        self.b000.grid(sticky = S + E)
        
    def set_body_part_ID(self, body_part_ID):
        '''stores selected body part ID.'''
        if self.mode == 'new_workout':
            self.vc._body_part_selected_nw(body_part_ID)
        elif self.mode == 'new_exercise':
            self.vc._body_part_selected_ne(body_part_ID)
        elif self.mode == 'edit_exercise':
            self.vc._body_part_selected_ee(body_part_ID)
    
############################################################### BODYPARTS END###
############################################################### CARTVIEW #######
class CartView(Frame):
    '''Widget cart view. Shows a list of exercises choosed for the next gym session.'''
    def __init__(self, vc, frame, cart):
        Frame.__init__(self, frame)
        self.vc = vc
        self.grid(sticky = N + W)
        self.cart = cart
        bo_key = None
        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_cart_viewX_delegate) # Exit action when x (top right corner) pressed
        cart_label_frame = LabelFrame(self, font = ('Courier', 10, 'normal', 'italic'), text = 'Exercises cart')
        cart_label_frame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = N + W)
        form_button = Button(self, text = 'form', command = self.vc._form)
        form_button.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = W + E)
        clear_button = Button(self, text = 'clear', command = self.vc._clear_cart)
        clear_button. grid(row = 1, column = 1, padx = 10, pady = 5, sticky = W + E)
        close_button = Button(self, text = 'close', command = self.vc._exit_on_cart_viewX_delegate)
        close_button.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = W + E)
        if len(self.cart) == 0:
            Label(cart_label_frame, font = ('Courier', 10), fg = 'red', text = 'The cart is empty___________________').grid(ipadx = 10, sticky = W)
        else:
            for record in self.cart:
                ex_key = record[1]
                if bo_key != record[0]:
                    bo_key = record[0]
                    t1_tmp = self.vc.model._get_body_part_name(bo_key)
                    t1_tmp = t1_tmp + (35 - len(t1_tmp))*'_'
                    t2_tmp = self.vc.model._get_exercise_name(ex_key)
                    t2_tmp = '   ' + t2_tmp + (33 - len(t2_tmp))*'_'                
                    Label(cart_label_frame, font = ('Courier', 10), text = t1_tmp).grid(ipadx = 10, sticky = W)
                    Label(cart_label_frame, font = ('Courier', 10), text = t2_tmp).grid(ipadx = 10, sticky = W)
                else:
                    t2_tmp = self.vc.model._get_exercise_name(ex_key)
                    t2_tmp = '   ' + t2_tmp + (33 - len(t2_tmp))*'_' 
                    Label(cart_label_frame, font = ('Courier', 10), text = t2_tmp).grid(ipadx = 10, sticky = W)
             
############################################################## CARTVIEW END ####
############################################################### WPLVIEW #######
class WPLView(Frame):
    '''Widget Workout Plan List view. Shows a list of workout plans stored in database.'''
    def __init__(self, vc, frame, mode):
        Frame.__init__(self, frame)
        self.vc = vc
        self.workout_plans_list = self.vc.model._get_workout_list_IDs()
        self.mode = mode
        self.grid()
        self.body = Frame(self, bg = 'grey90')
        self.body.grid(padx = 10, pady = 10)
        self.commands = Frame(self, bg = 'grey90')
        self.commands.grid(padx = 10, pady = 1, sticky = E)
        self.f_b = tkFont.Font(family = 'Courier', size = 9)

        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_WPL_view_delegate) # Exit action when x (top right corner) pressed

        self.lb = Listbox(self.body, bd = 0, font = self.f_b, width = 30)
        self.lb.grid()
        for i, wp_id in enumerate(self.workout_plans_list):
            wp_text = ' ' + wp_id + ': ' + self.vc.model._get_workout_plan_name(wp_id)
            self.lb.insert(END, wp_text)
            

        close_button = Button(self.commands, font = self.f_b, text = 'close', command = self.vc._exit_on_WPL_view_delegate)
        close_button.grid(row = 0, column = 1, sticky = N+E)
        select_button = Button(self.commands, font = self.f_b, text = 'select', command = self._select)
        select_button.grid(row = 0, column = 0, sticky = N+E)

    def _select(self):
        index = int(self.lb.curselection()[0]) 
        self.vc._workout_plan(self.workout_plans_list[index])
             
############################################################## WPLVIEW END ####
############################################################### CALVIEW #######
class CalView(Frame):
    '''Calendar widget.'''
    def __init__(self, vc, frame, scale = 'BIG', mode = 'LOAD'):
        Frame.__init__(self, frame)
        self.vc = vc
        self.scale = scale
        self.mode = mode # possible modes: 'LOAD', 'SET'
        self.grid()
        self.f1 = Frame(self)
        self.f2 = Frame(self)
        self.f3 = Frame(self)
        self.f1.grid(row = 0)
        self.f2.grid(row = 1)
        self.f3.grid(row = 2)
        
        frame.protocol('WM_DELETE_WINDOW', self.vc._exit_on_CV_view_delegate) # Exit action when x (top right corner) pressed

        today = localtime(time())
        self.currentYear = today.tm_year
        self.year = self.currentYear
        self.currentMonth  = today.tm_mon
        self.month = self.currentMonth
        self.currentDay = today.tm_mday
        self.day = self.currentDay

        self.months = {1: 'Jan',
                       2: 'Feb',
                       3: 'Mar',
                       4: 'Apr',
                       5: 'May',
                       6: 'Jun',
                       7: 'Jul',
                       8: 'Aug',
                       9: 'Sep',
                       10: 'Oct',
                       11: 'Nov',
                       12: 'Dec'}

        if self.scale == 'BIG':
            self.size = (11, 8, 4) # self.size[0] - days label width
                                   # self.size[1] - calendar button width
                                   # self.size[2] - calendar button height
        elif self.scale == 'SMALL':
            self.size = (5, 2, 1) # self.size[0] - days label width
                                   # self.size[1] - calendar button width
                                   # self.size[2] - calendar button height
            
        self.data_dates = self.vc.model._get_data_dates()
#----------------------------------------------------------------------        
        self.makeCalendar()
        self.drawCalendar()        

    def makeCalendar(self):
        self.yearVar = IntVar()
        self.yearVar.set(self.year)
        self.monthVar = IntVar()
        self.monthVar.set(self.months[self.month])        

# ------ draws year and associated buttons -----------
        yearLabel = Label(self.f1, textvariable = self.yearVar)
        leftButton1 = Button(self.f1, text = '<<', width = self.size[1], command = self.yearMinus)
        rightButton1 = Button(self.f1, text = '>>', width = self.size[1], command = self.yearPlus)
        leftButton1.grid(row = 0, column = 0, sticky=W)
        yearLabel.grid(row = 0, column = 3)
        rightButton1.grid(row = 0, column = 6, sticky=E)
        
# ------ draws month and associated buttons -----------        
        monthLabel = Label(self.f1, textvariable = self.monthVar)
        leftButton2 = Button(self.f1, text = ' <', width = self.size[1], command = self.monthMinus)
        rightButton2 = Button(self.f1, text = '> ', width = self.size[1], command = self.monthPlus)
        leftButton2.grid(row = 1, column = 0, sticky=W)        
        monthLabel.grid(row = 1, column = 3)
        rightButton2.grid(row = 1, column = 6, sticky=E)
# ------ draws line with day names -----------
        Mon = Button(self.f1, text = 'Mon', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Mon.grid(row = 2, column = 0)
        Tue = Button(self.f1, text = 'Tue', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Tue.grid(row = 2, column = 1)
        Wed = Button(self.f1, text = 'Wed', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Wed.grid(row = 2, column = 2)
        Thr = Button(self.f1, text = 'Thr', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Thr.grid(row = 2, column = 3)
        Fri = Button(self.f1, text = 'Fri', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Fri.grid(row = 2, column = 4)
        Sat = Button(self.f1, text = 'Sat', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Sat.grid(row = 2, column = 5)
        Sun = Button(self.f1, text = 'Sun', width = self.size[1], bg = 'grey',
                     state = 'disabled', disabledforeground = 'white')
        Sun.grid(row = 2, column = 6)

    def monthPlus(self):
        '''increase month, redraw current month'''
        self.f3.destroy()
        a = self.month + 1
        if a == 13:
            self.month = 1
        else:
            self.month = a
        self.monthVar.set(self.months[self.month])
        self.f3 = Frame(self)
        self.f3.grid(row = 3)
        self.drawCalendar()

    def monthMinus(self):
        '''decrease month, redraw current month'''
        self.f3.destroy()
        a = self.month - 1
        if a == 0:
            self.month = 12
        else:
            self.month = a
        self.monthVar.set(self.months[self.month])
        self.f3 = Frame(self)
        self.f3.grid(row = 3)        
        self.drawCalendar()

    def yearPlus(self):
        '''increase year, redraw current month'''
        self.f3.destroy()
        self.year += 1
        self.yearVar.set(self.year)
        self.f3 = Frame(self)
        self.f3.grid(row = 3)
        self.drawCalendar()

    def yearMinus(self):
        '''decrease year, redraw current month'''
        self.f3.destroy()
        self.year -= 1
        self.yearVar.set(self.year)
        self.f3 = Frame(self)
        self.f3.grid(row = 3)
        self.drawCalendar()        

    def drawCalendar(self):
        '''draw a calendar'''
        buttons_param = []
        dayVar = StringVar()
        mon = monthcalendar(self.year, self.month)

        for i in range(len(mon)):
            for j, k in enumerate(mon[i]):
                day = str(k)
                buttons_param.append([day,i,j])

        b = []
        for j, i in enumerate(buttons_param):
            b.append(Button(self.f3, width = self.size[1], height = self.size[2], text = i[0], activeforeground = 'white'))
            b[j].config(command = lambda a = i[0]: self.getDay(a))
# ---------- Saturdays and Sundays set to red color --------------------            
            if i[2] == 6 or i[2] == 5:
                b[j].config(fg = 'red')
# ---------- actual day set to yellow background color --------------------
            if i[0] == str(self.day) and self.month == self.currentMonth and self.year == self.currentYear:
                b[j].config(bg = 'yellow')
# ---------- blank day of the month set to disabled state and white background color------------                
            if i[0] == '0':
                b[j].config(state = 'disabled', text = '', bg = 'white')
            if self._data_encode(self.month, i[0], self.year) in self.data_dates:
                b[j].config(text = '*'+i[0]+'*')
            b[j].grid(row = i[1], column = i[2])

    def _data_encode(self, month, day, year):
        '''changes month, day , year to form YYYYMMDD '''
        m = '{0:0{width}}'.format(month, width=2)
        d = '{0:0{width}}'.format(int(day), width=2)
        y = str(year)
        return y+m+d
        
    def getDay(self, a):
        '''returns choosed day as CAL_ID (e.g. 20141211 = 11/12/2014).'''
        CAL_ID = self._data_encode(self.month, a, self.year)
        if self.mode == 'SET':
            self.vc.view.wf_draft.set_date(CAL_ID)
            self.vc.view.wf_draft.AccB.grid_remove()
            self.vc.view.wf_draft.SCaB.grid()
        elif self.mode == 'LOAD':
            if CAL_ID in self.data_dates:
                self.vc._workout_from_cal(CAL_ID)
            else:
                self.vc.view.status_line.set('There is no workout under this date: ' + CAL_ID, 'red')
        return CAL_ID
############################################################## CALVIEW END ####        

                    
class FormBodyLabel(Label):
    def __init__(self, parent):
        Label.__init__(self, parent)
        font_label = tkFont.Font(family = 'Courier', size = 9)
        self.config(font = font_label,
                    padx = 2,
                    bg = 'grey80',
                    anchor = E)
        
class FormBodyEntry(Entry):
    def __init__(self, parent):
        Entry.__init__(self, parent)
        font_label = tkFont.Font(family = 'Courier', size = 9)
        self.config(font = font_label,
                    bg = 'white',
                    justify = RIGHT,
                    width = 5)

class FormBodyButton(Button):
    def __init__(self, parent):
        Button.__init__(self, parent)
        font_label = tkFont.Font(family = 'Courier', size = 8)
        self.config(font = font_label,
                    height = 1,
                    bg = 'grey80')
    
############################################################### FORMVIEW #####
class FormDraftView(Frame):
    '''Widget 'FormDraftView'. Shows a form for particular cart and fields to be filled out. '''
    def __init__(self, vc, frame, mode, wo_id = None, cal_id = None):
        Frame.__init__(self, frame)
        self.vc = vc
        self.mode = mode
        self.grid()
        
        self.head = Frame(self)
        self.head.grid(padx = 10, sticky = W)
        self.body = Frame(self, bg = 'grey90')
        self.body.grid(padx = 10, pady = 10)
        self.commands = Frame(self, bg = 'grey90')
        self.commands.grid(padx = 10, pady = 1, sticky = E)

        self.f_h = tkFont.Font(family = 'Courier', size = 10)
        self.f_l = tkFont.Font(family = 'Courier', size = 9, weight = 'bold')
        self.f_b = tkFont.Font(family = 'Courier', size = 9)        

        self.ExiB = Button(self.commands, text = 'exit form', font = self.f_b, command = self.vc._exit_on_form_view_delegate)
        self.ExiB.grid(row = 0, column = 2, sticky = N+E)
        self.AccB = Button(self.commands, text = 'accept', font = self.f_b, command = self.accept_plan)
        self.AccB.grid(row = 0, column = 1, sticky = N+E)
        self.SCaB = Button(self.commands, text = 'save to calendar', font = self.f_b, command = self.save_workout_to_cal)
        self.SCaB.grid(row = 0, column = 1, sticky = N+E)
        self.SCaB.grid_remove()
        self.DelB = Button(self.commands, text = 'delete', font = self.f_b, command = self.delete_plan)
        self.DelB.grid(row = 0, column = 0, sticky = N+E)        

        if self.mode == 'NEW':
            self.plan = self.vc.workout_plan.get_workout_plan()
        elif self.mode == 'LOAD':
            self.wo_id = wo_id
            self.plan = self.vc.model._get_WOplan(self.wo_id)
        elif self.mode == 'LOAD CAL':
            self.wo_id = wo_id
            self.plan = self.vc.model._get_WO_from_cal(cal_id)
            self.AccB.grid_remove()
            self.SCaB.grid()
            

        self.plan_list = list(self.plan)
        self.plan_list.sort()

        self.initialize_control_variables()        
        self.make_header()
        self.make_headline()
        self.make_data_view()

    def set_date(self, date):
        self.wo_date.set(date)
    
    def initialize_control_variables(self):
        
        self.wo_name = StringVar()
        self.wo_name.set(self.plan[self.plan_list[0]]['WO_NAME'])
        self.wo_date = StringVar()
        self.wo_date.set(self.plan[self.plan_list[0]]['WO_DATE'])

        self.ex_sets =     [StringVar() for i in range(len(self.plan))]
        self.ex_reps_0 =   [StringVar() for i in range(len(self.plan))]
        self.ex_reps_1 =   [StringVar() for i in range(len(self.plan))]
        self.ex_weigth_0 = [StringVar() for i in range(len(self.plan))]
        self.ex_weigth_1 = [StringVar() for i in range(len(self.plan))]
        self.ex_level_0 =  [StringVar() for i in range(len(self.plan))]
        self.ex_level_1 =  [StringVar() for i in range(len(self.plan))]
        self.ex_time_0 =   [StringVar() for i in range(len(self.plan))]
        self.ex_time_1 =   [StringVar() for i in range(len(self.plan))]
        self.ex_rest_0 =   [StringVar() for i in range(len(self.plan))]
        self.ex_rest_1 =   [StringVar() for i in range(len(self.plan))]
        

    def make_header(self):
        self.wo_id_label_01 = Label(self.head, font = self.f_h, text = 'Workout ID: ').grid(row = 0, column = 0, sticky = W)
        self.wo_id_label_02 = Label(self.head, font = self.f_h, text = self.plan[self.plan_list[0]]['WO_ID']).grid(row = 0, column = 1, sticky = W)
        self.wo_name_label = Label(self.head, font = self.f_h, text = 'Workout name: ').grid(row = 1, column = 0, sticky = W)
        self.wo_name_entry = Entry(self.head, font = self.f_h, textvariable = self.wo_name).grid(row = 1, column = 1, sticky = W)
        self.wo_date_label = Label(self.head, font = self.f_h, text = 'Workout date: ').grid(row = 2, column = 0, sticky = W)
        self.wo_date_entry = Entry(self.head, font = self.f_h, textvariable = self.wo_date).grid(row = 2, column = 1, sticky = W)
        self.schedule = Button(self.head, text = 'schedule', font = self.f_b, command = self.schedule_plan).grid(row = 2, column = 2, sticky = W)

    def make_headline(self):
        Label(self.body, font = self.f_l, text = 'Body part', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 1, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Ex name', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 3, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Sets', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 4, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Reps', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 5, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Weigth', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 6, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Level', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 7, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Time', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 8, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Rest', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 9, sticky = W+E)
        Label(self.body, font = self.f_l, text = 'Status', fg = 'white', bg = 'grey', padx = 1).grid(padx = 1, row = 0, column = 10, sticky = W+E)

    def make_data_view(self):
        i = 0
        r = 1
        for ex_no in self.plan_list:
            a = FormBodyLabel(self.body)
            a.config(text = self.plan[ex_no]['BO_NAME'])
            a.grid(row = r, column = 1, padx = 1, sticky = W+E)
            
            b = FormBodyLabel(self.body)
            b.config(text = self.plan[ex_no]['EX_NAME'])
            b.grid(row = r, column = 3, padx = 1, sticky = W+E)
            
            self.ex_sets[i].set(str(self.plan[ex_no]['EX_SETS']))
            c = FormBodyEntry(self.body)
            c.config(textvariable = self.ex_sets[i])
            c.grid(row = r, column = 4, sticky = W+E)
            
            self.ex_reps_0[i].set(str(self.plan[ex_no]['EX_REPS'][0]))
            d0 = FormBodyEntry(self.body)
            d0.config(textvariable = self.ex_reps_0[i])
            d0.grid(row = r, column = 5, sticky = W+E)
            
            self.ex_reps_1[i].set(str(self.plan[ex_no]['EX_REPS'][1]))
            d1 = FormBodyEntry(self.body)
            d1.config(textvariable = self.ex_reps_1[i])
            d1.grid(row = r + 1, column = 5, sticky = W+E)
            
            self.ex_weigth_0[i].set(str(self.plan[ex_no]['EX_WEIGTH'][0]))
            e0 = FormBodyEntry(self.body)
            e0.config(textvariable = self.ex_weigth_0[i])
            e0.grid(row = r, column = 6, sticky = W+E)

            self.ex_weigth_1[i].set(str(self.plan[ex_no]['EX_WEIGTH'][1]))
            e1 = FormBodyEntry(self.body)
            e1.config(textvariable = self.ex_weigth_1[i])
            e1.grid(row = r + 1, column = 6, sticky = W+E)

            self.ex_level_0[i].set(str(self.plan[ex_no]['EX_LEVEL'][0]))
            f0 = FormBodyEntry(self.body)
            f0.config(textvariable = self.ex_level_0[i])
            f0.grid(row = r, column = 7, sticky = W+E)

            self.ex_level_1[i].set(str(self.plan[ex_no]['EX_LEVEL'][1]))
            f1 = FormBodyEntry(self.body)
            f1.config(textvariable = self.ex_level_1[i])
            f1.grid(row = r + 1, column = 7, sticky = W+E)
            
            self.ex_time_0[i].set(str(self.plan[ex_no]['EX_TIME'][0]))
            g0 = FormBodyEntry(self.body)
            g0.config(textvariable = self.ex_time_0[i])
            g0.grid(row = r, column = 8, sticky = W+E)

            self.ex_time_1[i].set(str(self.plan[ex_no]['EX_TIME'][1]))
            g1 = FormBodyEntry(self.body)
            g1.config(textvariable = self.ex_time_1[i])
            g1.grid(row = r + 1, column = 8, sticky = W+E)

            self.ex_rest_0[i].set(str(self.plan[ex_no]['EX_REST'][0]))
            h0 = FormBodyEntry(self.body)
            h0.config(textvariable = self.ex_rest_0[i])
            h0.grid(row = r, column = 9, sticky = W+E)

            self.ex_rest_1[i].set(str(self.plan[ex_no]['EX_REST'][1]))
            h1 = FormBodyEntry(self.body)
            h1.config(textvariable = self.ex_rest_1[i])
            h1.grid(row = r + 1, column = 9, sticky = W+E)

            j0 = FormBodyLabel(self.body)
            j0.config(text = self.plan[ex_no]['EX_STATUS'][0])
            j0.grid(row = r, column = 10, padx = 1, sticky = W+E)

            j1 = FormBodyLabel(self.body)
            j1.config(text = self.plan[ex_no]['EX_STATUS'][1])
            j1.grid(row = r + 1, column = 10, padx = 1, sticky = W+E)

            r += 2
            i += 1


    def accept_plan(self):
        '''accepts and saves workout plan into database'''
        for i, ex_no in enumerate(self.plan_list):
            self.plan[ex_no] = {'WO_ID'       : self.plan[self.plan_list[0]]['WO_ID'],  # ok
                                'WO_NAME'     : self.wo_name.get(),                     # ok
                                'WO_DATE'     : self.wo_date.get(),                     # ok
                                'EX_NO'       : ex_no,                                                  # ok
                                'BO_ID'       : self.plan[ex_no]['BO_ID'],                              # ok
                                'BO_NAME'     : self.plan[ex_no]['BO_NAME'],                            # ok
                                'EX_ID'       : self.plan[ex_no]['EX_ID'],                              # ok
                                'EX_NAME'     : self.plan[ex_no]['EX_NAME'],                            # ok
                                'EX_SETS'     : self.ex_sets[i].get(),                                  # ok
                                'EX_REPS'     : [self.ex_reps_0[i].get(), self.ex_reps_1[i].get()],     # ok
                                'EX_WEIGTH'   : [self.ex_weigth_0[i].get(), self.ex_weigth_1[i].get()], # ok
                                'EX_LEVEL'    : [self.ex_level_0[i].get(), self.ex_level_1[i].get()],   # ok
                                'EX_TIME'     : [self.ex_time_0[i].get(), self.ex_time_1[i].get()],     # ok
                                'EX_REST'     : [self.ex_rest_0[i].get(), self.ex_rest_1[i].get()],     # ok
                                'EX_STATUS'   : [self.plan[ex_no]['EX_STATUS'][0], self.plan[ex_no]['EX_STATUS'][1]] }# ok
        self.vc._save_workout_plan(self.plan[self.plan_list[0]]['WO_ID'], self.plan)

    def save_workout_to_cal(self):
        '''saves workout to calendar database '''
        for i, ex_no in enumerate(self.plan_list):
            self.plan[ex_no] = {'WO_ID'       : self.plan[self.plan_list[0]]['WO_ID'],  # ok
                                'WO_NAME'     : self.wo_name.get(),                     # ok
                                'WO_DATE'     : self.wo_date.get(),                     # ok
                                'EX_NO'       : ex_no,                                                  # ok
                                'BO_ID'       : self.plan[ex_no]['BO_ID'],                              # ok
                                'BO_NAME'     : self.plan[ex_no]['BO_NAME'],                            # ok
                                'EX_ID'       : self.plan[ex_no]['EX_ID'],                              # ok
                                'EX_NAME'     : self.plan[ex_no]['EX_NAME'],                            # ok
                                'EX_SETS'     : self.ex_sets[i].get(),                                  # ok
                                'EX_REPS'     : [self.ex_reps_0[i].get(), self.ex_reps_1[i].get()],     # ok
                                'EX_WEIGTH'   : [self.ex_weigth_0[i].get(), self.ex_weigth_1[i].get()], # ok
                                'EX_LEVEL'    : [self.ex_level_0[i].get(), self.ex_level_1[i].get()],   # ok
                                'EX_TIME'     : [self.ex_time_0[i].get(), self.ex_time_1[i].get()],     # ok
                                'EX_REST'     : [self.ex_rest_0[i].get(), self.ex_rest_1[i].get()],     # ok
                                'EX_STATUS'   : [self.plan[ex_no]['EX_STATUS'][0], self.plan[ex_no]['EX_STATUS'][1]] }# ok        
        self.vc._save_workout_to_calendar(self.wo_date.get(), self.plan)

    def delete_plan(self):
        '''deletes plan from database'''
        self.vc._delete_wo_plan(self.plan[self.plan_list[0]]['WO_ID'])
        
    def schedule_plan(self):
        '''shows mini calendar on screen'''
        self.vc._calendar('SMALL', 'SET')


############################################################### FORMVIEW END##
################################################################# FORM #######
class WorkoutPlan:
    '''This object creates and keeps information about planned workout session.'''
    def __init__(self, vc, mode):
        self.vc = vc
        self.mode = mode
        if self.mode == 'NEW':
            self._new()
        elif self.mode == 'LOAD':
            self.workout_plan = workout_plan  # here put db['WO_PLAN'][WO_ID]

    def _new(self):
        self.cart_list = self.vc.model.cart.get_content()
        self.workout_plan = {}
        self.WO_ID = self.vc.model._get_new_workout_ID()
        self.WO_NAME = 'input workout name'
        self.WO_DATE = None
        for i, cc in enumerate(self.cart_list):
            self.ex_no = (i + 1) * 10                                # exercise number
            self.bo_id = cc[0]                                       # body part ID
            self.bo_name = self.vc.model._get_body_part_name(self.bo_id) # body part name
            self.ex_id = cc[1]                                       # exercise ID
            self.ex_name = self.vc.model._get_exercise_name(self.ex_id)   # exercise name
            self.ex_sets = 1                                         # exercise sets (default = 1)
            self.ex_reps_0 = 0                                       # planned exercise repetitions
            self.ex_reps_1 = 0                                       # accomplished exercise repetitions
            self.ex_weigth_0 = 0                                     # planned weigth used by doing exercise
            self.ex_weigth_1 = 0                                     # actual weigth used by doing exercise            
            self.ex_level_0 = 0                                      # planned level of resistance by doing exercise
            self.ex_level_1 = 0                                      # accomplished level of resistance by doing exercise
            self.ex_time_0 = 0                                       # planned exercise duration, if applicable [s]
            self.ex_time_1 = 0                                       # actual exercise duration, if applicable [s]
            self.ex_rest_0 = 0                                       # planned rest time between exercises or sets [s]
            self.ex_rest_1 = 0                                       # actual rest time between exercises or sets [s]
            self.ex_status_0 = 'plan'                                # if exercise status is PLAN
            self.ex_status_1 = 'done'                                # if exercise status is PLAN
            
            self.workout_plan[self.ex_no] = {'WO_ID'       : self.WO_ID,
                                             'WO_NAME'     : self.WO_NAME,
                                             'WO_DATE'     : self.WO_DATE,
                                             'EX_NO'       : self.ex_no,
                                             'BO_ID'       : self.bo_id,
                                             'BO_NAME'     : self.bo_name,
                                             'EX_ID'       : self.ex_id,
                                             'EX_NAME'     : self.ex_name,
                                             'EX_SETS'     : self.ex_sets,
                                             'EX_REPS'     : [self.ex_reps_0, self.ex_reps_1],
                                             'EX_WEIGTH'   : [self.ex_weigth_0, self.ex_weigth_1],
                                             'EX_LEVEL'    : [self.ex_level_0, self.ex_level_1],
                                             'EX_TIME'     : [self.ex_time_0, self.ex_time_1], 
                                             'EX_REST'     : [self.ex_rest_0, self.ex_rest_1],
                                             'EX_STATUS'   : [self.ex_status_0, self.ex_status_1] }

       
    def get_workout_plan(self):
        return self.workout_plan

    def set_workout_plan_data(self, ex_no, element):
        self.workout_plan[ex_no] = element
        
################################################################# FORM END ###

################################################################# EXCART #######
class ExCart:
    '''This object keeps choosen excercises in a 'cart' for later operations
       like saving or editing'''
    def __init__(self):
        self.cart = []

    def add_exercise(self, EX):
        '''adds excercise to the cart'''
        if not EX in self.cart:
            self.cart.append(EX)
            self.cart.sort()

    def remove_exercise(self, EX):
        '''removes excercise from cart'''
        if EX in self.cart:
            self.cart.remove(EX)

    def get_content(self):
        '''returns what does the cart contain so far'''
        return self.cart

    def is_empty(self):
        return len(self.cart) == 0

    def clear_cart(self):
        self.cart = []
################################################################# EXCART END ###
############################################################### SEMAPHORE ######
class Semaphore:
    '''This object remembers if particular frame is occupied or free. '''
    def __init__(self, frame = None):
        self.up()
        self.frame = frame
        self.stack = []

    def up(self):
        self.state = True

    def down(self):
        self.state = False
        
    def get_state(self):
        return self.state

    def set_frame(self, frame):
        self.frame = frame

    def get_frame(self):
        return self.frame
############################################################### SEMAPHORE END###
############################################################### STACK ##########
class WinStack:
    '''This object remembers a sequence of opened windows/frames. Used for managing
       if more then one frame is open in command sequence.'''
    def __init__(self):
        self.stack = []

    def push(self, widget):
        self.stack.append(widget)

    def top(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None

    def is_empty(self):
        if len(self.stack):
            return False
        else:
            return True
    def get_stack(self):
        return self.stack

    def __len__(self):
        return len(self.stack)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.stack.pop()
############################################################### STACK END ######
