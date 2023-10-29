import numpy as np
from multipledispatch import dispatch
import sys
import getpass
import numpy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pprint import pprint
import sympy
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import math

errorinput = 0
Npolinom = 0
Kof = []
Choice = 0
previousKof = []
previousChoice = 0
previousResult = ""
oldDataX = []
oldNewDataY = []
E = 0
out = []


def CheckInputFile(CHAR):
    result = 1
    try:
        a = CHAR
        b = float(CHAR)
    except ValueError:
        # print("error")
        # print(a)
        messagebox.showerror("Error", "Файл содержит неверные данные! Возможно в данных есть лишние символы.")
        result = -1
    finally:
        return result



def DeleteXorY(CHAR, DATA):
    try:
        complex(CHAR)
    except ValueError:
        DATA.remove(CHAR)


def Gauss(LEFT, RIGHT, X):
    for k in range(len(X)-1):
        for i in range(k+1, len(X)):
            for j in range(k+1, len(X)):
                LEFT[i, j] -= LEFT[k, j] * (LEFT[i, k] / LEFT[k, k])
            RIGHT[i] -= RIGHT[k] * LEFT[i, k] / LEFT[k, k]
    for k in range(len(X) - 1, -1, -1):
        S = 0
        for j in range(k+1, len(X)):
            S += LEFT[k, j] * X[j]
        X[k] = (RIGHT[k] - S) / LEFT[k, k]
    return X


def Simple(X, Y, N):
    XN = numpy.zeros((N+1, N+1))
    XNRows = len(XN)
    XNCols = len(XN[0])
    XY = numpy.zeros(N+1)
    Kof = numpy.zeros(N+1)
    pX = 0
    pY = 0
    for i in range(XNRows):
        for j in range(XNCols):
            for k in range(len(X)):
                XN[i, j] += float(X[k])**pX
            pX += 1
        pX -= XNRows - 1;
        for h in range(len(Y)):
            XY[i] += (float(X[h])**pY) * float(Y[h])
        pY += 1
    Kof = Gauss(XN, XY, Kof)
    return Kof


def CloseWindow():
    if messagebox.askokcancel("Закрыть", "Вы хотите завершить программу?"):
        root.destroy()
        root.quit()


def openfile():
    return askopenfilename()


def ChangeN():
    global Npolinom
    Npolinom = tk.simpledialog.askinteger(title="Степень Полинома",
                                          prompt="Введите степень полинома, который вам нужен")


def DefaultPolinom():
    global Kof
    global Choice
    CheckChoice(1)
    Choice = 1
    Kof = Simple(DataX, DataY, Npolinom)
    EntryProgramm()


def EntryProgramm():
    global previousResult
    global out
    Result = ""
    out = [i for i in range(len(Kof))]

    for i in range(0, len(Kof)):
        if E > 0:
            a = Kof[i]
            out[i] = round(Kof[i], E)
            Kof[i] = a
        else:
            out[i] = Kof[i]

    if Choice == 1:
        for i in range(0, len(Kof)):
            if i == 0 and Npolinom == 0:
                Result += "(" + str(out[i]) + ")"
            elif i == 0 and Npolinom != 1:
                Result += "(" + str(out[i]) + ")" + " + "
            elif i == 0 and Npolinom == 1:
                Result += "(" + str(out[i]) + ")" + " + "
            elif i == 1 and Npolinom != 1:
                Result += "(" + str(out[i]) + ")" + "*x + "
            elif i == 1 and Npolinom == 1:
                Result += "(" + str(out[i]) + ")" + "*x"
            elif i == len(Kof) - 1 and i != 0:
                Result += "(" + str(out[i]) + ")" + "*x^" + str(i)
            else:
                Result += "(" + str(out[i]) + ")" + "*x^" + str(i) + " + "

    if Choice == 2 or Choice == 3:
        dop = ""
        if Choice == 2:
            dop = "*sin("
        else:
            dop = "*cos("
        for i in range(0, Npolinom+1):
            if i == 0:
                Result += "(" + str(out[i]) + ")" + " + "
            elif i == Npolinom:
                Result += "(" + str(out[i]) + ")" + dop + str(i) + "x)"
            else:
                Result += "(" + str(out[i]) + ")" + dop + str(i) + "x) + "
    if Choice == 4:
        dop = "ln(x+"
        for i in range(0, Npolinom+1):
            if i == 0:
                Result += "(" + str(out[i]) + ")" + " + "
            elif i == Npolinom:
                Result += "(" + str(out[i]) + ")" + dop + str(i) + ")"
            else:
                Result += "(" + str(out[i]) + ")" + dop + str(i) + ") + "
    if Choice == 5:
        dop = "sin("
        for i in range(0, Npolinom + 1):
            if i == 0:
                Result += "(" + str(out[i]) + ")" + " + "
            elif i == Npolinom:
                Result += "(" + str(out[i]) + ")" + dop + str(i/10) + "PI*x)"
            else:
                Result += "(" + str(out[i]) + ")" + dop + str(i/10) + "PI*x) + "
    entry_text.set("y = " + Result)
    if previousChoice > 0:
        previous_text.set("y0 = " + previousResult)
        SaveFile("Предыдущая апроксимируемая функция:\ny0 = " + previousResult +
                 "\nТекущая апроксимируемая функция:\ny = " + Result)
    else:
        SaveFile("Полученная апроксимируемая функция:\ny = " + Result)
    previousResult = Result


