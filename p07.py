#!/usr/bin/python3

#Szymon Nowosielski
#James Livulpi
#Employing MVC model

#################################################################################

#This program will allow you to create a workout plan and explore different
#options on how to workout, as well as plan out days in which you would like
#to workout on. Done in a semester for software engineering 2

#################################################################################

from tkinter import *
import shelve
from workout import *

############################################################### CONTROLLER ######
class Controller():
    def __init__(self, parent):
        self.root = parent
        self.model = Model(self)
        self.view = View(self, self.root)

    def foo(self):
        self.view.status_line.set('foo')

    def new_exercise(self):
        '''create new exercise and store it into database'''
        body_parts_list_IDs = self.model._get_body_parts_list_IDs()
        self.view._show_body_parts(body_parts_list_IDs, 'new_exercise')

    def _body_part_selected_ne(self, BP_ID):
        EX_ID = self.model._getNewExID(BP_ID)
        self.view._show_exercise_record(BP_ID, EX_ID, 'new_exercise')

    def edit_exercise(self):
        '''edit exercise and changes store it into database'''
        body_parts_list_IDs = self.model._get_body_parts_list_IDs()
        self.view._show_body_parts(body_parts_list_IDs, 'edit_exercise')

    def _body_part_selected_ee(self, BP_ID):
        excercises_list_IDs = self.model._get_exercises_list_IDs(BP_ID)
        self.view._show_excercises(BP_ID, excercises_list_IDs, 'edit_exercise')

    def _exercise_delete(self, BO_ID, EX_ID):
        '''deletes exercise from database'''
        self.model._deleteEX(BO_ID, EX_ID)
        self.view.status_line.set('Exercise ' + EX_ID + ' has been deletetd', 'red')
        self._exit_on_new_workout_delegate()
        self.edit_exercise()
        self._body_part_selected_ee(BO_ID)

    def _delete_wo_plan(self, WO_ID):
        '''deletes workout plan WO_ID from database '''
        self.model._deleteWO_plan(WO_ID)
        self.view.status_line.set('Workout plan ' + WO_ID + ' has been deletetd', 'red')
        self._exit_on_new_workout_delegate()
        
    def _exercise_save(self, BO_ID, EX_ID, EX_NAME, EX_INFO, EX_IMG):
        '''saves exercise into database'''
        self.model._saveEX(BO_ID, EX_ID, EX_NAME, EX_INFO, EX_IMG)
        self.view.status_line.set('Exercise ' + EX_ID + ' has been saved', 'red')
        self.view._exit_on_exercise_view()

    def new_workout(self):
        '''new workout plan'''
        body_parts_list_IDs = self.model._get_body_parts_list_IDs()
        self.view._show_body_parts(body_parts_list_IDs, 'new_workout')

    def _save_workout_plan(self, wo_id, workout_plan_record):
        '''save workout_plan into database'''
        self.model._saveWOplan(wo_id, workout_plan_record)
        self.view.status_line.set('Workout plan ' + wo_id + ' has been saved into database', 'red')
        self._exit_on_form_view_delegate()

    def _save_workout_to_calendar(self, cal_id, workout_record):
        '''save workout into calendar database'''
        self.model._saveWO_to_cal(cal_id, workout_record)
        self.view.status_line.set('Workout has been saved into calendar', 'red')
        self._exit_on_form_view_delegate()

    def _load_workout_plan(self):
        '''loads workout plans from database'''
        self.view._show_workout_plans_list('LOAD')

    def _calendar(self, scale = 'BIG', mode = 'LOAD'):
        '''shows calendar'''
        self.view._show_calendar(scale, mode)
        if mode == 'LOAD':
            self.view.status_line.set('Choose date with "*" to load workout', 'red')

    def _exit_on_CV_view_delegate(self):
        self.view._exit_on_calendar()
        
    def _body_part_selected_nw(self, BP_ID):
        excercises_list_IDs = self.model._get_exercises_list_IDs(BP_ID)
        self.view._show_excercises(BP_ID, excercises_list_IDs, 'new_workout')

    def _exercise_selected(self, BO_ID, EX_ID, index):
        '''adds/removes exercises to/from cart '''
        state = self.state_1[index].get()
        if state:                                            # if exercise selected
            self.model.cart.add_exercise([BO_ID, EX_ID])     # add it to current cart
        else:                                                # if deselected
            self.model.cart.remove_exercise([BO_ID, EX_ID])  # remove it from cart
        self._cart_record()

    def _exercise_record(self, BP_ID, EX_ID, mode):
        '''shows exercise record '''
        self.view._show_exercise_record(BP_ID, EX_ID, mode)

    def _cart_record(self):
        actual_cart = self.model.cart.get_content()
        self.view._show_cart_view(actual_cart)

    def _clear_cart(self):
        '''makes exercise cart empty'''
        self.model.cart.clear_cart()
        self._cart_record()
        if not self.view.sema_01.get_state():
            self.view._exit_on_new_workout()
            self.new_workout()

    def _exit_on_new_workout_delegate(self):
        self.view._exit_on_new_workout()

    def _exit_on_exercise_view_delegate(self):
        self.view._exit_on_exercise_view()

    def _exit_on_cart_viewX_delegate(self):
        self.view._exit_on_cart_viewX()

    def _exit_on_WPL_view_delegate(self):
        self.view._exit_on_WPL_view()

    def _exit_on_form_view_delegate(self):
        self.view._exit_on_form_view()
        self.view.status_line.set('Workout 101', 'red')

    def _exit_on_about_view_delegate(self):
        self.view._exit_on_about_view()

    def _exit_on_help_view_delegate(self):
        self.view._exit_on_help_view()

    def _exit_on_FAQ_view_delegate(self):
        self.view._exit_on_FAQ_view()
        
    def _about(self):
        '''shows "about" window '''
        self.view._show_about_view()

    def _help(self):
        '''shows "help" window '''
        self.view._show_help_view('view')

    def _edit_help(self):
        '''edit "help" text '''
        self.view._show_help_view('edit')

    def _FAQ(self):
        '''shows "FAQ" window '''
        self.view._show_FAQ_view('view')

    def _edit_FAQ(self):
        '''edit "FAQ" text '''
        self.view._show_FAQ_view('edit')

    def _form(self):
        '''start preparing form'''
        self.workout_plan = WorkoutPlan(self, 'NEW')
        self.view._show_draft_form('NEW', None)

    def _workout_plan(self, wo_id):
        '''call workout plan from workout plan list '''
        self.view._show_draft_form('LOAD', wo_id)

    def _workout_from_cal(self, cal_id):
        '''call workout from calendar '''
        wo_id = self.model._get_wo_id_from_cal(cal_id)
        self.view._show_draft_form('LOAD CAL', wo_id, cal_id)
        
    def goQuit(self):
        '''close the main window '''
        self.root.destroy()
