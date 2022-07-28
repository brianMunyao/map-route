import sys
import os

import folium
from PyQt5.QtWidgets import QApplication, QWidget,  QComboBox, QPushButton, QLabel
from PyQt5.QtWidgets import QFormLayout

from graph import Graph
from utils import TOWNS,  getCoordForList, getCoordPath, getDistance, getPath, getPathDistance

# vertices and edges
g = Graph()
dictTowns = getCoordForList(TOWNS)

nbi = g.addNode('Nairobi')
msa = g.addNode('Mombasa')
ksm = g.addNode('Kisumu')
eld = g.addNode('Eldoret')
kti = g.addNode('Kitui')
mak = g.addNode('Makueni')
nkr = g.addNode('Nakuru')
nyk = g.addNode('Nanyuki')
lmu = g.addNode('Kilifi')
gsa = g.addNode('Garissa')

g.addEdge(nbi, nkr, getDistance('Nairobi', 'Nakuru'))
g.addEdge(nbi, ksm, getDistance('Nairobi', 'Kisumu'))
g.addEdge(nbi, msa, getDistance('Nairobi', 'Mombasa'))
g.addEdge(nbi, kti, getDistance('Nairobi', 'Kitui'))
g.addEdge(nbi, nyk, getDistance('Nairobi', 'Nanyuki'))
g.addEdge(nbi, mak, getDistance('Nairobi', 'Makueni'))
g.addEdge(msa, lmu, getDistance('Mombasa', 'Kilifi'))
g.addEdge(nkr, ksm, getDistance('Nakuru', 'Kisumu'))
g.addEdge(nkr, nyk, getDistance('Nakuru', 'Nanyuki'))
g.addEdge(nkr, eld, getDistance('Nakuru', 'Eldoret'))
g.addEdge(kti, lmu, getDistance('Kitui', 'Kilifi'))
g.addEdge(kti, mak, getDistance('Kitui', 'Makueni'))
g.addEdge(kti, gsa, getDistance('Kitui', 'Garissa'))
g.addEdge(gsa, lmu, getDistance('Garissa', 'Kilifi'))
g.addEdge(nyk, gsa, getDistance('Nanyuki', 'Garissa'))
g.addEdge(eld, ksm, getDistance('Eldoret', 'Kisumu'))
g.addEdge(eld, nyk, getDistance('Eldoret', 'Nanyuki'))

# GUI
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Map Routes')
window.setGeometry(100, 100, 280, 80)

formLayout = QFormLayout()

cbxStart = QComboBox(window)
cbxStart.addItems(TOWNS)
cbxStart.setMaximumWidth(200)

cbxGoal = QComboBox(window)
cbxGoal.addItems(TOWNS)
cbxGoal.setMaximumWidth(200)

cbxAlgo = QComboBox(window)
cbxAlgo.addItems(('Breadth First Search', 'Depth First Search', 'A* Search'))
cbxAlgo.setMaximumWidth(200)

lblResult = QLabel(window)


formLayout.addRow("Start:", cbxStart)
formLayout.addRow("Goal:", cbxGoal)
formLayout.addRow("Algorithm:", cbxAlgo)
formLayout.setVerticalSpacing(17)


def recreate(lines):
    if os.path.exists("index.html"):
        os.remove("index.html")

    myMap = folium.Map(zoom_start=7, location=(-1.2832533,
                       36.8172449))

    for key in dictTowns:
        folium.Marker(
            dictTowns[key], tooltip=f'<strong>{key}</strong>').add_to(myMap)

    if lines:
        polyLine = folium.PolyLine(locations=lines, weight=5)
        myMap.add_child(polyLine)
    myMap.save('index.html')


recreate(False)


def getRoute(graph):
    startPoint = cbxStart.currentText()
    endPoint = cbxGoal.currentText()
    algorithm = cbxAlgo.currentText()

    map_route = getPath(graph, startPoint, endPoint, algorithm)
    totalDist = getPathDistance(map_route)
    lblResult.setText(f'{startPoint} -> {endPoint} = {totalDist}')

    co = getCoordPath(dictTowns, map_route)
    recreate(co)


btn = QPushButton(window, text='Get Route')
btn.setMaximumWidth(280)
btn.clicked.connect(lambda: getRoute(g))
formLayout.addRow(lblResult)
formLayout.addRow(btn)


window.setLayout(formLayout)
window.show()
sys.exit(app.exec_())