def TrigFunc(kf, x):
    res = 0
    if Choice == 2:
        res = math.sin(kf * x)
    if Choice == 3:
        res = math.cos(kf * x)
    if Choice == 4:
        res = math.log(x+kf)
    if Choice == 5:
        res = math.sin(kf / 10 * math.pi * x)
    return res


def TRIG(i, j, x):
    result = 0
    if i == 0 and j == 0:
        result = 1
    elif i == 0:
        result = TrigFunc(j, x)
    elif j == 0:
        result = TrigFunc(i, x)
    else:
        result = TRIG(i, 0, x) * TRIG(0, j, x)
    return result


def SinPolinom():
    global Choice
    CheckChoice(2)
    Choice = 2
    TRIGPolinom()


def CosPolinom():
    global Choice
    CheckChoice(3)
    Choice = 3
    TRIGPolinom()


def LogPolinom():
    global Choice
    CheckChoice(4)
    Choice = 4
    TRIGPolinom()


def PiPolinom():
    global Choice
    CheckChoice(5)
    Choice = 5
    TRIGPolinom()


def TRIGPolinom():
    global Kof
    n = len(DataX)
    Kof = numpy.zeros(Npolinom+1)
    XN = numpy.zeros((Npolinom+1, Npolinom+1))
    XY = numpy.zeros(Npolinom+1)
    addXN, addXY = 0, 0
    for i in range(0, len(XN)):
        for j in range(0, len(XN[0])):
            for k in range(0, len(DataX)):
                    addXN += TRIG(i, j, DataX[k])
            XN[i, j] = addXN
            addXN = 0
        for p in range(0, len(DataY)):
                addXY += DataY[p] * TRIG(i, 0, DataX[p])
        XY[i] = addXY
        addXY = 0
    Kof = Gauss(XN, XY, Kof)
    # pprint(Kof)
    EntryProgramm()


def NewY(X):
    Y = 0
    for i in range(0, len(Kof)):
        if Choice == 1:
            Y += Kof[i] * (X**i)
        # if Choice == 2 or Choice == 3 or Choice == 4 :
        else:
            if i != 0:
                Y += Kof[i] * TrigFunc(i, X)
            else:
                Y += Kof[i]
    return Y


def StartGraf():
    plt.scatter(DataX, DataY, color='r', label='Исходные точки')
    plt.xlabel("Ось абсцисс")
    plt.ylabel("Ось ординат")
    plt.title("Загруженные данные")
    plt.legend()
    plt.grid()
    plt.show()
    plt.clf()