############################################################### CONTROLLER END##
#################################################################### VIEW ######
class View(Frame):

    def __init__(self, vc, parent):
        self.root = parent
        self.root.geometry('600x600+10+10')
        self.vc = vc
        self.makeFrames()
        self.status_line = Status(self.vc, self.frame4)
        self.makeMenu()

    def makeFrames(self):

        self.frame0 = Frame(self.root, width = 200)
        self.frame0.grid(row = 1, column = 0, sticky = W + N)
#        self.sema_00 = Semaphore(self.frame0)
        
        self.frame1 = Frame(self.root, width = 200)
        self.frame1.grid(row = 1, column = 0, sticky = W + N)
        self.sema_01 = Semaphore(self.frame1)
        
        self.frame2 = Frame(self.root, width = 200)
        self.frame2.grid(row = 1, column = 1, sticky = W + N)
        self.sema_02 = Semaphore(self.frame2)

        self.frame3 = Frame(self.root, width = 0)
        self.frame3.grid(row = 1, column = 2, sticky = W + N)
        self.sema_03 = Semaphore(self.frame3)

        self.frame4 = Frame(self.root) # status line frame
        self.frame4.grid(row = 0, column = 0, columnspan = 3, sticky = W+E)

        self.frame5 = Frame(self.root) # command frame
        self.frame5.grid(row = 2, column = 0, columnspan = 3, sticky = E)

        self.sema_top   = Semaphore()
        self.sema_about = Semaphore()
        self.sema_help  = Semaphore()
        self.sema_cart  = Semaphore()
        self.sema_FAQ   = Semaphore()
        self.sema_WPL   = Semaphore()
        self.sema_Cal   = Semaphore()



    def makeMenu(self):
        self.root.title('Main Menu')

