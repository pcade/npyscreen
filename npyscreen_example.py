import npyscreen as nps
from collections import namedtuple
import curses


# Minimum and maximum width and height for the application window
MIN_WIDTH = 105
MIN_HEIGHT = 35

WIDTH = 100
HEIGHT = 30

MAX_WIDTH = 300
MAX_HEIGHT = 300

# List of values for the select one menu
values_list = [
    "Message",
    "Enter text",
    "Inputed value"]

error_messages = {
    FileNotFoundError: "Указанная команда или исполняемый файл не найдены.",
    PermissionError: "У вас недостаточно прав для выполнения этой операции.",
    Exception: "Произошла непредвиденная ошибка: {}",
}

class Menu(nps.FormBaseNew):
    select_file = ""
    input_value = ""

    def create(self):
        self.color = 'NO_EDIT'

        self.option = self.add(
            nps.TitleSelectOne,
            name="Values\n",
            relx = (MIN_WIDTH - WIDTH) // 2 + 4,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 2,
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
            relx=(MIN_WIDTH - WIDTH) // 2,
            rely=(MIN_HEIGHT - HEIGHT) // 2,
            width=100,
            height=20,
            editable=False)

# Этот блок относится к - Статус - его наполнение
        self.box_processbar = self.add(
            nps.BoxBasic,
            name="Processbar",
            relx = (MIN_WIDTH - WIDTH) // 2 + 61,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 1,
            color='CURSOR_INVERSE',
            max_height=5,
            max_width=37,
            editable=False)

        self.widget_processbar = self.add(
            ProcessBar,
            relx = (MIN_WIDTH - WIDTH) // 2 + 63,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 4,
            value=int(50),
            color='WARNING',
            max_width=33,
            editable=False)


# Этот блок относится к - Статус ALSE - его наполнение
        self.button_processbar_minus = self.add(
            nps.ButtonPress,
            name="-Progress",
            relx = (MIN_WIDTH - WIDTH) // 2 + 61,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 7,
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
            relx = (MIN_WIDTH - WIDTH) // 2 + 75,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 6,
            color='CONTROL',
            max_height=3,
            max_width=13,
            editable=False)

# Этот блок относится к - Статус ALSE - его наполнение
        self.button_processbar_plus = self.add(
            nps.ButtonPress,
            name="+Progress",
            relx = (MIN_WIDTH - WIDTH) // 2 + 75,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 7,
            when_pressed_function=self.ButtonProcessbarPlus,
            color='GOOD',
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,)

        self.button_file_manager = self.add(
            nps.ButtonPress,
            name="File manager",
            relx = (MIN_WIDTH - WIDTH) // 2 + 22,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 14,
            when_pressed_function=self.ButtonFileManager,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.button_file_selected = self.add(
            nps.ButtonPress,
            name="Selected file",
            relx = (MIN_WIDTH - WIDTH) // 2 + 40,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 14,
            when_pressed_function=self.ButtonFileSelected,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.button_open_file = self.add(
            nps.ButtonPress,
            name="Open file",
            relx = (MIN_WIDTH - WIDTH) // 2 + 60,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 14,
            when_pressed_function=lambda: self.ButtonFileOpen(Menu.select_file, 'Content'),
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

        self.button_exit = self.add(
            nps.ButtonPress,
            name="Exit",
            relx = (MIN_WIDTH - WIDTH) // 2 + 72,
            rely = (MIN_HEIGHT - HEIGHT) // 2 + 14,
            when_pressed_function=self.ButtonExit,
            begin_entry_at=0,
            scroll_exit=True,
            editable=True,
        )

    def resize(self):
        super(Menu, self).resize()
        maxy, maxx = curses.initscr().getmaxyx()

        if maxx < MIN_WIDTH or maxy < MIN_HEIGHT:
            return

        if maxx > MAX_WIDTH or maxy > MAX_HEIGHT:
            maxx, maxy = MAX_WIDTH, MAX_HEIGHT

        self.box.relx = (maxx - WIDTH) // 2
        self.box.rely = (maxy - HEIGHT) // 2

        self.option.relx = (maxx - WIDTH) // 2 + 4
        self.option.rely = (maxy - HEIGHT) // 2 + 2


        self.box_processbar.relx = (maxx - WIDTH) // 2 + 61
        self.box_processbar.rely = (maxy - HEIGHT) // 2 + 1

        self.widget_processbar.relx = (maxx - WIDTH) // 2 + 63
        self.widget_processbar.rely = (maxy - HEIGHT) // 2 + 4

        self.button_processbar_minus.relx = (maxx - WIDTH) // 2 + 61
        self.button_processbar_minus.rely = (maxy - HEIGHT) // 2 + 7

        self.box_button_processbar_minus.relx = (maxx - WIDTH) // 2 + 75
        self.box_button_processbar_minus.rely = (maxy - HEIGHT) // 2 + 6

        self.button_processbar_plus.relx = (maxx - WIDTH) // 2 + 75
        self.button_processbar_plus.rely = (maxy - HEIGHT) // 2 + 7

        self.button_file_manager.relx = (maxx - WIDTH) // 2 + 22
        self.button_file_manager.rely = (maxy - HEIGHT) // 2 + 14

        self.button_file_selected.relx = (maxx - WIDTH) // 2 + 40
        self.button_file_selected.rely = (maxy - HEIGHT) // 2 + 14

        self.button_open_file.relx = (maxx - WIDTH) // 2 + 60
        self.button_open_file.rely = (maxy - HEIGHT) // 2 + 14

        self.button_exit.relx = (maxx - WIDTH) // 2 + 72
        self.button_exit.rely = (maxy - HEIGHT) // 2 + 14

        super(Menu, self).resize()

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
                lines=HEIGHT-10,
                columns=WIDTH,
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
                lines=HEIGHT-10,
                columns=WIDTH,
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

                nps.notify_wait(f'Your msg: {Menu.input_value}', title='Example')

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
        self.message = self.add(
            nps.Pager,
            values=self.text.split('\n'),
            columns=20,
            relx=2,
            rely=1,
            lines=90,
            scroll_exit=True,
            editable=True,
            name=self.name
        )
    
    def on_ok(self):
        self.parentApp.switchFormPrevious()

class App(nps.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', Menu, name='', columns=MAX_WIDTH, lines=MAX_HEIGHT, framed=False)
        self.addForm('FileManager', FileManager, name="", columns=WIDTH, lines=HEIGHT- 10)



    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()

if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except tuple(error_messages.keys()) as e:
        print(e)