def CreateGraf():
    global oldDataX
    global oldNewDataY
    NewDataY = [0] * len(DataY)
    for i in range(0, len(DataX)):
        NewDataY[i] = NewY(float(DataX[i]))

    plt.plot(DataX, DataY, color='b', label='Загруженные точки')
    plt.plot(DataX, NewDataY, color='r', label='Текущая Апроксимируемая функция')
    if previousChoice > 0:
        plt.plot(oldDataX, oldNewDataY, color='g', label='Предыдущая Апроксимируемая функция')
    plt.xlabel("Ось абсцисс")
    plt.ylabel("Ось ординат")
    plt.title("Сравнение графиков")
    plt.legend()
    plt.grid()
    plt.show()
    plt.clf()

    plt.scatter(DataX, DataY, color='b', label='Загруженные точки')
    plt.plot(DataX, NewDataY, color='r', label='Апроксимируемая функция')
    if previousChoice > 0:
        plt.plot(oldDataX, oldNewDataY, color='g', label='Предыдущая Апроксимируемая функция')
    plt.xlabel("Ось абсцисс")
    plt.ylabel("Ось ординат")
    plt.title("Сравнение апроксимируемых графиков с исходными точками")
    plt.legend()
    plt.grid()
    plt.show()

    oldDataX = DataX
    oldNewDataY = NewDataY


def SaveFile(Result):
    USER_NAME = getpass.getuser()
    path = r'C:\Users\%s\Desktop\РезультатМНК.txt' % USER_NAME
    f = open(path, 'w')
    f.write(Result)
    f.close()
    messagebox.showinfo("Файл с результатом МНК", "Результат был сохранен на Рабочем столе с именем РезультатМНК.txt")


def CheckChoice(NewChoice):
    global previousChoice
    global previousKof
    if Choice > 0:
        # print(Choice)
        previousChoice = Choice
        previousKof = Kof


def ReadFile():
    DataX = []
    DataY = []
    global errorinput
    errorinput = 1
    with open(file) as File:
        CountLine = 0
        for line in File:
            if CountLine % 2 == 0:
                DataX += line.split()
            else:
                DataY += line.split()
            CountLine += 1
    checkDataX = [DataX[i].lower() for i in range(0, len(DataX))]
    checkDataY = [DataY[i].lower() for i in range(0, len(DataY))]
    DataX = checkDataX
    DataY = checkDataY
    for i in range(0, len(DataX)):
        if DataX[i] != "x":
            errorinput = CheckInputFile(DataX[i])
            if errorinput == -1:
                break
        if DataY[i] != "y":
            errorinput = CheckInputFile(DataY[i])
            if errorinput == -1:
                break
        if errorinput == -1:
            break
    if errorinput != -1:
        for char in DataX:
            DeleteXorY(char, DataX)
        for char in DataY:
            DeleteXorY(char, DataY)
        for i in range(0, len(DataX)):
            DataX[i] = float(DataX[i])
            DataY[i] = float(DataY[i])
        DataX = np.array(DataX)
        DataY = np.array(DataY)
        SortDataX = sorted(DataX)
        SortDataY = [0] * len(DataY)
        for i in range(0, len(DataX)):
            for j in range(0, len(DataX)):
                if DataX[i] == SortDataX[j]:
                    SortDataY[j] = DataY[i]
        DataX = SortDataX
        DataY = SortDataY
    return DataX, DataY


def ChangeE():
    global E
    E = tk.simpledialog.askinteger(title="Количество знаков после запятой",
                                          prompt="Введите число знаков, которое вам нужно")


def Latex():
    f = tk.simpledialog.askinteger(title="Запрос масштаба",
                                   prompt="Введите масштаб формулы, положительное число")
    x = sympy.symbols('x')
    ln = sympy.symbols('ln')
    y = 0
    if Choice == 1:
        for i in range(0, len(Kof)):
            if i == 0:
                y += out[i]
            elif i == 1:
                y += out[i] * x
            else:
                y += out[i] * (x ** i)
    elif Choice == 2:
        for i in range(0, len(Kof)):
            if i == 0:
                y += out[i]
            elif i == 1:
                y += out[i] * sympy.sin(x)
            else:
                y += out[i] * sympy.sin(i*x)
    elif Choice == 3:
        for i in range(0, len(Kof)):
            if i == 0:
                y += out[i]
            elif i == 1:
                y += out[i] * sympy.cos(x)
            else:
                y += out[i] * sympy.cos(i*x)
    elif Choice == 4:
        for i in range(0, len(Kof)):
            if i == 0:
                y += out[i]
            else:
                y += out[i] * ln * (x+i)
    elif Choice == 5:
        for i in range(0, len(Kof)):
            if i == 0:
                y += out[i]
            else:
                y += out[i] * sympy.sin(i / 10 * sympy.pi * x)

    lat = sympy.latex(y)
    plt.text(0, 0.6, r"$%s$" % lat, fontsize=f)
    fig = plt.gca()
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.spines['top'].set_visible(False)
    fig.axes.spines['right'].set_visible(False)
    fig.axes.spines['bottom'].set_visible(False)
    fig.axes.spines['left'].set_visible(False)
    plt.draw()
    plt.show()
    # plt.clear()