##        self.wall = Background(self.frame0)
##        self.wall.grid(row=1)
               
        menubar = Menu(self.root, tearoff = 0)
        self.root.config(menu = menubar)

        m1_Menu = Menu(menubar)
        m1_Menu.add_command(label = 'New', command = self.vc.new_workout)
        m1_Menu.add_command(label = 'Load Plan', command = self.vc._load_workout_plan)
        m1_Menu.add_command(label = 'Load from calendar', command = self.vc._calendar)
        m1_Menu.add_separator()
        m1_Menu.add_command(label = 'Save', command = self.vc.foo)
        m1_Menu.add_command(label = 'Print', command = self.vc.foo)
        m1_Menu.add_command(label = 'PDF export', command = self.vc.foo)
        m1_Menu.add_command(label = 'Exit', command = self.vc.goQuit)
        menubar.add_cascade(label= 'Workout', menu=m1_Menu)

        m2_Menu = Menu(menubar)
        m2_Menu.add_command(label = 'New', command = self.vc.new_exercise)
        m2_Menu.add_command(label = 'Edit/Delete', command = self.vc.edit_exercise)
        menubar.add_cascade(label= 'Exercises', menu=m2_Menu)

        m3_Menu = Menu(menubar)
        m3_Menu.add_command(label = 'Show', command = self.vc._cart_record)
        m3_Menu.add_command(label = 'Form', command = self.vc.foo)
        menubar.add_cascade(label= 'Exercise Cart', menu=m3_Menu)

        m5_Menu = Menu(menubar)
        m5_Menu.add_command(label = 'Convert db --> txt file', command = self.vc.model._data_base_2_txt_file)
        m5_Menu.add_command(label = 'Convert txt file --> db', command = self.vc.model._txt_file_2_data_base)
        m5_Menu.add_command(label = 'Merge two dbs', command = self.vc.model._merge_2_data_bases)
        m5_Menu.add_command(label = 'Edit help', command = self.vc._edit_help)
        m5_Menu.add_command(label = 'Edit FAQ', command = self.vc._edit_FAQ)
        menubar.add_cascade(label= 'DevTools', menu=m5_Menu)

        m6_Menu = Menu(menubar)
        m6_Menu.add_command(label = 'About', command = self.vc._about)
        m6_Menu.add_command(label = 'Workout 101 help', command = self.vc._help)
        m6_Menu.add_command(label = 'FAQ', command = self.vc._FAQ)
        menubar.add_cascade(label= 'Help', menu=m6_Menu)

    def _show_body_parts(self, bp_IDs, mode):
        '''list body parts in frame 1 '''
        if self.sema_01.get_state():                      # if frame 1 is empty
            self.vc.new_workout_stack = WinStack()
            bp = BodyParts(self.vc, self.frame1, bp_IDs, mode)  # create bp instance
            self.status_line.set('Select body part for choosing exercises')
            self.vc.new_workout_stack.push(bp)            # push bp on stack
            self.sema_01.down()                           # block frame 1 for writing
        else:
            self._exit_on_new_workout()
            self.vc.new_workout_stack = WinStack()
            bp = BodyParts(self.vc, self.frame1, bp_IDs, mode)  # create bp instance
            self.status_line.set('Select body part for choosing exercises')
            self.vc.new_workout_stack.push(bp)            # push bp on stack
            self.sema_01.down()                           # block frame 1 for writing
          

               
    def _show_excercises(self, BP_ID, ex_IDs, mode):
        '''list excercises in frame 2 '''
        if self.sema_02.get_state():                      # if frame 2 is empty
            ex = Excercises(self.vc, self.frame2, BP_ID, ex_IDs, mode) # create ex instance
            self.status_line.set('Select exercises')
            self.vc.new_workout_stack.push(ex)            # push bp on stack
            self.sema_02.down()                           # block frame 2 for writing
        else:                                             # if frame 2 is not empty
            if not self.sema_top.get_state():             # check if top level window is not empty
                self.vc.exercise_stack.pop().destroy()    # remove its content and remove it from exercise stack
                self.sema_top.up()                        # let make top level window accessable for later inserting
                self.top.destroy()                        # close top level window
            else:
                self.vc.new_workout_stack.pop().destroy()
                self.sema_02.up()
                ex = Excercises(self.vc, self.frame2, BP_ID, ex_IDs, mode) # create ex instance
                self.vc.new_workout_stack.push(ex)            # push bp on stack
                self.sema_02.down()
           
    def _show_exercise_record(self, BP_ID, EX_ID, mode):
        '''show exercise record in separate window '''
        if self.sema_top.get_state():                     # if top window is empty
            self.top = Toplevel()                         # create pop-up window
            if mode == 'edit_exercise':
                self.top.geometry('405x610+440+35')
                self.top.title('Exercise record edit')
            if mode == 'new_exercise':
                self.top.geometry('405x610+300+35')
                self.top.title('New exercise record')
            elif mode == 'new_wokrout':
                self.top.geometry('405x600+630+10')
                self.top.title('Exercise record view')
            self.sema_top.set_frame(self.top)             # set top window to semaphore
            ex_record = ExcerciseView(self.vc, self.top, EX_ID, BP_ID, mode) # put ExerciseView into top level window
            self.vc.exercise_stack = WinStack()           # create stack for exercise record thread 
            self.vc.exercise_stack.push(ex_record)        # push ex_record on exercise stack
            self.sema_top.down()
        else:
            self.vc.exercise_stack.pop().destroy()        # remove top window content
            self.sema_top.up()                            # make top window accessable
            ex_record = ExcerciseView(self.vc, self.top, EX_ID, BP_ID, mode) # put new ExerciseView into top level window
            self.vc.exercise_stack.push(ex_record)        # push ex_record on exercise stack
            self.sema_top.down()                          # close top window for insering objects


    def _exit_on_exercise_view(self):
        '''handler when exercise record window is closed by clicking X '''
        self.sema_top.up()
        self.vc.exercise_stack.pop().destroy()
        del self.vc.exercise_stack
        self.top.destroy()
        

    def _show_about_view(self):
        if self.sema_about.get_state():                   # if about window is empty
            self.about = Toplevel(bd = 10)                # create pop-up window
            self.about.geometry('320x250+280+200')
            self.about.title('About')
            self.sema_about.set_frame(self.about)        
            about_window = AboutView(self.vc, self.about)
            self.sema_about.down()

    def _exit_on_about_view(self):
        '''handler when "about" window is closed by clicking X '''
        self.sema_about.up()
        self.about.destroy()

    def _show_help_view(self, mode):
        if self.sema_help.get_state():                   # if about window is empty
            self.help = Toplevel()                       # create pop-up window
            self.help.geometry('+630+10')
            self.help.title('Help')
            self.sema_help.set_frame(self.help)        
            help_window = HelpView(self.vc, self.help, mode)
            self.sema_help.down()

    def _exit_on_help_view(self):
        '''handler when "help" window is closed by clicking X '''
        self.sema_help.up()
        self.help.destroy()

    def _show_FAQ_view(self, mode):
        if self.sema_FAQ.get_state():                   # if FAQ window is empty
            self.FAQ = Toplevel()                       # create pop-up window
            self.FAQ.geometry('+630+10')
            self.FAQ.title('Frequently Asked Questions')
            self.sema_FAQ.set_frame(self.FAQ)        
            FAQ_window = FAQView(self.vc, self.FAQ, mode)
            self.sema_FAQ.down()

    def _exit_on_FAQ_view(self):
        '''handler when "FAQ" window is closed by clicking X '''
        self.sema_FAQ.up()
        self.FAQ.destroy()

    def _show_workout_plans_list(self, mode):
        '''show list of workout plans from database in separate window '''
        if self.sema_WPL.get_state():                   # if WPL (workout_plan_list) window is empty
            self.WPL = Toplevel()                       # create pop-up window
            self.WPL.geometry('+630+10')
            self.WPL.title('Workout Plans List')
            self.sema_WPL.set_frame(self.WPL)        
            WPL_window = WPLView(self.vc, self.WPL, mode)
            self.sema_WPL.down()        

    def _exit_on_WPL_view(self):
        '''handler when "WPL" window is closed by clicking X '''
        self.sema_WPL.up()
        self.WPL.destroy()

    def _show_calendar(self, scale = 'BIG', mode = 'LOAD'):
        '''show calendar '''
        if self.sema_Cal.get_state():               # if CalView window is empty
            self.CV = Toplevel()                    # create pop-up window
            self.CV.title('Calendar')
            self.sema_Cal.set_frame(self.CV)
            CV_window = CalView(self.vc, self.CV, scale, mode)
            self.sema_Cal.down()

    def _exit_on_calendar(self):
        '''handler when "CV" window is closed by clicking X '''
        self.sema_Cal.up()
        self.CV.destroy()      

    def _show_cart_view(self, actual_cart):
        '''list selected excercises in frame 3 - cart frame '''
        if self.sema_cart.get_state():                          # if cart frame is empty
            self.top_cart = Toplevel()
            self.top_cart.geometry('+630+10')
            self.top_cart.title('Exercise cart')
            ca = CartView(self.vc, self.top_cart, actual_cart)  # create ca (cart view) instance
            self.vc.cart_stack = WinStack()                     # create stack for cart thread 
            self.vc.cart_stack.push(ca)                         # push cart on stack
            self.sema_cart.down()                               # block cart frame from writing
        else:                                                   # if cart frame is not empty
            self.vc.cart_stack.pop().destroy()
            self.sema_cart.up()
            ca = CartView(self.vc, self.top_cart, actual_cart)  # create new ca (cart view) instance
            self.vc.cart_stack.push(ca)                         # push cart on stack
            self.sema_cart.down()

    def _exit_on_cart_viewX(self):
        self.sema_cart.up()
        self.vc.cart_stack.pop().destroy()
        del self.vc.cart_stack
        self.top_cart.destroy()

    def _show_draft_form(self, mode, wo_id, cal_id = None):
        '''shows workout plan on the screen'''
        if not self.sema_cart.get_state():
            self._exit_on_cart_viewX()
        if not self.sema_01.get_state():
            self._exit_on_new_workout()
        self.vc.new_workout_stack = WinStack()
        if mode == 'NEW':
            self.wf_draft = FormDraftView(self.vc, self.frame1, mode)
        elif mode == 'LOAD':
            self.wf_draft = FormDraftView(self.vc, self.frame1, mode, wo_id)
        elif mode == 'LOAD CAL':
            self.wf_draft = FormDraftView(self.vc, self.frame1, mode, wo_id, cal_id)
        self.status_line.set('Workout form: please fill out this form.')
        self.vc.new_workout_stack.push(self.wf_draft)       # push wf_draft on stack
        self.sema_01.down()                                 # block frame 1 for writing
        
    def _exit_on_form_view(self):
        self.sema_01.up()
        self.vc.new_workout_stack.pop().destroy()
        del self.vc.new_workout_stack

    def _exit_on_new_workout(self):
        '''new workout exit '''
        if not self.sema_top.get_state():                # if top window present
            self._exit_on_exercise_view()                # close it and update top semaphore and stack
        for i in range(len(self.vc.new_workout_stack)):  # close all windows opened in new_workout thread
            self.vc.new_workout_stack.pop().destroy()
        self.sema_01.up()                                # set all semaphores open
        self.sema_02.up()
