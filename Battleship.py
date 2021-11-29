from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtWidgets import QLineEdit, QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout, QGridLayout, QDateEdit
import sys
import random

class Button(QToolButton): # 이 부분은 mycalc 실습 코드를 그대로 가져왔습니다

    def __init__(self, text,callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Battleship(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATTLESHIP GAME")

        self.totalLayout = QGridLayout() #제목, AI의 필드, 사용자의 필드, 재시작 버튼을 위한 전체 레이아웃 선언
        self.totalLayout.setSizeConstraint(QLayout.SetFixedSize)

        #제목 레이아웃
        self.titleGrid = QGridLayout()
        self.titleLabel = QLabel("<WELCOME TO BATTLESHIP GAME>",self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleGrid.addWidget(self.titleLabel,0,0)
        self.totalLayout.addLayout(self.titleGrid,0,0)

        #AI 필드 구성
        self.gridAI = QGridLayout()

        for i in range(10):
            for j in range(10):
                self.gridAI.addWidget(Button("?",self.AIButtonClicked),i,j)
        self.totalLayout.addLayout(self.gridAI,1,0)

        self.messageLayout = QGridLayout()
        self.messageLine = QLineEdit()
        self.messageLine.setReadOnly(True)
        self.messageLine.setText("Welcome To Battleship Game!!!")
        self.messageLayout.addWidget(self.messageLine,0,0)
        self.totalLayout.addLayout(self.messageLayout,2,0)


        #사용자 필드 구성 + ai 선박배치
        self.gridUser = QGridLayout()

        for i in range(10):
            for j in range(10):
                self.gridUser.addWidget(Button("X", self.buttonClicked), i, j)

        self.hori = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.verti = [1, 2, 3, 4, 5, 6, 7, 8]
        self.user_sample = []
        self.user_selected = []
        self.ai_sample = []
        self.ai_selected = []
        for p in self.verti:
            for q in self.hori:
                self.user_sample.append((p, q))
                self.ai_sample.append((p,q))

        for s in range (3):
            (i,j) = random.choice(self.user_sample)
            self.user_selected.append((i,j))
            self.user_selected.append((i-1,j))
            self.user_selected.append((i+1,j))
            (p,q) = random.choice(self.ai_sample)
            self.ai_selected.append((p, q))
            self.ai_selected.append((p-1, q))
            self.ai_selected.append((p+1, q))

            if (2 < p < 7):
                try:
                    self.remove_Dup_ai(p - 2, p + 3, q)
                except Exception as e:
                    print(e)

            elif (p < 3):
                try:
                    self.remove_Dup_ai(1, p + 2, q)
                except Exception as e:
                    print(e)
            else:
                try:
                    self.remove_Dup_ai(p - 2, 8, q)
                except Exception as e:
                    print(e)
            self.gridUser.addWidget(Button("O", self.buttonClicked), i, j)
            self.gridUser.addWidget(Button("O", self.buttonClicked), i-1, j)
            self.gridUser.addWidget(Button("O", self.buttonClicked), i+1, j)

            if (2 < i < 7):
                try:
                    self.remove_Dup_user(i - 2, i + 3, j)
                except Exception as e:
                    print(e)

            elif (i < 3):
                try:
                    self.remove_Dup_user(1, i + 2, j)
                except Exception as e:
                    print(e)

            else:
                try:
                    self.remove_Dup_user(i - 2, 8, j)
                except Exception as e:
                    print(e)

        print("AI SHIP:" + str(self.ai_selected))
        print("PLAYER SHIP:" + str(self.user_selected))
        self.totalLayout.addLayout(self.gridUser,1,2)

        self.date = QDateEdit()
        self.dateLayout = QGridLayout()
        self.date.setDate(QDate.currentDate())
        self.dateLayout.addWidget(self.date,0,0)
        self.totalLayout.addLayout(self.dateLayout,2,1)

        #재시작 버튼 레이아웃
        self.restartLayout = QGridLayout()
        self.restartButton = Button("Restart",self.Gameplay)
        self.restartLayout.addWidget(self.restartButton,0,0)
        self.totalLayout.addLayout(self.restartLayout,2,2)

        self.attacked_location = []
        self.vertical = [x for x in range(10)]
        for p in self.vertical:
            for q in self.hori:
                self.attacked_location.append((p, q))

        self.connect = False
        self.click = False
        self.i8 = False
        self.setLayout(self.totalLayout)
        self.setGeometry(300,300,300,200)
        self.onCenter()

    def onCenter(self):
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().top()
        frame.moveTop(center)
        self.move(frame.topLeft())

    def remove_Dup_user(self, m, n, j):  # m = i-2 n = i+2
        for k in range(m, n + 1):
            #print("removed : " + str((k, j)))
            self.user_sample.remove((k, j))

    def remove_Dup_ai(self, m, n, j):  # m = i-2 n = i+2
        for k in range(m, n + 1):
            #print("removed : " + str((k, j)))
            self.ai_sample.remove((k, j))

    def AIButtonClicked(self): #ai가 공격을 당하는 경우
        btn = self.sender()
        i = (btn.y()-29)//44
        j = (btn.x()-11)//44
        pos = (i,j)
        self.successBtn = Button("*", self.AIButtonClicked)
        self.failBtn = Button("X", self.AIButtonClicked)
        self.guessBtn = Button("G1", self.AIButtonClicked)
        self.guessBtn2 = Button("G2", self.AIButtonClicked)
        self.guessBtn3 = Button("G3", self.AIButtonClicked)
        self.guessBtn4 = Button("G4", self.AIButtonClicked)

        if pos in self.ai_selected:
            self.gridAI.addWidget(self.successBtn, i, j)
            self.messageLine.setText("Guessed. 1 More Chance.")
            self.successBtn.setDisabled(True)
            self.ai_selected.remove(pos)
        else:
            self.gridAI.addWidget(self.failBtn, i, j)
            self.messageLine.setText("Failed. AI Takes Chance.")
            self.failBtn.setDisabled(True)
            self.attack_by_ai()
        if len(self.ai_selected) == 0:
            for i in range(10):
                for j in range(10):
                    endBtn = Button("!",self.AIButtonClicked)
                    self.gridAI.addWidget(endBtn,i,j)
                    endBtn.setDisabled(True)
            self.messageLine.setText("YOU WIN ! CLICK RESTART TO REPLAY!")

        #print("(i,j) = " + str(pos))

    def Gameplay(self):
        self.close()
        self.BTS = Battleship()
        self.BTS.show()

    def buttonClicked(self):
        pass

    def attack_by_ai(self) :
        (i, j) = random.choice(self.attacked_location)
        print("attack : "+ str((i,j)))

        if ((i,j) in self.user_selected) :

            if self.connect == True:
                self.hit3(self.save[0], self.save[1])
                self.connect = False
                try:
                    pos = (self.save[0], self.save[1])
                    self.user_selected.remove(pos)
                except Exception as e:
                    print(e)

            if self.click == True:
                self.hit2(i - self.m, j)
                self.hit3(i - 2 * self.m, j)
                self.click = False


            if (1<i<8) :
                self.hit(i,j)
                option = [+1,-1]
                m = random.choice(option)
                self.middle_attack_tactics(m,i,j)

            elif (i==1): #이거 지리적인 위치 고려해보면 (i+1,j)는 무조건 보장이 되는 위치 따라서 바로 공격
                option_a = [-1, +2]
                self.hit(i,j)
                self.hit2(i+1,j)
                p = random.choice(option_a)

                if (p == -1):
                    if ((i-1,j) in self.user_selected):
                        self.hit3(i-1,j)

                    else :
                        self.failBtn.releaseMouse()
                        #self.hit2(i+2,j)

                if (p == +2):
                    if ((i+2,j) in self.user_selected):
                        self.hit3(i+2,j)

            elif (i == 8) :
                option_b = [+1,-2]
                self.hit(i, j)
                self.hit2(i-1,j)
                q = random.choice(option_b)
                if (q == +1):
                    if ((i+1,j) in self.user_selected):
                        self.hit3(i+1,j)

                    else :
                        self.failBtn.releaseMouse()

                if (q == -2):
                    if ((i-2,j) in self.user_selected):
                        self.hit3(i-2,j)


            elif (i == 0) :
                self.hit(i,j)
                self.hit2(i+1,j)
                self.hit3(i+2,j)

            elif (i == 9) :
                self.hit(i,j)
                self.hit2(i-1,j)
                self.hit3(i-2,j)

        else:
            if self.connect == True:
                self.hit3(self.save[0], self.save[1])
                self.connect = False
                try:
                    pos = (self.save[0], self.save[1])
                    self.user_selected.remove(pos)
                except Exception as e:
                    print(e)
            if self.click == True:
                self.hit2(i - self.m, j)
                self.hit3(i - 2 * self.m, j)
                self.click = False

            self.gridUser.addWidget(self.guessBtn, i, j)
            self.guessBtn.setDisabled(True)

        self.attacked_location.remove((i,j))

        if len(self.user_selected) == 0:
            for i in range(10):
                for j in range(10):
                    endBtn = Button("!",self.AIButtonClicked)
                    self.gridAI.addWidget(endBtn,i,j)
                    endBtn.setDisabled(True)
            self.messageLine.setText("YOU LOSE ! CLICK RESTART TO REPLAY!")

    def hit(self,a,b):
        self.gridUser.addWidget(self.guessBtn2, a, b)
        self.guessBtn2.setDisabled(True)
        pos = (a,b)
        print("hit pos : " +str(pos))
        try:
            self.user_selected.remove((a,b))
        except Exception as e:
            print(e)

    def hit2 (self,a,b):
        self.gridUser.addWidget(self.guessBtn3, a, b)
        self.guessBtn3.setDisabled(True)
        pos = (a,b)
        try:
            self.user_selected.remove((a,b))
        except Exception as e:
            print(e)
        print("hit pos : " +str(pos))

    def hit3 (self,a,b):
        self.gridUser.addWidget(self.guessBtn4, a, b)
        self.guessBtn4.setDisabled(True)
        pos = (a,b)
        try:
            self.user_selected.remove((a,b))
        except Exception as e:
            print(e)
        print("hit pos : " +str(pos))


    def middle_attack_tactics(self,m,i,j): #m=+1
        if ((i + m, j) in self.user_selected):
            self.hit2(i + m, j)
            if ((i + 2*m , j) in self.user_selected):
                self.hit3(i + 2*m , j)
            else:
                self.failBtn.releaseMouse()
                self.save = []
                self.save.append(int(i-m))
                self.save.append(int(j))
                self.connect = True
        else:
            self.click = True
            self.m = m

if __name__ == '__main__':
   app = QApplication(sys.argv)
   bts = Battleship()
   bts.show()
   sys.exit(app.exec_())