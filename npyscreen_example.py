import npyscreen as nps
import os
from collections import namedtuple
import subprocess
import sys
import signal


terminal_size = os.get_terminal_size()
if terminal_size.lines < 20:
    terminal_size = namedtuple('_TerminalSize', 'columns, lines')(terminal_size.columns, 20)
if terminal_size.columns < 100:
    terminal_size = namedtuple('_TerminalSize', 'columns, lines')(100, terminal_size.lines)


values_list = [
    "Message",
    "Enter text",
    "Inputed value",
    "Очистка"]

def get_console_size():
    rows, cols = 24, 104  # Set default values

    try:
        result = subprocess.check_output(['stty', 'size'])
        rows, cols = map(int, result.decode().split())
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return max(rows, 24), max(cols, 104)

def handle_resize(signum, frame):
    if hasattr(sys, 'frozen'):  # running in a PyInstaller bundle
        # Get the command-line arguments for the executable
        args = [sys.executable] + sys.argv[1:]

        # Restart the script using subprocess
        subprocess.run(args, check=True)

        # Exit the current process
        sys.exit(0)
    else:  # running in a normal Python environment
        os.execv(sys.executable, ['python'] + sys.argv)

class Menu(nps.FormBaseNew):
    select_file = ""
    input_value = ""

    def __init__(self, *args, **keywords):
        super(Menu, self).__init__(*args, **keywords)
        self.initializing = True

    def create(self):
        y = self.parentApp.y
        x = self.parentApp.x
        self.color = 'NO_EDIT'

        
        self.option = self.add(
            nps.TitleSelectOne,
            name="Values\n",
            relx = (x - 100) // 2 + 4,
            rely = (y - 20) // 2 + 2,
            values=values_list,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
            max_width=36,
            max_height=10)

        self.option.when_value_edited = self.on_option_selected

        self.box = self.add(
            nps.BoxBasic,
            name="My Box",
            relx=(x - 100) // 2,
            rely=(y - 20) // 2,
            width=100,
            height=20,
            editable=False)


# Этот блок относится к - Статус - его наполнение
        self.box_processbar = self.add(
            nps.BoxBasic,
            name="Processbar",
            relx = (x - 100) // 2 + 61,
            rely = (y - 20) // 2 + 1,
            color='CURSOR_INVERSE',
            max_height=5,
            max_width=37,
            editable=False)

        self.widget_processbar = self.add(
            ProcessBar,
            relx = (x - 100) // 2 + 63,
            rely = (y - 20) // 2 + 4,
            value=int(50),
            color='WARNING',
            max_width=33,
            editable=False)


# Этот блок относится к - Статус ALSE - его наполнение
        self.button_processbar_minus = self.add(
            nps.ButtonPress,
            name="-Progress",
            relx = (x - 100) // 2 + 61,
            rely = (y - 20) // 2 + 7,
            when_pressed_function=self.ButtonProcessbarMinus,
            color='DANGER',
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,)

# Этот блок относится к - Статус ALSE - создание блока
# в необходимом месте
        self.box_button_processbar_minus = self.add(
            nps.BoxBasic,
            name="",
            relx = (x - 100) // 2 + 75,
            rely = (y - 20) // 2 + 6,
            color='CONTROL',
            max_height=3,
            max_width=13,
            editable=False)

