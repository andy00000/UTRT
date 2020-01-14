# Импорт необходимых библиотек

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from ftplib import FTP
import os
import zipfile
from shutil import copyfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

# Класс описания функций непосредственной работы с файлами обмена
class RTBase:

# Инициализация, присвоение констант. В будущем переработать под импорт из файла конфигурации
    def __init__(self, Base, widget):
        self.Base = Base
        self.source_path = r'\\brc-1c-01\Exchange_RT_UT\Checked'
        self.temp_path = r'D:\Upload'
        self.widget = widget

# Функция обмена по направлению из УТ в РТ
    def UTRT(self):
        self.widget.delete(1.0, END)
        self.checked_fname = '\\Message_CNT_' + self.Base + '.xml'
        self.xml_path = self.source_path + self.checked_fname
        self.zip_path = 'D:\\Upload' + self.checked_fname[:-4] + '.zip'

        self.widget.insert(INSERT, 'XML path: ' + self.xml_path + '\n')

        copyfile(self.xml_path, self.temp_path + self.checked_fname)

        zf = zipfile.ZipFile(self.zip_path, mode='w')
        zf.write(self.temp_path + self.checked_fname, compress_type=compression)
        zf.close()

        self.widget.insert(INSERT, 'ZIP copy: ' + self.zip_path + '\n')

        ftp = FTP('brc-ftp-02.bristolcapital.ru')
        FTPOUT = ftp.login(user='Retail', passwd='#hjpybwf12)')
        FTPOUT += '\n'
        self.widget.insert(INSERT, FTPOUT)

        file = open(self.zip_path, 'rb')
        FTPOUT = ftp.storbinary('STOR ' + os.path.basename(self.zip_path), file)
        FTPOUT += '\n'
        self.widget.insert(INSERT, FTPOUT)

        file.close()
        FTPOUT = ftp.quit()
        FTPOUT += '\n'
        self.widget.insert(INSERT, FTPOUT)

# Функция обмена по направлению из РТ в УТ
    def RTUT(self):
        self.widget.delete(1.0, END)

        self.checked_fname = '\\Message_' + self.Base + '_CNT.xml'
        self.xml_path = self.source_path + self.checked_fname
        self.zip_path = 'D:\\Upload' + self.checked_fname[:-4] + '.zip'
        self.widget.insert(INSERT, 'XML path: ' + self.xml_path + '\n')
        self.widget.insert(INSERT, 'ZIP path: ' + self.zip_path + '\n')

        # copy .zip from FTP
        ftp = FTP('brc-ftp-02.bristolcapital.ru')
        FTPOUT = ftp.login(user='Retail', passwd='#hjpybwf12)')
        FTPOUT += '\n'
        self.widget.insert(INSERT, FTPOUT)

        with open(self.zip_path, 'wb') as f:
            FTPOUT = ftp.retrbinary('RETR ' + os.path.basename(self.zip_path), f.write)
            FTPOUT += '\n'
            self.widget.insert(INSERT, FTPOUT)

        f.close()
        FTPOUT = ftp.quit()
        FTPOUT += '\n'
        self.widget.insert(INSERT, FTPOUT)

        # unzip file
        zf = zipfile.ZipFile(self.zip_path, mode='r')
        zf.extractall(path=self.temp_path)

        # copy file to checked
        copyfile(self.temp_path + self.checked_fname, self.xml_path)

        self.widget.insert(INSERT, 'All files sucсessfully copied to destanation. Run synchronization at 1C.')

# Класс построения основного окна в программе и обработки событий UI
class WorkWindow:
    def __init__(self):

        # Проверка длины имени базы и её содержания. Доработать с учётом недопустимости русских букв
        def CheckBase(Base):
            AccSym = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for i in Base:
                if i not in AccSym:
                    return False
            return len(Base) == 3 and Base.isalpha()

        # Функция обработки кноки "ChekNode".
        def ChekNode():
            Node = self.BaseEntry.get()
            if CheckBase(Node):
                self.UTRTButton.configure(state='active')
                self.RTUTButton.configure(state='active')
            else:
                messagebox.showinfo('ERROR ALERT',
                                    message='Node name must be 3 capital letters without digits and special chars!')
                self.UTRTButton.configure(state='disabled')
                self.RTUTButton.configure(state='disabled')

        # Функция обработки клика по лого
        def logo_click(event):
            messagebox.showinfo('About', message='UT_RT exchange helper. V.2.1.20 by Andrey Shmyrov')

        # Функция обработки кнопок обмена, направление обмена зависит от параметра direction
        def Exchange(direction): #Bool. True - UT -> RT, False - RT -> UT
            method = 'UTRT' if direction else 'RTUT'

            if CheckBase(self.BaseEntry.get()):
                self.BaseEntry.configure(state='disabled')
                RB = RTBase(self.BaseEntry.get(), self.InfoArea)
                getattr(RB, method)()
                self.BaseEntry.configure(state='normal')
            else:
                messagebox.showinfo('ERROR ALERT',
                                    message='Node name must be 3 capital letters without digits and special chars!')
                self.RTUTButton.configure(state='disabled')
                self.UTRTButton.configure(state='disabled')

        # Блок отрисовки виджетов основного окна
        self.MainWin = Tk()

        self.MainWin.title('UT - RT exchange utility. V2.1.20')

        self.NodeLabel = Label(self.MainWin, text='NODE: ')
        self.NodeLabel.grid(column=0, row=1, padx=3, pady=3)

        self.validator = self.MainWin.register(CheckBase)
        self.BaseEntry = Entry(self.MainWin, width=4, font=('Arial Bold', 14))
        self.BaseEntry.grid(column=1, row=1, padx=3, pady=3)
        self.BaseEntry.insert(0, '***')

        self.CKButton = Button(self.MainWin, text="Check node", width=17,  height=5, command=ChekNode)
        self.CKButton.grid(column=0, columnspan=2, row=2, padx=3, pady=3)

        self.UTRTButton = Button(self.MainWin, text="UT to RT upload", width=17,  height=2,
                                 command=lambda direction=True: Exchange(direction))
        self.UTRTButton.grid(column=0, columnspan=2, row=3, padx=3, pady=3)
        self.UTRTButton.configure(state='disabled')

        self.RTUTButton = Button(self.MainWin, text="RT to UT download", width=17,  height=2,
                                 command=lambda direction=False: Exchange(direction))
        self.RTUTButton.grid(column=0, columnspan=2, row=4, padx=3, pady=3)
        self.RTUTButton.configure(state='disabled')

        self.InfoArea = scrolledtext.ScrolledText(self.MainWin, width=45, height=10, bg='#f4f4f4')
        self.InfoArea.grid(column=0, columnspan=4, row=5, padx=3, pady=6)
        self.InfoArea.insert(INSERT, 'Information area')

        self.canvas = Canvas(self.MainWin, width=200, height=200)
        self.canvas.grid(column=3, row=1, rowspan=4, padx=3, pady=6)
        self.logo = PhotoImage(file="oie_transparent.png")
        self.canvas.create_image(102, 102, anchor=CENTER, image=self.logo, tag='logo')
        self.canvas.tag_bind('logo', '<Button-1>', logo_click)

        self.MainWin.mainloop()

#Запуск жизни, вселенной и всего такого
answer42 = WorkWindow()
