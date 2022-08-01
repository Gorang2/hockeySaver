import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *#QWidget,  QDesktopWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidgetItem, QTableWidget, QRadioButton, QGridLayout
from PyQt5.QtCore import *
import csv

from MyQTableWidgetItem import MyQPushButton

DURATION_INT = 1200
PENALTY_DURATION = 120
class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		self.period = '1'
		self.homeState = set()
		self.homeState.add("Tie")
		self.homeState.add("1p")
		self.homeState.add("5on5")
		self.homePlayerCount = 5
		self.awayPlayerCount = 5
		self.awayState = set()
		self.awayState.add("Tie")
		self.awayState.add("1p")
		self.awayState.add('5on5')
		self.homeScore = 0
		self.awayScore = 0
		self.homeTeam = 'home'
		self.awayTeam = 'away'
		self.homePenaltyOne = 0
		self.homePenaltyTwo = 0
		self.awayPenaltyOne = 0
		self.awayPenaltyTwo = 0
		self.gameData = []
		self.selectedPlayer = ''
		self.selectedTeam = ''
		self.action = ''
		self.initUI()

	def initUI(self):
		self.setWindowTitle('SuperSaver')

		self.setFocusPolicy(Qt.StrongFocus)
		self.setCursor(Qt.ArrowCursor)
		self.root = QVBoxLayout()

		self.renderGameInfo() #render self.gameInfoSection
		self.renderRinkAndDataSection() #render self.rinkAndDataSection
		self.renderDataButtonSection()
		self.setTimer()
		self.setLayout(self.root)
		self.setFocus()
		self.showFullScreen()
	
	def renderDataButtonSection(self):
		#슛, 패스, 턴오버, 체킹, 골, 패스/리시브미스
		self.dataButtonSection = QHBoxLayout()
		self.homeSection = QVBoxLayout()

		self.homeDataLabelSection = QHBoxLayout()
		self.homeLabel = QLabel("홈")
		self.homeFrame = QFrame()
		self.homeFrame.setStyleSheet(".QFrame { border : 1px solid grey }")
		self.homeFrame.setLayout(self.homeSection)
		self.homeLabel.setAlignment(Qt.AlignCenter)
		self.homeDataLabelSection.addWidget(self.homeLabel, stretch=1)

		self.homeDataButtonSection = QHBoxLayout()
		self.homeDataButtonSectionOne = QVBoxLayout()
		self.homeDataButtonSectionTwo = QVBoxLayout()

		self.homeShotButton = QPushButton("슛\n(Q)")
		self.homeShotButton.clicked.connect(lambda : self.handleAction(self.homeTeam, 'shot'))
		self.homePassButton = QPushButton("패스\n(W)")
		self.homePassButton.clicked.connect(lambda : self.handleAction(self.homeTeam, 'pass'))
		self.homeCheckButton = QPushButton("체킹\n(E)")
		self.homeCheckButton.clicked.connect(lambda : self.handleAction(self.homeTeam, 'check'))
		self.homeGoalButton = QPushButton("골\n(R)")
		self.homeGoalButton.clicked.connect(lambda : self.handleAction(self.homeTeam, 'goal'))
		self.homeTurnOverButton = QPushButton("턴오버\n(T)")
		self.homeTurnOverButton.clicked.connect(lambda : self.handleAction(self.homeTeam, 'turnOver'))
		self.homePassMissButton = QPushButton("패스/리시브미스\n(Y)")
		self.homePassMissButton.clicked.connect(lambda : self.handleAction(self.homeTeam, 'passMiss'))

		self.homeDataButtonSectionOne.addWidget(self.homeShotButton)
		self.homeDataButtonSectionOne.addWidget(self.homePassButton)
		self.homeDataButtonSectionOne.addWidget(self.homeCheckButton)
		self.homeDataButtonSectionTwo.addWidget(self.homeGoalButton)
		self.homeDataButtonSectionTwo.addWidget(self.homeTurnOverButton)
		self.homeDataButtonSectionTwo.addWidget(self.homePassMissButton)

		self.homeDataButtonSection.addLayout(self.homeDataButtonSectionOne)
		self.homeDataButtonSection.addLayout(self.homeDataButtonSectionTwo)

		self.homeSection.addLayout(self.homeDataLabelSection, stretch=1)
		self.homeSection.addLayout(self.homeDataButtonSection, stretch=2)

		self.awaySection = QVBoxLayout()

		self.awayDataLabelSection = QHBoxLayout()
		self.awayLabel = QLabel("어웨이")
		self.awayFrame = QFrame()
		self.awayFrame.setStyleSheet(".QFrame { border : 1px solid grey }")
		self.awayFrame.setLayout(self.awaySection)
		self.awayLabel.setAlignment(Qt.AlignCenter)
		self.awayDataLabelSection.addWidget(self.awayLabel, stretch=1)

		self.awayDataButtonSection = QHBoxLayout()
		self.awayDataButtonSectionOne = QVBoxLayout()
		self.awayDataButtonSectionTwo = QVBoxLayout()

		self.awayShotButton = QPushButton("슛\n(A)")
		self.awayShotButton.clicked.connect(lambda : self.handleAction(self.awayTeam, 'shot'))
		self.awayPassButton = QPushButton("패스\n(S)")
		self.awayPassButton.clicked.connect(lambda : self.handleAction(self.awayTeam, 'pass'))
		self.awayCheckButton = QPushButton("체킹\n(D)")
		self.awayCheckButton.clicked.connect(lambda : self.handleAction(self.awayTeam, 'check'))
		self.awayGoalButton = QPushButton("골\n(F)")
		self.awayGoalButton.clicked.connect(lambda : self.handleAction(self.awayTeam, 'goal'))
		self.awayTurnOverButton = QPushButton("턴오버\n(G)")
		self.awayGoalButton.clicked.connect(lambda : self.handleAction(self.awayTeam, 'turnOver'))
		self.awayPassMissButton = QPushButton("패스/리시브미스\n(H)")
		self.awayPassMissButton.clicked.connect(lambda : self.handleAction(self.awayTeam, 'passMiss'))

		self.awayDataButtonSectionOne.addWidget(self.awayShotButton)
		self.awayDataButtonSectionOne.addWidget(self.awayPassButton)
		self.awayDataButtonSectionOne.addWidget(self.awayCheckButton)
		self.awayDataButtonSectionTwo.addWidget(self.awayGoalButton)
		self.awayDataButtonSectionTwo.addWidget(self.awayTurnOverButton)
		self.awayDataButtonSectionTwo.addWidget(self.awayPassMissButton)

		self.awayDataButtonSection.addLayout(self.awayDataButtonSectionOne)
		self.awayDataButtonSection.addLayout(self.awayDataButtonSectionTwo)

		self.awaySection.addLayout(self.awayDataLabelSection, stretch=1)
		self.awaySection.addLayout(self.awayDataButtonSection, stretch=2)

		self.selectSection = QVBoxLayout()
		self.selectedLabel = QLabel("현재 입력된 기록이 없습니다.")
		self.selectedLabel.setStyleSheet("font-size : 25px")
		self.selectedLabel.setAlignment(Qt.AlignCenter)
		self.selectSection.addWidget(self.selectedLabel)

		self.selectInput = QLineEdit()
		self.selectInput.setFixedHeight(50)
		self.selectInput.setStyleSheet('font-size : 30')
		self.selectInput.setAlignment(Qt.AlignCenter)
		self.selectInput.setPlaceholderText("기록할 동작을 한 선수의 등번호 입력(선택)")
		self.selectInput.returnPressed.connect(self.handleSelectPlayer)
		self.selectSection.addWidget(self.selectInput)

		self.infoLabel = QLabel("순서\n\n1.버튼이나 단축키를 통해 기록할 동작 선택\n\n2.선수 입력(선택사항, 숫자 및 백스페이스 사용 가능)\n\n3.링크장 이미지 위에 동작 위치 클릭")
		self.infoLabel.setAlignment(Qt.AlignCenter)
		self.selectSection.addWidget(self.infoLabel)

		#self.dataButtonSection.addLayout(self.homeSection)
		self.dataButtonSection.addWidget(self.homeFrame)
		self.dataButtonSection.addLayout(self.selectSection)
		self.dataButtonSection.addWidget(self.awayFrame)
		self.dataButtonSection.addLayout(self.awayDataButtonSection)

		self.root.addLayout(self.dataButtonSection)
	
	def handleAction(self, team, action):
		self.selectedTeam = team
		self.action = action
	
		self.handleSelectedDisplay()

	def handleSelectPlayer(self):
		self.setFocus()
		self.selectedPlayer = self.selectInput.text()
		self.selectInput.clear()
		self.handleSelectedDisplay()

	def handleSelectedDisplay(self):
		if self.selectedTeam == '' or self.action == '':
			if self.selectedPlayer != '':
				self.selectedLabel.setText("선택된 선수 : {}".format(self.selectedPlayer))
			else:
				self.selectedLabel.setText("현재 입력된 기록이 없습니다.")
		else:
			self.selectedLabel.setText("현재 입력된 기록 : {} by {} {}번".format(self.action, self.selectedTeam, self.selectedPlayer))
	#KEYBOARD EVENT (ALL WIDGET)
	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Space:
			self.handleTimer()
		elif e.key() == Qt.Key_Q:
			self.handleAction(self.homeTeam, 'shot')
		elif e.key() == Qt.Key_A:
			self.handleAction(self.awayTeam, 'shot')
		elif Qt.Key_0 <= e.key() <= Qt.Key_9:
			self.selectedPlayer += str(e.key() - Qt.Key_0)
			self.handleSelectedDisplay()
		elif e.key() == Qt.Key_Backspace:
			self.selectedPlayer = self.selectedPlayer[:-1]
			self.handleSelectedDisplay()
		elif e.key() == Qt.Key_W:
			self.handleAction(self.homeTeam, 'pass')
		elif e.key() == Qt.Key_S:
			self.handleAction(self.awayTeam, 'pass')
		elif e.key() == Qt.Key_E:
			self.handleAction(self.homeTeam, 'check')
		elif e.key() == Qt.Key_D:
			self.handleAction(self.awayTeam, 'check')
		elif e.key() == Qt.Key_R:
			self.handleAction(self.homeTeam, 'goal')
		elif e.key() == Qt.Key_F:
			self.handleAction(self.awayTeam, 'goal')
		elif e.key() == Qt.Key_T:
			self.handleAction(self.homeTeam, 'turnOver')
		elif e.key() == Qt.Key_G:
			self.handleAction(self.awayTeam, 'turnOver')
		elif e.key() == Qt.Key_Y:
			self.handleAction(self.homeTeam, 'passMiss')
		elif e.key() == Qt.Key_H:
			self.handleAction(self.awayTeam, 'passMiss')

	#RENDER SCORE, TIMER, PERIOD BUTTON번
	def renderGameInfo(self):
		self.gameInfoSection = QHBoxLayout()
		self.renderTimeScoreSection()
		self.renderPeriodButtonSection()
		self.root.addLayout(self.gameInfoSection)
	
	#RENDER PERIOD BUTTONS
	def renderPeriodButtonSection(self):
		self.buttonSection = QVBoxLayout()
		self.periodButtonSection = QHBoxLayout()

		self.firstPeriodButton = QRadioButton()
		self.firstPeriodButton.setChecked(True)
		self.firstPeriodButton.setText("1st Period")
		self.firstPeriodButton.toggled.connect(self.firstPeriodChecked)

		self.secondPeriodButton = QRadioButton()
		self.secondPeriodButton.setText("2nd Period")
		self.secondPeriodButton.toggled.connect(self.secondPeriodChecked)

		self.thirdPeriodButton = QRadioButton()
		self.thirdPeriodButton.setText("3rd Period")
		self.thirdPeriodButton.toggled.connect(self.thirdPeriodChecked)
		
		self.OverTimeButton = QRadioButton()
		self.OverTimeButton.setText("OT")
		self.OverTimeButton.toggled.connect(self.OverTimeChecked)

		self.renderPenaltySection()
		self.periodButtonSection.addStretch(1)
		self.periodButtonSection.addWidget(self.firstPeriodButton, stretch=1)
		self.periodButtonSection.addWidget(self.secondPeriodButton, stretch=1)
		self.periodButtonSection.addWidget(self.thirdPeriodButton, stretch=1)
		self.periodButtonSection.addWidget(self.OverTimeButton, stretch=1)
		
		self.buttonSection.addLayout(self.periodButtonSection)
		self.gameInfoSection.addLayout(self.buttonSection, stretch=1)

	def renderPenaltySection(self):
		self.penaltySection = QHBoxLayout()

		self.homePenaltySection = QVBoxLayout()

		self.homePenaltyLowerOne = QHBoxLayout()
		self.homePenaltyUpperOne = QHBoxLayout()
		self.homePenaltySectionOne = QVBoxLayout()
		self.homePenaltyBoxOne = QLineEdit()
		self.homePenaltyBoxOne.returnPressed.connect(lambda : self.handlePenalty("home1"))
		self.homePenaltyLabelOne = QLabel("home1")
		self.homePenaltyLabelOne.setAlignment(Qt.AlignCenter)
		self.homePenaltyTimerOne = QLCDNumber()
		self.homePenaltyTimerOne.display("2:00")
		self.homePenaltyTimerOne.setStyleSheet('background-color : black; color : yellow')
		self.homePenaltyButtonOne = QPushButton('제거')
		self.homePenaltyButtonOne.clicked.connect(lambda : self.handleDeletePenalty("home1"))
		
		self.homePenaltyLowerOne.addWidget(self.homePenaltyTimerOne, stretch=1)
		self.homePenaltyLowerOne.addWidget(self.homePenaltyButtonOne, stretch=1)

		self.homePenaltyUpperOne.addWidget(self.homePenaltyLabelOne, stretch=1)
		self.homePenaltyUpperOne.addWidget(self.homePenaltyBoxOne, stretch=1)

		self.homePenaltySectionOne.addLayout(self.homePenaltyUpperOne, stretch=1)
		self.homePenaltySectionOne.addLayout(self.homePenaltyLowerOne, stretch=1)		

		self.homePenaltySectionTwo = QVBoxLayout()

		self.homePenaltyUpperTwo = QHBoxLayout()
		self.homePenaltyLowerTwo = QHBoxLayout()
		self.homePenaltyBoxTwo = QLineEdit()
		self.homePenaltyBoxTwo.returnPressed.connect(lambda : self.handlePenalty("home2"))
		self.homePenaltyLabelTwo = QLabel("home2")
		self.homePenaltyLabelTwo.setAlignment(Qt.AlignCenter)
		self.homePenaltyTimerTwo = QLCDNumber()
		self.homePenaltyTimerTwo.setStyleSheet('background-color : black; color : yellow')
		self.homePenaltyTimerTwo.display("2:00")
		self.homePenaltyButtonTwo = QPushButton('제거')
		self.homePenaltyButtonTwo.clicked.connect(lambda : self.handleDeletePenalty("home2"))

		self.homePenaltyUpperTwo.addWidget(self.homePenaltyLabelTwo, stretch=1)
		self.homePenaltyUpperTwo.addWidget(self.homePenaltyBoxTwo, stretch=1)
		self.homePenaltyLowerTwo.addWidget(self.homePenaltyTimerTwo)
		self.homePenaltyLowerTwo.addWidget(self.homePenaltyButtonTwo)

		self.homePenaltySectionTwo.addLayout(self.homePenaltyUpperTwo, stretch=1)
		self.homePenaltySectionTwo.addLayout(self.homePenaltyLowerTwo, stretch=1)

		self.homePenaltySection.addLayout(self.homePenaltySectionOne, stretch=1)
		self.homePenaltySection.addLayout(self.homePenaltySectionTwo, stretch=1)
		#===================AWAY PENALTY SECTION=====================
		self.awayPenaltySection = QVBoxLayout()
		self.awayPenaltyUpperOne = QHBoxLayout()
		self.awayPenaltyLowerOne = QHBoxLayout()
		self.awayPenaltySectionOne = QVBoxLayout()
		self.awayPenaltyBoxOne = QLineEdit()
		self.awayPenaltyBoxOne.returnPressed.connect(lambda : self.handlePenalty("away1"))
		self.awayPenaltyLabelOne = QLabel("away1")
		self.awayPenaltyLabelOne.setAlignment(Qt.AlignCenter)
		self.awayPenaltyTimerOne = QLCDNumber()
		self.awayPenaltyTimerOne.setStyleSheet('background-color : black; color : yellow')
		self.awayPenaltyTimerOne.display("2:00")
		self.awayPenaltyButtonOne = QPushButton('제거')
		self.awayPenaltyButtonOne.clicked.connect(lambda : self.handleDeletePenalty("away1"))
		
		self.awayPenaltyLowerOne.addWidget(self.awayPenaltyTimerOne, stretch=1)
		self.awayPenaltyLowerOne.addWidget(self.awayPenaltyButtonOne, stretch=1)
		self.awayPenaltyUpperOne.addWidget(self.awayPenaltyLabelOne, stretch=1)
		self.awayPenaltyUpperOne.addWidget(self.awayPenaltyBoxOne, stretch=1)

		self.awayPenaltySectionOne.addLayout(self.awayPenaltyUpperOne, stretch=1)
		self.awayPenaltySectionOne.addLayout(self.awayPenaltyLowerOne, stretch=1)

		self.awayPenaltySectionTwo = QVBoxLayout()

		self.awayPenaltyUpperTwo = QHBoxLayout()
		self.awayPenaltyLowerTwo = QHBoxLayout()
		self.awayPenaltyBoxTwo = QLineEdit()
		self.awayPenaltyBoxTwo.returnPressed.connect(lambda : self.handlePenalty("away2"))
		self.awayPenaltyLabelTwo = QLabel("away2")
		self.awayPenaltyLabelTwo.setAlignment(Qt.AlignCenter)
		self.awayPenaltyTimerTwo = QLCDNumber()
		self.awayPenaltyTimerTwo.setStyleSheet('background-color : black; color : yellow')
		self.awayPenaltyTimerTwo.display("2:00")
		self.awayPenaltyButtonTwo = QPushButton('제거')
		self.awayPenaltyButtonTwo.clicked.connect(lambda : self.handleDeletePenalty("away2"))

		self.awayPenaltyLowerTwo.addWidget(self.awayPenaltyTimerTwo, stretch=1)
		self.awayPenaltyLowerTwo.addWidget(self.awayPenaltyButtonTwo, stretch=1)
		self.awayPenaltyUpperTwo.addWidget(self.awayPenaltyLabelTwo, stretch=1)
		self.awayPenaltyUpperTwo.addWidget(self.awayPenaltyBoxTwo, stretch=1)

		self.awayPenaltySectionTwo.addLayout(self.awayPenaltyUpperTwo, stretch=1)
		self.awayPenaltySectionTwo.addLayout(self.awayPenaltyLowerTwo, stretch=1)

		self.awayPenaltySection.addLayout(self.awayPenaltySectionOne)
		self.awayPenaltySection.addLayout(self.awayPenaltySectionTwo)

		self.penaltySection.addLayout(self.homePenaltySection)
		self.penaltySection.addLayout(self.awayPenaltySection)

		self.buttonSection.addLayout(self.penaltySection, stretch=2)

	def handleHomePlayerCount(self, op):
		print("handle home player : {}".format(self.homeState))
		self.homeState.remove('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		self.awayState.remove('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		if (op == '+'):
			self.homePlayerCount += 1
		else:
			self.homePlayerCount -= 1
		self.homeState.add('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		self.awayState.add('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		print("after : {}".format(self.homeState))

	def handleAwayPlayerCount(self, op):
		self.homeState.remove('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		self.awayState.remove('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		if (op == '+'):
			self.awayPlayerCount += 1
		else:
			self.awayPlayerCount -= 1
		self.homeState.add('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))
		self.awayState.add('{}on{}'.format(self.homePlayerCount, self.awayPlayerCount))

	def handleDeletePenalty(self, section):
		if section == 'home1':
			if self.homePenaltyOne == 0:
				return 
			self.gameData.insert(0, ['PenaltyEnd', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.homeTeam, self.homePenaltyOne, list(self.homeState), list(self.awayState)])
			self.homePenaltyOne = 0
			self.homePenaltyOneTime = PENALTY_DURATION
			self.homePenaltyTimerOne.display("2:00")
			self.homePenaltyBoxOne.clear()
			self.handleHomePlayerCount('+')
			
		elif section == 'home2':
			if self.homePenaltyTwo == 0:
				return 
			self.gameData.insert(0, ['PenaltyEnd', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.homeTeam, self.homePenaltyTwo, list(self.homeState), list(self.awayState)])
			self.homePenaltyTwo = 0
			self.homePenaltyTwoTime = PENALTY_DURATION
			self.homePenaltyTimerTwo.display("2:00")
			self.homePenaltyBoxTwo.clear()
			self.handleHomePlayerCount('+')

		elif section == 'away1':
			if self.awayPenaltyOne == 0:
				return 
			self.gameData.insert(0, ['PenaltyEnd', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.awayTeam, self.awayPenaltyOne, list(self.homeState), list(self.awayState)])
			self.awayPenaltyOne = 0
			self.awayPenaltyOneTime = PENALTY_DURATION
			self.awayPenaltyTimerOne.display("2:00")
			self.awayPenaltyBoxOne.clear()
			self.handleAwayPlayerCount('+')
		elif section == 'away2' :
			if self.awayPenaltyTwo == 0:
				return 
			self.gameData.insert(0, ['PenaltyEnd', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.awayTeam, self.awayPenaltyTwo, list(self.homeState), list(self.awayState)])
			self.awayPenaltyTwo = 0
			self.awayPenaltyTwoTime = PENALTY_DURATION
			self.awayPenaltyTimerTwo.display("2:00")
			self.awayPenaltyBoxTwo.clear()
			self.handleAwayPlayerCount('+')
		self.reRenderTable()
	
	def handlePenalty(self, info):
		try:
			if info == 'home1':
				self.homePenaltyOne = int(self.homePenaltyBoxOne.text())
				self.gameData.insert(0, ['PenaltyStart', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.homeTeam, self.homePenaltyOne, list(self.homeState), list(self.awayState) ] )
				self.handleHomePlayerCount('-')	
			elif info == 'home2':
				self.homePenaltyTwo = int(self.homePenaltyBoxTwo.text())
				self.gameData.insert(0, ['PenaltyStart', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.homeTeam, self.homePenaltyTwo, list(self.homeState), list(self.awayState) ] )
				self.handleHomePlayerCount('-')	
			elif info == 'away1':
				self.awayPenaltyOne = int(self.awayPenaltyBoxOne.text())
				self.gameData.insert(0, ['PenaltyStart', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.awayTeam, self.awayPenaltyOne, list(self.homeState), list(self.awayState) ] )
				self.handleAwayPlayerCount('-')	
			elif info == 'away2':
				self.awayPenaltyTwo = int(self.awayPenaltyBoxTwo.text())
				self.gameData.insert(0, ['PenaltyStart', self.period, '{}:{}'.format(self.time_left//60, str(self.time_left%60).zfill(2)), self.awayTeam, self.awayPenaltyTwo, list(self.homeState), list(self.awayState) ] )
				self.handleAwayPlayerCount('-')	
			else:
				print("ERR in handlePenalty")
			self.reRenderTable()
		except Exception as e:
			print(e)
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setInformativeText("선수의 등번호를 입력하세요.")
			msg.setWindowTitle("오류")
			msg.setStyleSheet("QLabel { min-width : 75px }")
			msg.exec_()
		self.setFocus()

	#RENDER TIMER & SCORE
	def renderTimeScoreSection(self):
		self.timeScoreSection = QHBoxLayout()
		self.renderTimerSection()
		self.renderTimerHandleSection()
		self.renderScoreSection()		
		self.renderScoreButtonSection()
		self.gameInfoSection.addLayout(self.timeScoreSection, stretch = 2)

	#RENDER SCORE
	def renderScoreSection(self):
		self.scoreSection = QVBoxLayout()

		self.teamSection = QHBoxLayout()
		self.homeTeamInput = QLineEdit()
		self.homeTeamInput.setPlaceholderText("홈")
		self.homeTeamInput.setAlignment(Qt.AlignCenter)
		self.homeTeamInput.returnPressed.connect(self.handleTeamInput)
		self.homeTeamInput.setStyleSheet('font-size : 15px')
		self.awayTeamInput = QLineEdit()
		self.awayTeamInput.setPlaceholderText("어웨이")
		self.awayTeamInput.setAlignment(Qt.AlignCenter)
		self.awayTeamInput.returnPressed.connect(self.handleTeamInput)
		self.awayTeamInput.setStyleSheet('font-size : 15px')
		self.colonLabel = QLabel(' : ')

		self.teamSection.addWidget(self.homeTeamInput)
		self.teamSection.addWidget(self.colonLabel)
		self.teamSection.addWidget(self.awayTeamInput)

		self.score = QLabel(str(self.homeScore) +  ' : ' +str(self.awayScore))
		self.score.setAlignment(Qt.AlignCenter)
		self.score.setStyleSheet("background-color : black; font-size : 40px")

		self.scoreSection.addLayout(self.teamSection, stretch=1)
		self.scoreSection.addWidget(self.score, stretch=2)
		self.timeScoreSection.addLayout(self.scoreSection, stretch=1)

	def handleTeamInput(self):
		self.homeTeam = self.homeTeamInput.text()
		self.awayTeam = self.awayTeamInput.text()

		if self.homeTeam != '' :
			self.homeLabel.setText(self.homeTeam)
			self.homePenaltyLabelOne.setText(self.homeTeam+"1")
			self.homePenaltyLabelTwo.setText(self.homeTeam+"2")
		if self.awayTeam != '' :
			self.awayLabel.setText(self.awayTeam)
			self.awayPenaltyLabelOne.setText(self.awayTeam+"1")
			self.awayPenaltyLabelTwo.setText(self.awayTeam+"2")
		self.setFocus()

	#RENDER TIMER
	def renderTimerSection(self):
		self.gameTimer = QLCDNumber()
		self.gameTimer.display('20:00')
		self.gameTimer.setDigitCount(5)
		self.gameTimer.setStyleSheet("background-color : black; color : yellow; font-size : 40px;")
		self.timeScoreSection.addWidget(self.gameTimer, stretch=1)
		
	#RENDER BUTTONS FOR TIMER
	def renderTimerHandleSection(self):
		self.gameTimerInput = QLineEdit()
		self.gameTimerInput.setPlaceholderText("시간 변경 (mm:ss)")
		self.gameTimerInputButton = QPushButton('시간 변경')
		self.timerButton = QPushButton("시작\n(space)")
		self.timerButton.clicked.connect(self.handleTimer)

		self.gameTimerInput.returnPressed.connect(self.handleTimerEdit)
		self.gameTimerInputButton.clicked.connect(self.handleTimerEdit)

		self.timeHandleSection = QVBoxLayout()
		self.timeHandleSection.addWidget(self.timerButton)
		self.timeHandleSection.addWidget(self.gameTimerInput)
		self.timeHandleSection.addWidget(self.gameTimerInputButton)
		self.timeScoreSection.addLayout(self.timeHandleSection, stretch=1)
	
	#HANDLER FOR TIMER
	def handleTimerEdit(self):
		try:
			min, sec = self.gameTimerInput.text().split(":")
			gap = self.time_left - int(min)*60-int(sec)
			print(gap, self.homePenaltyOneTime)
			if gap < 0 and self.homePenaltyOneTime + abs(gap) > 120:
				self.homePenaltyOneTime = 1
				self.handleHomePlayerCount('+')
			elif gap > 0 and self.homePenaltyOneTime - abs(gap) < 0:
				tmp = self.time_left
				self.time_left -= self.homePenaltyOneTime
				self.handleDeletePenalty('home1')
				self.time_left = tmp
			else :
				self.homePenaltyOneTime -= gap

			if gap < 0 and self.homePenaltyTwoTime + abs(gap) > 120:
				self.handleAwayPlayerCount('+')
				self.homePenaltyTwoTime = 1
			elif gap > 0 and self.homePenaltyTwoTime - abs(gap) < 0:
				tmp = self.time_left
				self.time_left -= self.homePenaltyTwoTime
				self.handleDeletePenalty('home2')
				self.time_left = tmp
			else :
				self.homePenaltyTwoTime -= gap

			if gap < 0 and self.awayPenaltyOneTime + abs(gap) > 120:
				self.awayPenaltyOneTime = 1
			elif gap > 0 and self.awayPenaltyOneTime - abs(gap) < 0:
				tmp = self.time_left
				self.time_left -= self.awayPenaltyOneTime
				self.handleDeletePenalty('away1')
				self.time_left = tmp
			else :
				self.awayPenaltyOneTime -= gap

			if gap < 0 and self.awayPenaltyTwoTime + abs(gap) > 120:
				self.awayPenaltyTwoTime = 1
			elif gap > 0 and self.awayPenaltyTwoTime - abs(gap) < 0:
				tmp = self.time_left
				self.time_left -= self.awayPenaltyTwoTime
				self.handleDeletePenalty('away2')
				self.time_left = tmp
			else :
				self.awayPenaltyTwoTime -= gap

			self.time_left = int(min)*60 + int(sec)
			if (self.time_left > 1200 or self.time_left <= 0):
				self.time_left = 1200
				self.gameTimerInput.clear()	
				self.setFocus()
			else :
				self.gameTimerInput.clear()
				self.gameTimer.display(min+":"+sec)
				self.setFocus()
		
		except:
			self.gameTimerInput.clear()
			self.setFocus()
			return

	#RENDER SCORE IN/DECREASE BUTTONS
	def renderScoreButtonSection(self):
		self.homeScoreButtonSection = QVBoxLayout()
		self.homeIncreaseButton = QPushButton('홈 스코어 증가\n+')
		self.homeDecreaseButton = QPushButton('홈 스코어 감소\n-')
		self.homeIncreaseButton.clicked.connect(lambda : self.handleIncrease(self.homeTeam))
		self.homeDecreaseButton.clicked.connect(lambda : self.handleDecrease(self.homeTeam))
		self.homeScoreButtonSection.addWidget(self.homeIncreaseButton)
		self.homeScoreButtonSection.addWidget(self.homeDecreaseButton)

		self.awayScoreButtonSection = QVBoxLayout()
		self.awayIncreaseButton = QPushButton('어웨이 스코어 증가\n+')
		self.awayDecreaseButton = QPushButton('어웨이 스코어 감소\n-')
		self.awayIncreaseButton.clicked.connect(lambda : self.handleIncrease(self.awayTeam))
		self.awayDecreaseButton.clicked.connect(lambda : self.handleDecrease(self.awayTeam))

		self.awayScoreButtonSection.addWidget(self.awayIncreaseButton)
		self.awayScoreButtonSection.addWidget(self.awayDecreaseButton)

		self.timeScoreSection.addLayout(self.homeScoreButtonSection, stretch=1)
		self.timeScoreSection.addLayout(self.awayScoreButtonSection, stretch=1)

	#INCREASE HANDLER
	def handleIncrease(self, team):
		if team==self.homeTeam:
			self.homeScore += 1
		else:
			self.awayScore += 1
		self.handleScoreState()
		self.score.setText(str(self.homeScore)+' : '+str(self.awayScore))
	
	#DECREASE HANDLER
	def handleDecrease(self, team):
		if team=='home' and self.homeScore > 0:
			self.homeScore -= 1
		elif team=='away' and self.awayScore > 0:
			self.awayScore -= 1

		self.handleScoreState()
		self.score.setText(str(self.homeScore)+' : '+str(self.awayScore))
	
	def handleScoreState(self):
		if (self.homeScore == self.awayScore):
			try:
				self.homeState.remove("Winning")
				self.awayState.remove("Losing")
			except:
				self.homeState.remove("Losing")
				self.awayState.remove("Winning")
			self.homeState.add("Tie")
			self.awayState.add("Tie")
		
		elif self.homeScore < self.awayScore:
			try:
				self.homeState.remove("Tie")
				self.awayState.remove("Tie")
				self.homeState.add("Losing")
				self.awayState.add("Winning")
			except:
				pass
		
		elif self.homeScore > self.awayScore:
			try:
				self.homeState.remove("Tie")
				self.awayState.remove("Tie")
				self.awayState.add("Losing")
				self.homeState.add("Winning")
			except:
				pass

	#INIT TIMER	
	def setTimer(self):
		self.timer = QTimer(self)
		self.time_left = DURATION_INT
		self.homePenaltyOneTime = PENALTY_DURATION
		self.homePenaltyTwoTime = PENALTY_DURATION
		self.awayPenaltyOneTime = PENALTY_DURATION
		self.awayPenaltyTwoTime = PENALTY_DURATION
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.timeout)

	#TIMER SETTINGS
	def timeout(self):
		if self.timer.isActive() == False:
			return
		self.time_left -= 1
		if self.homePenaltyOne > 0:
			self.homePenaltyOneTime -= 1
			if self.homePenaltyOneTime == 0:
				self.handleHomePlayerCount('+')
				self.homePenaltyOne = 0
				self.homePenaltyOneTime = PENALTY_DURATION
				self.homePenaltyBoxOne.clear()
				self.homePenaltyTimerOne.display("2:00")
			else :
				self.homePenaltyTimerOne.display("{}:{}".format(self.homePenaltyOneTime//60, self.homePenaltyOneTime%60))
		if self.homePenaltyTwo > 0:
			self.homePenaltyTwoTime -= 1
			if self.homePenaltyTwoTime == 0:
				self.handleHomePlyaerCount('+')
				self.homePenaltyTwo = 0
				self.homePenaltyTwoTime = PENALTY_DURATION
				self.homePenaltyBoxTwo.clear()
				self.homePenaltyTimerTwo.display("2:00")
			else:
				self.homePenaltyTimerTwo.display("{}:{}".format(self.homePenaltyTwoTime//60, self.homePenaltyTwoTime%60))
		if self.awayPenaltyOne > 0:
			self.awayPenaltyOneTime -= 1
			if self.awayPenaltyOneTime == 0:
				self.handleAwayPlayerCount('+')
				self.awayPenaltyOne = 0
				self.awayPenaltyOneTime = PENALTY_DURATION
				self.awayPenaltyBoxOne.clear()
				self.awayPenaltyTimerOne.display("2:00")
			else:
				self.awayPenaltyTimerOne.display("{}:{}".format(self.awayPenaltyOneTime//60, self.awayPenaltyOneTime%60))
			
		if self.awayPenaltyTwo > 0:
			self.awayPenaltyTwoTime -= 1
			if self.awayPenaltyTwoTime == 0:
				self.handleAwayPlayerCount('-')
				self.awayPenaltyTwo = 0
				self.awayPenaltyTwoTime = PENALTY_DURATION
				self.awayPenaltyBoxTwo.clear()
				self.awayPenaltyTimerTwo.display("2:00")
			else:
				self.awayPenaltyTimerTwo.display("{}:{}".format(self.awayPenaltyTwoTime//60, self.awayPenaltyTwoTime%60))

		if self.time_left == 0:
			self.time_left = DURATION_INT
			self.timer.stop()
			if self.period == '1':
				self.period = '2'
				self.secondPeriodButton.setChecked(True)
			elif self.period == '2':
				self.period = '3'
				self.thirdPeriodButton.setChecked(True)
			elif self.period == '3':
				self.period = 'OT'
			self.gameTimer.display("20:00")
		else:
			self.gameTimer.display("{}:{}".format(self.time_left // 60, self.time_left % 60))

	#TIMER BUTTON HANDLER
	def handleTimer(self):
		if self.timer.isActive():
			self.timerButton.setText("시작\nspace")
			self.timer.stop()
		else :
			self.timer.start()
			self.timerButton.setText("일시정지\nspace")
		self.timerButton.update()

	#PERIOD INDICATORS
	def firstPeriodChecked(self, checked):
		print(list(self.homeState), list(self.awayState))
		self.period = '1'
		self.homeState.add("1p")
		self.awayState.add("1p")
		try:
			try:
				self.homeState.remove("2p")
				self.awayState.remove("2p")
			except:
				pass
			try:
				self.homeState.remove("OT")
				self.awayState.remove("OT")
			except : 
				pass
			try:
				self.homeState.remove("3p")
				self.awayState.remove("3p")
			except :
				pass
		except:
			pass
			
	
	def secondPeriodChecked(self, checked):
		self.period = '2'
		self.homeState.add("2p")
		self.awayState.add("2p")
		try:
			try:
				self.homeState.remove("1p")
				self.awayState.remove("1p")
			except:
				pass
			try:
				self.homeState.remove("3p")
				self.awayState.remove("3p")
			except : 
				pass
			try:
				self.homeState.remove("OT")
				self.awayState.remove("OT")
			except :
				pass
		except:
			pass
	
	def thirdPeriodChecked(self, checked):
		self.period = '3'
		self.homeState.add("3p")
		self.awayState.add("3p")
		try:
			try:
				self.homeState.remove("1p")
				self.awayState.remove("1p")
			except:
				pass
			try:
				self.homeState.remove("OT")
				self.awayState.remove("OT")
			except : 
				pass
			try:
				self.homeState.remove("2p")
				self.awayState.remove("2p")
			except :
				pass
		except:
			pass
	
	def OverTimeChecked(self, checked):
		self.period = 'OT'
		self.homeState.add("OT")
		self.awayState.add("OT")
		try:
			try:
				self.homeState.remove("2p")
				self.awayState.remove("2p")
			except:
				pass
			try:
				self.homeState.remove("1p")
				self.awayState.remove("1p")
			except : 
				pass
			try:
				self.homeState.remove("3p")
				self.awayState.remove("3p")
			except :
				pass
		except:
			pass
	
	#RINK AND TABLE RENDER
	def renderRinkAndDataSection(self):
		self.rinkAndDataSection = QHBoxLayout()
		self.renderRink() #render self.iceRink
		self.renderTableSection() #render self.dataTable
		self.root.addLayout(self.rinkAndDataSection)

	#RENDER TABLE & DELETE
	def renderTableSection(self):
		self.tableSection = QVBoxLayout()
		self.renderTableEditSection()
		self.renderTable()
		self.rinkAndDataSection.addLayout(self.tableSection)

	#RENDER TABLE
	def renderTable(self):
		self.dataTable = QTableWidget(0, 5)
		self.dataTable.setHorizontalHeaderLabels(['종류', '피리어드', '시간', '팀', '번호'])

		header = self.dataTable.horizontalHeader()
		header.setSectionResizeMode(QHeaderView.Stretch)

		self.dataTable.setRowCount(len(self.gameData))
		#self.dataTable.setFixedSize(screen.size().width() - 1000, 435)

		self.tableSpan = QHBoxLayout()
		self.tableSpan.addWidget(self.dataTable)
		self.tableSection.addLayout(self.tableSpan)
	
	def renderTableEditSection(self):
		self.TableEditSection = QHBoxLayout()
		self.deleteInput = QLineEdit()
		self.deleteInput.setPlaceholderText("삭제할 행의 번호를 입력하세요.")
		self.deleteInput.returnPressed.connect(lambda : self.handleTableDelete(self.deleteInput.text()))
		self.deleteInput.setFocusPolicy(Qt.StrongFocus)

		self.deleteButton = QPushButton('삭제')
		self.deleteButton.clicked.connect(self.handleTableDelete)
		self.saveButton = QPushButton('테이블 csv로 저장 ..')
		self.saveButton.clicked.connect(self.handleTableSave)
		self.TableEditSection.addWidget(self.deleteInput, stretch=2)
		self.TableEditSection.addWidget(self.deleteButton, stretch=1)
		self.TableEditSection.addWidget(self.saveButton)
		self.tableSection.addLayout(self.TableEditSection)

	def handleTableDelete(self, index):
		try:
			del self.gameData[int(index) - 1]
			self.dataTable.removeRow(int(index)-1)
			self.deleteInput.clear()
		except Exception as e:
			print(e)
			self.deleteInput.clear()
			return
		self.reRenderTable()

	def handleTableSave(self):
		try:
			name = QFileDialog.getSaveFileName(self, 'Save')
			file = open('{}.csv'.format(name[0]), 'w', encoding='utf-8')
			w = csv.writer(file)
			for i in self.gameData:
				w.writerow(i)
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setInformativeText("저장되었습니다.")
			msg.setWindowTitle("알림")
			msg.setStyleSheet("QLabel { min-width : 75px }")
			msg.exec_()	
			file.close()
		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setInformativeText("예기치 못한 오류가 발생했습니다.")
			msg.setWindowTitle("오류")
			msg.setStyleSheet("QLabel { min-width : 75px }")
			msg.exec_()
		
		
	def renderRink(self):
		self.iceRink = QLabel(self)
		pixmap = QPixmap("./test.png").scaledToWidth(800)
		self.iceRink.setPixmap(pixmap)
		self.iceRink.setStyleSheet("background-color : blue")
		self.rinkAndDataSection.addWidget(self.iceRink)
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.iceRink.mousePressEvent = self.RinkClicked
	
	def RinkClicked(self, event):
		if self.timer.isActive() == False or self.action == '':
			return
		self.gameData.insert(0, [self.action, self.period, "{}:{}".format(self.time_left // 60, str(self.time_left % 60).zfill(2)), self.selectedTeam, self.selectedPlayer, event.pos().x()/800*60, event.pos().y()/400*30, list(self.homeState), list(self.awayState)])
		if self.action == 'goal':
			self.handleIncrease(self.selectedTeam)
			self.timer.stop()
		self.selectedTeam = ''
		self.selectedPlayer = ''
		self.action = ''
		self.handleSelectedDisplay()
		self.reRenderTable()
	
	def reRenderTable(self):
		print(self.gameData)
		self.dataTable.setRowCount(len(self.gameData))
		for i in range(len(self.gameData)):
			for j in range(5):
				self.dataTable.setItem(i, j, QTableWidgetItem(str(self.gameData[i][j])))
		self.dataTable.update()

	def renderControlSection(self):
		self.controlSection = QHBoxLayout()
		root.addLayout(self.controlSection, stretch=1)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())