root = tk.Tk()
root.title("Метод Наименьших Квадратов")
# root.attributes("-fullscreen", True)
root.geometry("1500x700")
root.protocol("WM_DELETE_WINDOW", CloseWindow)
file = ""
while errorinput != 1:
    file = ""
    while not file.lower().endswith('.txt'):
        file = askopenfilename(parent=root, title='Choose a file')
        if not file:
            root.destroy()
            print("Пользователь не загрузил файл и закончил программу")
            sys.exit()
        elif not file.lower().endswith('.txt'):
            messagebox.showerror("Error", "Неверный формат файла!")
            messagebox.showerror("Формат файла не .txt", "Вы загрузили файл:\n" + file)
    messagebox.showinfo("Успешно", "Вы загрузили файл\n" + file)
    DataX, DataY = ReadFile()

StartGraf()
Npolinom = tk.simpledialog.askinteger(title="Степень Полинома",
                                      prompt="Введите степень полинома, который вам нужен")
label = ttk.Label(text="Выберите полином для апроксимации: ", font=("Times New Roman", 20), foreground="#800000")
labelKof = ttk.Label(text="Результат: ", font=("Times New Roman", 18), foreground="#800000")
labelPreviousKof = ttk.Label(text="Предыдущий\nрезультат: ", font=("Times New Roman", 18), foreground="#800000")
label.pack()
labelPreviousKof.place(x=100, y=150)
labelKof.place(x=100, y=270)

DefaultButton = ttk.Button(root, text="Степенной Полином", command=DefaultPolinom)
ButtonSin = ttk.Button(root, text="Полином с синусами", command=SinPolinom)
ButtonCos = ttk.Button(root, text="Полином с косинусами", command=CosPolinom)
Button4 = ttk.Button(root, text="Полином с логарифмами", command=LogPolinom)
Button5 = ttk.Button(root, text="Полином с числом Пи", command=PiPolinom)
CloseButton = ttk.Button(root, text="Закрыть Программу", command=CloseWindow)
ButtonChangeN = ttk.Button(root, text="Изменить степень полинома", command=ChangeN)
ButtonGraf = ttk.Button(root, text="Построить графики", command=CreateGraf)
ButtonE = ttk.Button(root, text="Знаки после запятой", command=ChangeE)
ButtonLatex = ttk.Button(root, text="Latex-формула", command=Latex)
# ButtonSave = ttk.Button(root, text="Сохранить на Рабочем столе", command=SaveFile())
# ButtonTwoGraf = ttk.Button(root, text="Построить две апроксимации", command=CreateGraf)

DefaultButton.place(x=100, y=50, width=150, height=70)
ButtonSin.place(x=340, y=50, width=150, height=70)
ButtonCos.place(x=580, y=50, width=150, height=70)
Button4.place(x=820, y=50, width=150, height=70)
Button5.place(x=1060, y=50, width=170, height=70)
CloseButton.place(x=1300, y=50, width=150, height=70)
ButtonChangeN.place(x=100, y=400, width=170, height=70)
ButtonGraf.place(x=340, y=400, width=150, height=70)
ButtonE.place(x=580, y=400, width=150, height=70)
ButtonLatex.place(x=820, y=400, width=150, height=70)
# ButtonTwoGraf.place(x=580, y=250, width=150, height=70)
# ButtonSave.place(x=580, y=250, width=200, height=70)

entry_text = tk.StringVar()
previous_text = tk.StringVar()
EntryResult = tk.Entry(root, textvariable=entry_text, state="disabled", font=("Times New Roman", 14))
EntryResult.place(x=250, y=270, width=1200, height=70)
EntryPreviousResult = tk.Entry(root, textvariable=previous_text, state="disabled", font=("Times New Roman", 14))
EntryPreviousResult.place(x=250, y=150, width=1200, height=70)

root.mainloop()