#        self.sema_03.up()
        del self.vc.new_workout_stack
#        self.wall.grid_remove()
#        self.wall.grid()
##        self.wall = Background(self.frame0)
##        self.wall.grid(row=1)
        self.status_line.set('Main menu')
############################################################### VIEW END #######
############################################################### MODEL ##########
class Model:

    def __init__(self, vc):
        self.vc = vc
        self.cart = ExCart() #initialization of empty cart of exercises
        self.fileDB = 'components/database/db_04-test.db'
        self.fileHelp = 'components/help_files/help.txt'
        self.fileFAQ = 'components/help_files/FAQ.txt'

    def _get_body_parts_list_IDs(self):
        '''Returns a sorted list of body parts IDs'''
#        bpList = []
        db = shelve.open(self.fileDB)
        body_parts_IDs = list(db['BO'].keys()) # list of keys <- random sequence
        body_parts_IDs.sort()                  #              <- sorted sequence
        db.close()
        return body_parts_IDs

    def _get_workout_list_IDs(self):
        '''Returns a sorted list of workout plans IDs'''
        db = shelve.open(self.fileDB)
        wo_plans_IDs = list(db['WO_PLAN'].keys()) # list of keys <- random sequence
        wo_plans_IDs.sort()                     #              <- sorted sequence
        db.close()
        return wo_plans_IDs        

    def _get_workout_plan_name(self, WO_ID):
        '''Returns the name of workout plan for specified WO-ID.'''
        db = shelve.open(self.fileDB)
        woName = db['WO_PLAN'][WO_ID][10]['WO_NAME']
        db.close()
        return woName

        
    def _get_body_part_name(self, BO_ID):
        '''Returns the name of body for specified BO-ID.'''
        db = shelve.open(self.fileDB)
        boName = db['BO'][BO_ID]['BO-NAME']
        db.close()
        return boName

    def _get_exercises_list_IDs(self, BO_ID):
        '''Returns a sorted list of excercises for specified BO-ID.'''
        db = shelve.open(self.fileDB)
        exListID = db['BO'][BO_ID]['BO-EX']
        db.close()
        return exListID

    def _getNewExID(self, BO_ID):
        '''Creates excercise ID for new db['EX'] entry for specified BO-ID.'''
        db = shelve.open(self.fileDB)
        ex_list = db['BO'][BO_ID]['BO-EX'] # list of exercises for a specific BO_ID
        ex_list.sort()
        db.close()
        if len(ex_list) == 0:
            return 'EX-' + str(int(BO_ID[3:])) + '1'
        else:
            last_ex = ex_list[-1]
            return 'EX-' + str(int(last_ex[3:]) + 1)

    def _get_exercise_name(self, EX_ID):
        '''Returns excercise name for a specified EX-ID.'''
        db = shelve.open(self.fileDB)
        exName = db['EX'][EX_ID]['EX-NAME']
        db.close()
        return exName

    def _get_exercise_info(self, EX_ID):
        '''Returns exercise info for a specified EX-ID.'''
        db = shelve.open(self.fileDB)
        exInfo = db['EX'][EX_ID]['EX-INFO']
        db.close()
        return exInfo

    def _get_exercise_img_file_name(self, EX_ID):
        '''Returns exercise image file name for a specified EX-ID.'''
        db = shelve.open(self.fileDB)
        exIMG = db['EX'][EX_ID]['EX-IMG']
        db.close()
        return exIMG

    def _deleteEX(self, BO_ID, EX_ID):
        db = shelve.open(self.fileDB, writeback = True)
        db['BO'][BO_ID]['BO-EX'].remove(EX_ID)
        del db['EX'][EX_ID]
        db.close()

    def _saveEX(self, BO_ID, EX_ID, EX_NAME, EX_INFO, EX_IMG):
        EX_IMG = self._stripPATH(EX_IMG)
        db = shelve.open(self.fileDB, writeback = True)
        if EX_ID not in db['BO'][BO_ID]['BO-EX']:
            db['BO'][BO_ID]['BO-EX'].append(EX_ID)        
            db['EX'][EX_ID]={}
        db['EX'][EX_ID]['EX-ID'] = EX_ID
        db['EX'][EX_ID]['EX-NAME'] = EX_NAME
        db['EX'][EX_ID]['EX-INFO'] = EX_INFO
        db['EX'][EX_ID]['EX-IMG'] = EX_IMG
        if EX_ID not in db['BO'][BO_ID]['BO-EX']:
            db['BO'][BO_ID]['BO-EX'].append(EX_ID)
        db.close()

    def _get_new_workout_ID(self):
        '''New Workout ID generator.'''
        wo_list = self._get_workout_list_IDs()
        last_wo_ID = wo_list[-1]
        new_str_num = str(int(last_wo_ID[3:]) + 1)
        tmp = '000' + new_str_num # concatenates '000' and str(new number), i.e. '00011'
        tmp = tmp[-3:] # it takes the last three elements from string
        return 'WO-' + tmp

    def _get_WOplan(self, WO_ID):
        '''Retrives workout plan from database for specified workout_plan_ID.'''
        db = shelve.open(self.fileDB)
        wo_plan_record = db['WO_PLAN'][WO_ID]
        db.close()
        return wo_plan_record

    def _saveWOplan(self, WO_ID, data_record):
        '''Saves into database a new workout plan. '''
        db = shelve.open(self.fileDB, writeback = True)
        db['WO_PLAN'][WO_ID] = data_record
        db.close()

    def _deleteWO_plan(self, WO_ID):
        '''deletes workout plan from database '''
        db = shelve.open(self.fileDB, writeback = True)
        del db['WO_PLAN'][WO_ID]
        db.close()

    def _saveWO_to_cal(self, CAL_ID, workout_record):
        '''Saves workout into calendar database '''
        db = shelve.open(self.fileDB, writeback = True)
        db['CAL'][CAL_ID] = workout_record
        db.close()

    def _get_data_dates(self):
        '''returns dates with data from calendar database '''
        db = shelve.open(self.fileDB)
        data_dates = [date for date in db['CAL']]
        db.close()
        return data_dates

    def _get_wo_id_from_cal(self, CAL_ID):
        '''returns WO_ID from calendar database for given CAL_ID '''
        db = shelve.open(self.fileDB)
        wo_id = db['CAL'][CAL_ID][10]['WO_ID']
        db.close()
        return wo_id

    def _get_WO_from_cal(self, CAL_ID):
        '''returns workout record from calendar database for given CAL_ID '''
        db = shelve.open(self.fileDB)
        wo = db['CAL'][CAL_ID]
        db.close()
        return wo
    
    def _stripPATH(self, file_name):
        '''stripe PATH from file name'''
        a = file_name[::-1]
        b = a[:a.find('/')]
        c = b[::-1]
        return c

    def _get_help_text(self):
        file = open(self.fileHelp)
        help_text = file.read()
        file.close()
        return help_text

    def _get_FAQ_text(self):
        file = open(self.fileFAQ)
        FAQ_text = file.read()
        file.close()
        return FAQ_text        

    def _save_help(self, help_text):
        file = open(self.fileHelp, 'w')
        file.write(help_text)
        file.close()

    def _save_FAQ(self, FAQ_text):
        file = open(self.fileFAQ, 'w')
        file.write(FAQ_text)
        file.close()

    def _data_base_2_txt_file(self):
        '''reads data base and saves it as structurized text file'''
        file_to_read_from = filedialog.askopenfilename(defaultextension = '.db', filetypes = [('DB file', '*.db')])
        file_to_write_to = filedialog.asksaveasfilename(defaultextension = '.txt', filetypes = [('text file', '*.txt')])
        db = shelve.open(file_to_read_from)
        file = open(file_to_write_to, 'w')
        for level_01 in db:
            file.write('$$$' + str(level_01) + '$$$' + str(db[level_01]))
        file.close()
        db.close()

    def _txt_file_2_data_base(self):
        '''reads data base and saves it as structurized text file'''
        file_to_read_from = filedialog.askopenfilename(defaultextension = '.txt', filetypes = [('text file', '*.txt')])
        file_to_write_to = filedialog.asksaveasfilename(defaultextension = '.db', filetypes = [('DB file', '*.db')])
        file = open(file_to_read_from, 'r')
        fileS = file.read()
        file.close()
        b = fileS.split('$$$')
        db = shelve.open(file_to_write_to)
        db[b[1]] = eval(b[2])
        db[b[3]] = eval(b[4])
        db.close()

    def _merge_2_data_bases(self):
        '''opens 2 data bases, merges them and saves output as a new database'''
        file01_to_read_from = filedialog.askopenfilename(defaultextension = '.db', filetypes = [('DB file', '*.db')])
        file02_to_read_from = filedialog.askopenfilename(defaultextension = '.db', filetypes = [('DB file', '*.db')])
        db_01 = shelve.open(file01_to_read_from)
        db_02 = shelve.open(file02_to_read_from, writeback = True)
        print('db1 ex list:', list(db_01['EX']))
        print('db2 ex list:', list(db_02['EX']))
        for bp_ID in db_01['BO']:
            test = db_01['BO'][bp_ID]['BO-EX'] != db_02['BO'][bp_ID]['BO-EX'] # if particular body part exercise list of both dbs are different
            if test: # yes - there are differences
                merged_list_of_exercises = [i for i in set(db_01['BO'][bp_ID]['BO-EX']).union(set(db_02['BO'][bp_ID]['BO-EX']))]
                db_02['BO'][bp_ID]['BO-EX'] = merged_list_of_exercises # update body part exercises
                for ex_ID in merged_list_of_exercises:
                    if ex_ID in list(db_01['EX']):
                        db_02['EX'][ex_ID] = db_01['EX'][ex_ID]
        for i in (db_02['BO']):
            print(i, db_02['BO'][i])
        print(50*'-')
        print('db1 ex list:', list(db_01['EX']))
        print('db2 ex list:', list(db_02['EX']))
        db_01.close()
        db_02.close()
        
############################################################### MODEL END#######

def main():
    root = Tk()
    root.title('Workout 101')
    app = Controller(root)
    root.mainloop()
    
if __name__ == '__main__':
    main() 
