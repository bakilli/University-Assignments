import sys

import docx2txt
import networkx as nx
import pandas as pd
import pdfrw
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton,
    QDoubleSpinBox,
    QVBoxLayout,
    QComboBox,
    QFileDialog,
)
from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QAction,
    QFormLayout,
    QHeaderView,
    QTextEdit,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from parameters_score import calculate_rouge, start


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GRAF TABANLI METİN ÖZETLEME UYGULAMASI")
        self.create_menu()
        self.setMinimumSize(1350, 750)
        self.open = Window()
        self.setCentralWidget(self.open)
        self.show()

    def create_menu(self):
        menubar = self.menuBar()

        user_interface = menubar.addMenu("Yeni Pencere")
        query_screen = QAction("Graf Görselleştirici", self)
        user_interface.addAction(query_screen)
        user_interface.triggered.connect(self.response)

    def response(self, action):
        if action.text() == "Graf Görselleştirici":
            tabtitle = action.text()
            self.open.new_tab(user_interface(), tabtitle)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(user_interface(), "Ana Pencere")
        self.tabwidget.setTabsClosable(True)
        h_box = QHBoxLayout()
        h_box.addWidget(self.tabwidget)
        self.setLayout(h_box)
        self.tabwidget.tabCloseRequested.connect(self.close_function)
        self.show()

    def close_function(self, index):
        self.tabwidget.removeTab(index)

    def new_tab(self, w_name, tabtitle):
        self.tabwidget.addTab(w_name, tabtitle)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class user_interface(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # sadece okunabilir
        self.text_edit2 = QTextEdit(self)
        self.text_edit2.setReadOnly(True)
        self.text_edit3 = QTextEdit(self)
        self.text_edit3.setReadOnly(True)
        self.text_edit3.setFixedHeight(
            30
        )  # İstenilen boyutu burada belirleyebilirsiniz

        self.color = ["red", "green", "blue", "yellow"]

        self.content = ""
        self.threshold = 0.4
        self.threshold2 = 0.5  # başlangıçta varsayılan eşleşme eşiği
        # sentences = self.get_sentences(content)

        button1 = QPushButton("Dosya Seç", self)
        button1.clicked.connect(self.open_file_dialog)

        button2 = QPushButton("Dosyayı Graf Olarak Görüntüle", self)
        button2.clicked.connect(self.Draw_graf)

        button3 = QPushButton("Özetle", self)
        button3.clicked.connect(self.summer)
        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Word Embedding")
        self.dropdown.addItem("Bert")
        self.dropdown.currentIndexChanged.connect(self.dropdown_selection_changed)

        self.display_sentences(self.content)
        # threshold değeri için bir QDoubleSpinBox aracı ekleniyor
        self.threshold_spinbox = QDoubleSpinBox(self)
        self.threshold_spinbox.setValue(self.threshold)
        self.threshold_spinbox.setSingleStep(0.1)
        self.threshold_spinbox.setMinimum(0)
        self.threshold_spinbox.setMaximum(1)
        self.threshold_spinbox.setDecimals(2)
        self.threshold_spinbox2 = QDoubleSpinBox(self)
        self.threshold_spinbox2.setValue(self.threshold2)
        self.threshold_spinbox2.setSingleStep(0.1)
        self.threshold_spinbox2.setMinimum(0)
        self.threshold_spinbox2.setMaximum(1)
        self.threshold_spinbox2.setDecimals(2)

        self.threshold_spinbox.valueChanged.connect(
            self.threshold_spinbox_value_changed
        )
        self.threshold_spinbox2.valueChanged.connect(
            self.threshold_spinbox2_value_changed
        )
        f_box.addRow("Cümle Benzerliği Tresholdu:", self.threshold_spinbox)
        f_box.addRow("Cümle Skoru Tresholdu:", self.threshold_spinbox2)
        f_box.addWidget(self.dropdown)

        f_box.addRow("Cümleler:", self.text_edit)
        f_box.addRow("Özet:", self.text_edit2)
        f_box.addRow("Rouge Skoru :", self.text_edit3)
        h_box.addWidget(button1)
        h_box.addWidget(button2)
        h_box.addWidget(button3)
        main_layout = QVBoxLayout()
        main_layout.addLayout(f_box)
        main_layout.addLayout(h_box)

        self.setLayout(main_layout)

    def set_number(self, number):
        self.text_edit3.clear()
        self.text_edit3.append(str(number))

    def threshold_spinbox_value_changed(self, value):
        self.threshold = value  # Yeni threshold değerini güncelle

    def threshold_spinbox2_value_changed(self, value):
        self.threshold2 = value

    def dropdown_selection_changed(self, index):
        selected_option = self.dropdown.currentText()
        print("Seçilen seçenek:", selected_option)

    def display_sentences(self, sentences):
        self.text_edit.clear()
        title = self.content.split("\n")[0]
        if self.content == title:
            title = ""
        self.text_edit.append(f"TITLE ~~>" + title)
        doc = self.content
        if title != "":
            doc = self.content.replace(title + "\n", "")
        doc = doc.replace("\n", " ").strip()
        for i, sentence in enumerate(doc.split(".")):
            if sentence != "":
                self.text_edit.append(f"{i}.~~>" + sentence.strip())

    def summer(self):
        title = self.content.split("\n")[0]
        # everything except the title
        doc = self.content
        if title != "":
            doc = self.content.replace(title + "\n", "")
        doc = doc.replace("\n", " ").strip()
        if self.dropdown.currentText() == "Word Embedding":
            isBert = False
        else:
            isBert = True
        (
            summary_text,
            sentences,
            sentence_scores,
            node_connection_scores,
            top_terms,
            connection_count
        ) = start(
            doc,
            title,
            self.threshold,
            self.threshold2,
            isBert,
        )
        self.text_edit2.clear()
        # for i, sentence in enumerate(summary_text):
        self.text_edit2.append(summary_text)
        if summary_text != "":
            self.open_file_dialog_for_summary()
            self.set_number(calculate_rouge(summary_text, self.content2)[0]["rouge-1"]["f"])

    def Draw_graf(self):
        G = nx.complete_graph(len(self.content.split(".")))
        labels = {}
        for i, line in enumerate(self.content.split(".")):
            labels[i] = line.strip()
        nx.set_node_attributes(G, labels, "label")

        fig = Figure(figsize=(5, 5), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.text(
            0.5,
            1.05,
            self.dropdown.currentText(),
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(
                facecolor="lightblue", edgecolor="white", boxstyle="round,pad=0.5"
            ),
        )
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, ax=ax)
        title = self.content.split("\n")[0]
        # everything except the title
        doc = self.content
        if title != "":
            doc = self.content.replace(title + "\n", "")
        doc = doc.replace("\n", " ").strip()
        if self.dropdown.currentText() == "Word Embedding":
            isBert = False
        else:
            isBert = True
        (
            summary_text,
            sentences,
            sentence_scores,
            node_connection_scores,
            top_terms,
            connection_count
        ) = start(doc, title, self.threshold, self.threshold2, isBert)
        lastColor = ""
        for edge in G.edges:
            i, j = edge  # Düğüm indeksleri
            if i < len(node_connection_scores) and j < len(node_connection_scores[0]):
                # if i>=node_connection_scores.shape
                text = "{:.2f}".format(node_connection_scores[i][j])

                if node_connection_scores[i][j] >= self.threshold:
                    lastColor = self.color[1]
                else:
                    lastColor = self.color[3]
                ax.annotate(
                    text,
                    xy=(
                        (pos[edge[0]][0] + pos[edge[1]][0]) / 2,
                        (pos[edge[0]][1] + pos[edge[1]][1]) / 2,
                    ),
                    xytext=(0, 0),
                    textcoords="offset points",
                    ha="center",
                    va="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc=lastColor, alpha=1),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.5"),
                )
        canvas.draw()

        def onclick(event):
            x, y = event.xdata, event.ydata
            for node, coords in pos.items():
                distance = ((coords[0] - x) ** 2 + (coords[1] - y) ** 2) ** 0.5
                if distance < 0.05:
                    msg_box = QtWidgets.QMessageBox()
                    msg_box.setWindowTitle(f"{node}. cümlenin diğer cümlerle skoru")
                    msg_box.setText("Cümle: " + labels[node] + ".")

                    # Create a QDialog to hold the table
                    dialog = QtWidgets.QDialog()
                    dialog.setWindowTitle("Table")
                    dialog.setMinimumSize(950, 550)
                    layout = QtWidgets.QVBoxLayout(dialog)

                    # Create the table
                    self.table = QtWidgets.QTableView()

                    # Configure the table
                    self.table.horizontalHeader().setStretchLastSection(True)
                    self.table.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch
                    )

                    # Populate the table
                    # split the content to title and content
                    title = self.content.split("\n")[0]
                    # everything except the title
                    doc = self.content
                    if title != "":
                        doc = self.content.replace(title + "\n", "")
                    doc = doc.replace("\n", " ").strip()
                    if self.dropdown.currentText() == "Word Embedding":
                        isBert = False
                    else:
                        isBert = True
                    (
                        summary_text,
                        sentences,
                        sentence_scores,
                        node_connection_scores,
                        top_terms,
                        connection_count
                    ) = start(
                        doc,
                        title,
                        self.threshold_spinbox.value(),
                        self.threshold_spinbox2.value(),
                        isBert,
                    )
                    print(sentence_scores)
                    # Combine Sentence_scores and connection_count
                    data = []
                    for i, sentence in enumerate(sentences):
                        data.append(
                            [
                                sentence_scores[i][0],
                                sentence_scores[i][1],
                                sentence_scores[i][2],
                                sentence_scores[i][3],
                                sentence_scores[i][4],
                                sentence_scores[i][5],
                                connection_count[i],
                            ]
                        )

                    columns = [
                        "özel isim",
                        "sayısal değer",
                        "node bağlantı kontrolü",
                        "başlıktaki kelimeyi içeriyor mu",
                        "kelime frekansı(tf-idf)",
                        "Son Skor",
                        "Bağlantılı Cümle Sayısı"
                    ]
                    df = pd.DataFrame(data, columns=columns)
                    self.model = TableModel(df)
                    self.table.setModel(self.model)

                    # Add the table to the layout
                    layout.addWidget(self.table)

                    # Add the layout to the dialog
                    dialog.setLayout(layout)

                    # Show the dialog
                    if dialog.exec_() == QtWidgets.QDialog.Accepted:
                        pass  # Handle the dialog closing

        cid = fig.canvas.mpl_connect("button_press_event", onclick)
        canvas.show()

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Dosya Seç",
            "",
            "Metin Dosyaları (*.txt);;Word Dosyaları (*.docx);;PDF Dosyaları (*.pdf);;Tüm Dosyalar (*.*)",
        )

        if filename.endswith(".txt"):
            with open(filename, "r") as f:
                self.content = f.read()
        elif filename.endswith(".docx"):
            self.content = docx2txt.process(filename)
        elif filename.endswith(".pdf"):
            pdf_file = pdfrw.PdfReader(filename)
            self.content = ""
            for page in pdf_file.pages:
                for obj in page["/Resources"]["/Font"]:
                    if (
                        isinstance(obj, pdfrw.objects.pdfname.PdfName)
                        and str(obj) == "/TrueType"
                    ):
                        continue
                    elif isinstance(obj, pdfrw.objects.pdfname.PdfName):
                        continue
                    elif (
                        isinstance(obj, pdfrw.objects.pdfdict.PdfDict)
                        and obj.get("/Subtype") == "/TrueType"
                    ):
                        font = obj["/BaseFont"]
                        text = obj["/Encoding"]["/Differences"][2:]
                        self.content += text.decode(font)

        print(self.content)
        self.display_sentences(self.content)

    def open_file_dialog_for_summary(self):
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Dosya Seç",
            "",
            "Metin Dosyaları (*.txt);;Word Dosyaları (*.docx);;PDF Dosyaları (*.pdf);;Tüm Dosyalar (*.*)",
        )

        if filename.endswith(".txt"):
            with open(filename, "r") as f:
                self.content2 = f.read()
        elif filename.endswith(".docx"):
            self.content2 = docx2txt.process(filename)
        elif filename.endswith(".pdf"):
            pdf_file = pdfrw.PdfReader(filename)
            self.content2 = ""
            for page in pdf_file.pages:
                for obj in page["/Resources"]["/Font"]:
                    if (
                        isinstance(obj, pdfrw.objects.pdfname.PdfName)
                        and str(obj) == "/TrueType"
                    ):
                        continue
                    elif isinstance(obj, pdfrw.objects.pdfname.PdfName):
                        continue
                    elif (
                        isinstance(obj, pdfrw.objects.pdfdict.PdfDict)
                        and obj.get("/Subtype") == "/TrueType"
                    ):
                        font = obj["/BaseFont"]
                        text = obj["/Encoding"]["/Differences"][2:]
                        self.content2 += text.decode(font)


# class SubWindow(QWidget):
#     def __init__(self,):
#         super().__init__()
#         self.setWindowTitle("Thread Manager")
#         self.setMinimumSize(1280, 720)

# class SubWindow_csv(QWidget):
#     def __init__(self,):
#         super().__init__()
#         self.setWindowTitle("Result")
#         self.setMinimumSize(1280, 720)


def start_app():
    app = QApplication(sys.argv)

    Win = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_app()
