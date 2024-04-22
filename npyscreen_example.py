import npyscreen as nps
import os
from collections import namedtuple



values_list = [
    "Message",
    "Enter text",
    "Inputed value",
    "Очистка"]

terminal_size = os.get_terminal_size()
if terminal_size.lines < 20:
    terminal_size = namedtuple('_TerminalSize', 'columns, lines')(terminal_size.columns, 20)
if terminal_size.columns < 100:
    terminal_size = namedtuple('_TerminalSize', 'columns, lines')(100, terminal_size.lines)



class Menu(nps.FormBaseNew):
    select_file = ""
    input_value = ""

    def while_waiting(self):
        self.display()

    def create(self):
        self.color = 'NO_EDIT'

        self.option = self.add(
            nps.TitleSelectOne,
            name="Values\n",
            values=values_list,
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 4,
            rely=(terminal_size.lines - 20) // 2 + 2,
            scroll_exit=True,
            editable=True,
            max_width=36,
            max_height=10)
    
        self.option.when_value_edited = self.on_option_selected

        self.box = self.add(nps.BoxBasic,
                            name="My Box",
                            width=100,
                            height=20,
                            relx=(terminal_size.columns - 100) // 2,
                            rely=(terminal_size.lines - 20) // 2,
                            editable=False)


# Этот блок относится к - Статус - его наполнение
        self.add(
            nps.BoxBasic,
            name="Progressbar",
            relx=(terminal_size.columns - 100) // 2 + 61,
            rely=(terminal_size.lines - 20) // 2 + 1,
            color='CURSOR_INVERSE',
            max_height=5,
            max_width=37,
            editable=False)

        self.process_widget = self.add(
            ProcessBar,
            value=int(50),
            relx=(terminal_size.columns - 100) // 2 + 63,
            rely=(terminal_size.lines - 20) // 2 + 4,
            color='WARNING',
            max_width=33,
            editable=False)


# Этот блок относится к - Статус ALSE - его наполнение
        self.status_check = self.add(
            nps.ButtonPress,
            name="-Progress",
            when_pressed_function=self.Progressbar_minus,
            color='DANGER',
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 61,
            rely=(terminal_size.lines - 20) // 2 + 7,
            scroll_exit=True,
            editable=True,)

# Этот блок относится к - Статус ALSE - создание блока
# в необходимом месте
        self.add(
            nps.BoxBasic,
            name="",
            relx=(terminal_size.columns - 100) // 2 + 75,
            rely=(terminal_size.lines - 20) // 2 + 6,
            color='CONTROL',
            max_height=3,
            max_width=13,
            editable=False)

# Этот блок относится к - Статус ALSE - его наполнение
        self.status_check = self.add(
            nps.ButtonPress,
            name="+Progress",
            when_pressed_function=self.Progressbar_plus,
            color='GOOD',
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 75,
            rely=(terminal_size.lines - 20) // 2 + 7,
            scroll_exit=True,
            editable=True,)

        self.file_manager_button = self.add(
            nps.ButtonPress,
            name="File manager",
            when_pressed_function=self.FileManagerButton,
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 22,
            rely=(terminal_size.lines - 20) // 2 + 14,
            scroll_exit=True,
            editable=True,
        )

        self.file_selected_button = self.add(
            nps.ButtonPress,
            name="Selected file",
            when_pressed_function=self.FileSelectedButton,
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 40,
            rely=(terminal_size.lines - 20) // 2 + 14,
            scroll_exit=True,
            editable=True,
        )

        self.open_file_button = self.add(
            nps.ButtonPress,
            name="Open file",
            when_pressed_function=lambda: self.FileOpenButton('Menu.select_file', 'Content'),
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 60,
            rely=(terminal_size.lines - 20) // 2 + 14,
            scroll_exit=True,
            editable=True,
        )

        self.exit_button = self.add(
            nps.ButtonPress,
            name="Exit",
            when_pressed_function=self.Exit,
            begin_entry_at=0,
            relx=(terminal_size.columns - 100) // 2 + 72,
            rely=(terminal_size.lines - 20) // 2 + 14,
            scroll_exit=True,
            editable=True,
        )

    def Progressbar_minus(self):
        if self.process_widget.value == 00:
            self.process_widget.color = "DANGER"
        if self.process_widget.value > 00:
            self.process_widget.value -= 10
            self.process_widget.color = "WARNING"
        self.display()

    def Progressbar_plus(self):
        if self.process_widget.value == 100:
            self.process_widget.color = "GOOD"
        if self.process_widget.value < 100:
           self.process_widget.value += 10
           self.process_widget.color = "WARNING"
        self.display()

    def FileManagerButton(self):
        self.parentApp.change_form('FileManager')

    def FileSelectedButton(self):
        nps.notify_wait(f'Your value: {Menu.select_file}', title='Example')

    def FileOpenButton(self, text, name):
        try:
            file_content = open('test.txt')
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

    def Exit(self):
        self.parentApp.setNextForm(None)
        self.parentApp.switchForm(None)

    def input(self):
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
                self.input()

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
        self.addForm('MAIN', Menu, name='', lines=terminal_size.lines, columns=terminal_size.columns,)
        self.addForm('FileManager', FileManager, name="")

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()

if __name__ == "__main__":
    app = App()
    app.run()