# Этот блок относится к - Статус ALSE - его наполнение
        self.button_processbar_plus = self.add(
            nps.ButtonPress,
            name="+Progress",
            relx = (x - 100) // 2 + 75,
            rely = (y - 20) // 2 + 7,
            when_pressed_function=self.ButtonProcessbarPlus,
            color='GOOD',
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,)

        self.button_file_manager = self.add(
            nps.ButtonPress,
            name="File manager",
            relx = (x - 100) // 2 + 22,
            rely = (y - 20) // 2 + 14,
            when_pressed_function=self.ButtonFileManager,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.button_file_selected = self.add(
            nps.ButtonPress,
            name="Selected file",
            relx = (x - 100) // 2 + 40,
            rely = (y - 20) // 2 + 14,
            when_pressed_function=self.ButtonFileSelected,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.button_open_file = self.add(
            nps.ButtonPress,
            name="Open file",
            relx = (x - 100) // 2 + 60,
            rely = (y - 20) // 2 + 14,
            when_pressed_function=lambda: self.ButtonFileOpen(Menu.select_file, 'Content'),
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.button_exit = self.add(
            nps.ButtonPress,
            name="Exit",
            relx = (x - 100) // 2 + 72,
            rely = (y - 20) // 2 + 14,
            when_pressed_function=self.ButtonExit,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.display()
        self.initializing = False

    def resize(self, y=None, x=None):
        if self.initializing:
            return
        if y is None or x is None:
            y, x = get_console_size()

        x, y = get_console_size()
        self.box.relx = (x - 100) // 2
        self.box.rely = (y - 20) // 2

        self.option.relx = (x - 100) // 2 + 4
        self.option.rely = (y - 20) // 2 + 2

        self.box_processbar.relx = (x - 100) // 2 + 61
        self.box_processbar.rely = (y - 20) // 2 + 1

        self.widget_processbar.relx = (x - 100) // 2 + 63
        self.widget_processbar.rely = (y - 20) // 2 + 4

        self.button_processbar_minus.relx = (x - 100) // 2 + 61
        self.button_processbar_minus.rely = (y - 20) // 2 + 7

        self.box_button_processbar_minus.relx = (x - 100) // 2 + 75
        self.box_button_processbar_minus.rely = (y - 20) // 2 + 6

        self.button_processbar_plus.relx = (x - 100) // 2 + 75
        self.button_processbar_plus.rely = (y - 20) // 2 + 7

        self.button_file_manager.relx = (x - 100) // 2 + 22
        self.button_file_manager.rely = (y - 20) // 2 + 14

        self.button_file_selected.relx = (x - 100) // 2 + 40
        self.button_file_selected.rely = (y - 20) // 2 + 14

        self.button_open_file.relx = (x - 100) // 2 + 60
        self.button_open_file.rely = (y - 20) // 2 + 14

        self.button_exit.relx = (x - 100) // 2 + 72
        self.button_exit.rely = (y - 20) // 2 + 14

        self.display()

    def ButtonProcessbarMinus(self):
        if self.widget_processbar.value == 00:
            self.widget_processbar.color = "DANGER"
        if self.widget_processbar.value > 00:
            self.widget_processbar.value -= 10
            self.widget_processbar.color = "WARNING"
        self.display()

    def ButtonProcessbarPlus(self):
        if self.widget_processbar.value == 100:
            self.widget_processbar.color = "GOOD"
        if self.widget_processbar.value < 100:
           self.widget_processbar.value += 10
           self.widget_processbar.color = "WARNING"
        self.display()

    def ButtonFileManager(self):
        self.parentApp.change_form('FileManager')

    def ButtonFileSelected(self):
        nps.notify_wait(f'Your value: {Menu.select_file}', title='Example')

    def ButtonFileOpen(self, text, name):
        try:
            file_content = open(text)
            self.parentApp.addForm(
                'FILE_VIEWER',
                AttentionForm,
                name=name,
                lines=terminal_size.lines,
                columns=terminal_size.columns,
                scroll_exit=True,
                editable=True,
                text=file_content.read()
            )
            self.parentApp.switchForm('FILE_VIEWER')
        except FileNotFoundError:
            self.parentApp.addForm(
                'FILE_VIEWER',
                AttentionForm,
                name='Error',
                lines=terminal_size.lines,
                columns=terminal_size.columns,
                scroll_exit=True,
                editable=True,
                text="File not found."
            )
            self.parentApp.switchForm('FILE_VIEWER')

    def ButtonExit(self):
        self.parentApp.setNextForm(None)
        self.parentApp.switchForm(None)

    def Buttoninput(self):
        input_form = nps.Form(name="Enter some text",
                                            lines=10,
                                            columns=80,
                                            x=20,
                                            y=20)

        input_field = input_form.add(nps.TitleText,
                                             name=' ',
                                             lines=10,
                                             columns=80)
        input_form.edit()
        Menu.input_value = input_field.value


    def on_option_selected(self):
        if self.option.value and self.option.value[0] is not None:
            selected_option_index = self.option.value[0]
            chosen_value = self.option.values[selected_option_index]

            if chosen_value == "Message":
                nps.notify_wait('Your text', title='Example')

            if chosen_value == "Enter text":
                self.Buttoninput()

            if chosen_value == "Inputed value":

                nps.notify_wait(f'Your file path: {Menu.input_value}', title='Example')

class ProcessBar(nps.Slider):
    def __init__(self, *args, **keywords):
        super(ProcessBar, self).__init__(*args, **keywords)
        self.editable = False

class FileManager(nps.FormBaseNew):
    def create(self):

        self.file_manager_form = self.add(nps.TitleFilenameCombo, name="File Manager", lines=31, columns=101,)

        self.button = self.add(
            nps.ButtonPress,
            name="Menu",
            when_pressed_function=self.MenuButton,
            begin_entry_at=0,
            relx=1,
            rely=6,
            scroll_exit=True,
            editable=True,)

    def MenuButton(self):
        Menu.select_file = self.file_manager_form.value
        self.parentApp.change_form('MAIN')

class AttentionForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = 'OK'
    
    def __init__(self, *args, **keywords):
        self.text = keywords.get('text', '')
        super(AttentionForm, self).__init__(*args, **keywords)
    
    def create(self):
        self.box = self.add(nps.BoxBasic,
                            name="My Box",
                            width=100,
                            height=20,
                            relx=(terminal_size.columns - 100) // 2,
                            rely=(terminal_size.lines - 20) // 2,
                            editable=False)
    
        self.message = self.add(
            nps.Pager,
            values=self.text.split('\n'),
            max_height=18,
            max_width=96,
            columns=90,
            relx=(terminal_size.columns - 100) // 2 + 2,
            rely=(terminal_size.lines - 20) // 2 + 1,
            lines=10,
            scroll_exit=True,
            editable=True,
            name=self.name
        )

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class App(nps.NPSAppManaged):
    def onStart(self):
        y, x = get_console_size()
        self.y = y
        self.x = x
        self.addForm('MAIN', Menu, name='', lines=y, columns=x)
        self.addForm('FileManager', FileManager, name="", lines=y, columns=x)

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()

if __name__ == "__main__":
    signal.signal(signal.SIGWINCH, handle_resize)
    app = App()
    app.run()