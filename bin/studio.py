"""
Authors:
Randy Heiland (heiland@iu.edu)
Adam Morrow, Michael Siler, Grant Waldrow, Drew Willis, Kim Crevecoeur
Dr. Paul Macklin (macklinp@iu.edu)

--- Versions ---
0.1 - initial version
"""
# https://doc.qt.io/qtforpython/gettingstarted.html

import os
import sys
import getopt
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
from xml.dom import minidom

# from matplotlib.colors import TwoSlopeNorm

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from config_tab import Config
from cell_def_tab import CellDef 
from microenv_tab import SubstrateDef 
from user_params_tab import UserParams 
from run_tab import RunModel 
from vis_tab import Vis 

class QHLine(QFrame):
    def __init__(self, sunken_flag):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameStyle(QFrame.NoFrame)
        if sunken_flag:
            self.setFrameShadow(QFrame.Sunken)

def SingleBrowse(self):
        # if len(self.csv) < 2:
    filePath = QFileDialog.getOpenFileName(self,'',".",'*.xml')

        #     if filePath != "" and not filePath in self.csv:
        #         self.csv.append(filePath)
        # print(self.csv)
  
#class PhysiCellXMLCreator(QTabWidget):
class PhysiCellXMLCreator(QWidget):
    # def __init__(self, parent = None):
    def __init__(self, show_vis_flag, parent = None):
        super(PhysiCellXMLCreator, self).__init__(parent)

        # self.nanohub = True
        self.nanohub_flag = False
        if( 'HOME' in os.environ.keys() ):
            self.nanohub_flag = "home/nanohub" in os.environ['HOME']


        # self.title_prefix = "PhysiCell Studio: "
        self.title_prefix = "test_normalize_studio: "
        # self.title_prefix = "PhysiCell Studio"
        self.setWindowTitle(self.title_prefix)

        # Menus
        vlayout = QVBoxLayout(self)
        # vlayout.setContentsMargins(5, 35, 5, 5)  # left,top,right,bottom
        vlayout.setContentsMargins(-1, 10, -1, -1)
        # if not self.nanohub_flag:
        if True:
            menuWidget = QWidget(self.menu())
            vlayout.addWidget(menuWidget)
            vlayout.addWidget(QHLine(False))
        # self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogNoButton')))
        # self.setWindowIcon(QtGui.QIcon('physicell_logo_25pct.png'))
        # self.grid = QGridLayout()
        # lay.addLayout(self.grid)
        self.setLayout(vlayout)

        self.resize(950, 770)  # width, height (height >= Cell Types|Death params)
        self.setMinimumSize(750, 770)  # width, height (height >= Cell Types|Death params)
        # self.setMinimumSize(1200, 770)  # width, height (height >= Cell Types|Death params)

        model_name = "PhysiCell_settings"

        # then what??
        # binDirectory = os.path.realpath(os.path.abspath(__file__))
        binDirectory = os.path.dirname(os.path.abspath(__file__))
        dataDirectory = os.path.join(binDirectory,'..','data')
        print("-------- dataDirectory (relative) =",dataDirectory)
        self.absolute_data_dir = os.path.abspath(dataDirectory)
        print("-------- absolute_data_dir =",self.absolute_data_dir)

        # NOTE: we set an env var here so in custom.cpp, it will also use it to read data (e.g., .csv)
        os.environ['KIDNEY_DATA_PATH'] = self.absolute_data_dir
        # dataDirectory = os.path.join(binDirectory,'..','config')
        # dataDirectory = os.path.join('.','config')

        # read_file = model_name + ".xml"
        # read_file = os.path.join(dataDirectory, model_name + ".xml")
        read_file = os.path.join(self.absolute_data_dir, model_name + ".xml")
        # self.setWindowTitle(self.title_prefix + model_name)


        # NOTE! We create a *copy* of the .xml sample model and will save to it.
        copy_file = "copy_" + model_name + ".xml"
        shutil.copy(read_file, copy_file)
        if self.nanohub_flag:
            # self.setWindowTitle(self.title_prefix + "pc4learning")
            self.setWindowTitle(self.title_prefix + copy_file)
        else:
            self.setWindowTitle(self.title_prefix + copy_file)
            # self.setWindowTitle(self.title_prefix + "pc4learning")
        # self.add_new_model(copy_file, True)
        # self.config_file = "config_samples/" + name + ".xml"
        self.config_file = copy_file  # to Save
        print("-----  __init__():  self.config_file = ",self.config_file)


        # self.config_file = read_file  # nanoHUB... to Save
        # self.tree = ET.parse(self.config_file)
        # fp = open(self.config_file)
        # self.tree = ET.parse(fp)
        # fp.close()

        with open(self.config_file, 'r') as xml_file:
            self.tree = ET.parse(xml_file)

        # tree = ET.parse(read_file)
        # self.tree = ET.parse(read_file)
        self.xml_root = self.tree.getroot()

        # self.template_cb()

        # self.num_models = 0
        # self.model = {}  # key: name, value:[read-only, tree]

        self.config_tab = Config(self.nanohub_flag)
        self.config_tab.xml_root = self.xml_root
        self.config_tab.fill_gui()

        self.microenv_tab = SubstrateDef()
        self.microenv_tab.xml_root = self.xml_root
        substrate_name = self.microenv_tab.first_substrate_name()
        print("studio.py: substrate_name=",substrate_name)
        self.microenv_tab.populate_tree()  # rwh: both fill_gui and populate_tree??

        # self.tab2.tree.setCurrentItem(QTreeWidgetItem,0)  # item

        self.celldef_tab = CellDef()
        self.celldef_tab.xml_root = self.xml_root
        cd_name = self.celldef_tab.first_cell_def_name()
        print("studio.py: cd_name=",cd_name)
        self.celldef_tab.populate_tree()
        self.celldef_tab.fill_substrates_comboboxes()
        # self.vis_tab.substrates_cbox_changed_cb(2)
        self.microenv_tab.celldef_tab = self.celldef_tab

        # self.cell_customdata_tab = CellCustomData()
        # self.cell_customdata_tab.xml_root = self.xml_root
        # self.cell_customdata_tab.celldef_tab = self.celldef_tab
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)
        # self.celldef_tab.fill_custom_data_tab()
        
        self.user_params_tab = UserParams()
        self.user_params_tab.xml_root = self.xml_root
        self.user_params_tab.fill_gui()

        # self.sbml_tab = SBMLParams()
        # self.sbml_tab.xml_root = self.xml_root
        # self.sbml_tab.fill_gui()


        # self.save_as_cb()

        self.tabWidget = QTabWidget()

        self.run_tab = RunModel(self.nanohub_flag, self.tabWidget)
        self.homedir = os.getcwd()
        print("studio.py: self.homedir = ",self.homedir)
        self.run_tab.homedir = self.homedir
        # self.run_tab.nanohub_flag = self.nanohub_flag

        # self.run_tab.xmin = 
        # self.run_tab.xmax = 

        #------------------
        # if self.nanohub_flag:  # to be able to fill_xml() from Run tab
        if True:  # to be able to fill_xml() from Run tab
            self.run_tab.config_tab = self.config_tab
            self.run_tab.microenv_tab = self.microenv_tab 
            self.run_tab.celldef_tab = self.celldef_tab
            self.run_tab.user_params_tab = self.user_params_tab
            self.run_tab.tree = self.tree

        #------------------
        # self.tabWidget = QTabWidget()
        stylesheet = """
            QTabBar::tab:selected {background: orange;}   #  dodgerblue
            """
        self.tabWidget.setStyleSheet(stylesheet)
        self.tabWidget.addTab(self.config_tab,"Config Basics")
        self.tabWidget.addTab(self.microenv_tab,"Microenvironment")
        self.tabWidget.addTab(self.celldef_tab,"Cell Types")
        # self.tabWidget.addTab(self.cell_customdata_tab,"Cell Custom Data")
        self.tabWidget.addTab(self.user_params_tab,"User Params")
        self.tabWidget.addTab(self.run_tab,"Run")
        if show_vis_flag:
            print("studio.py: creating vis_tab (Plot tab)")
            self.vis_tab = Vis(self.nanohub_flag)
            # self.vis_tab.setEnabled(False)
            # self.vis_tab.nanohub_flag = self.nanohub_flag
            # self.vis_tab.xml_root = self.xml_root
            self.tabWidget.addTab(self.vis_tab,"Plot")
            # self.tabWidget.setTabEnabled(5, False)
            self.enablePlotTab(False)

            self.run_tab.vis_tab = self.vis_tab
            print("studio.py: calling vis_tab.substrates_cbox_changed_cb(2)")
            self.vis_tab.fill_substrates_combobox(self.celldef_tab.substrate_list)
            # self.vis_tab.substrates_cbox_changed_cb(2)   # doesn't accomplish it; need to set index, but not sure when
            self.vis_tab.init_plot_range(self.config_tab)
            # self.vis_tab.show_edge = False

        vlayout.addWidget(self.tabWidget)
        # self.addTab(self.sbml_tab,"SBML")

        # self.tabWidget.setCurrentIndex(1)  # rwh/debug: select Microenv
        # self.tabWidget.setCurrentIndex(2)  # rwh/debug: select Cell Types
        if show_vis_flag:
            self.tabWidget.setCurrentIndex(0)    # Cconfig Basics
            # self.tabWidget.setCurrentIndex(2)    # Cell Types
            # self.tabWidget.setCurrentIndex(5)    # Plot
        else:
            self.tabWidget.setCurrentIndex(0)  # Config (default)

    def enablePlotTab(self, bval):
        self.tabWidget.setTabEnabled(5, bval)

    def menu(self):
        menubar = QMenuBar(self)
        menubar.setNativeMenuBar(False)

        menubar.adjustSize()  # Argh. Otherwise, only 1st menu appears, with ">>" to others!

    #-----------------------------------------------------------------
    def add_new_model(self, name, read_only):
        print("add_new_model: title suffix= ",name)
        self.setWindowTitle(self.title_prefix + name)

        #---------- rwh?
        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print("add_new_model(): self.tree = ET.parse(xml_file) for ",self.config_file)
        print("add_new_model(): self.tree = ET.parse(xml_file) for ",name)
        # with open(self.config_file, 'r') as xml_file:
        with open(name, 'r') as xml_file:
            self.tree = ET.parse(xml_file)
        # tree = ET.parse(read_file)
        # self.tree = ET.parse(read_file)
        self.xml_root = self.tree.getroot()

        # self.num_models = 0
        # self.model = {}  # key: name, value:[read-only, tree]

        #-------  Re-populate the GUI with the new model's params -------
        # self.config_tab = Config(self.nanohub_flag)
        self.config_tab.xml_root = self.xml_root
        self.config_tab.fill_gui()

        # self.microenv_tab = SubstrateDef()
        self.microenv_tab.xml_root = self.xml_root
        substrate_name = self.microenv_tab.first_substrate_name()
        print("studio.py: substrate_name=",substrate_name)
        self.microenv_tab.populate_tree()  # rwh: both fill_gui and populate_tree??

        # self.tab2.tree.setCurrentItem(QTreeWidgetItem,0)  # item

        # self.celldef_tab = CellDef()
        self.celldef_tab.xml_root = self.xml_root
        cd_name = self.celldef_tab.first_cell_def_name()
        print("studio.py: cd_name=",cd_name)
        self.celldef_tab.populate_tree()
        self.celldef_tab.fill_substrates_comboboxes()
        # self.vis_tab.substrates_cbox_changed_cb(2)
        self.microenv_tab.celldef_tab = self.celldef_tab

        # self.cell_customdata_tab = CellCustomData()
        # self.cell_customdata_tab.xml_root = self.xml_root
        # self.cell_customdata_tab.celldef_tab = self.celldef_tab
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)
        # self.celldef_tab.fill_custom_data_tab()
        
        # self.user_params_tab = UserParams()
        self.user_params_tab.xml_root = self.xml_root
        self.user_params_tab.fill_gui()


    def reset_xml_root(self):
        self.celldef_tab.param_d.clear()  # seems unnecessary as being done in populate_tree. argh.
        self.celldef_tab.clear_custom_data_tab()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("reset_xml_root(): after celldef_tab.param_d.clear(), param_d = ", self.celldef_tab.param_d)
        self.celldef_tab.current_cell_def = None
        # self.microenv_tab.param_d.clear()

        self.xml_root = self.tree.getroot()
        self.config_tab.xml_root = self.xml_root
        self.microenv_tab.xml_root = self.xml_root
        self.celldef_tab.xml_root = self.xml_root
        # self.cell_customdata_tab.xml_root = self.xml_root
        self.user_params_tab.xml_root = self.xml_root
        # self.run_tab.xml_root = self.xml_root

        # --------Now fill all tabs' params------
        self.config_tab.fill_gui()

        self.microenv_tab.clear_gui()
        self.microenv_tab.populate_tree()
        # self.microenv_tab.fill_gui(None)
        # self.microenv_tab.fill_gui()

        # Do this before the celldef_tab
        # self.cell_customdata_tab.clear_gui(self.celldef_tab)
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)

        # self.celldef_tab.clear_gui()
        self.celldef_tab.clear_custom_data_params()
        self.celldef_tab.populate_tree()
        # self.celldef_tab.fill_gui(None)
        # self.celldef_tab.customize_cycle_choices() #rwh/todo: needed? 
        self.celldef_tab.fill_substrates_comboboxes()
        self.microenv_tab.celldef_tab = self.celldef_tab

        # self.cell_customdata_tab.clear_gui(self.celldef_tab)
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)

        self.user_params_tab.clear_gui()
        self.user_params_tab.fill_gui()

        self.vis_tab.init_plot_range(self.config_tab)
        self.vis_tab.reset_model()
        # self.vis_tab.setEnabled(False)
        self.enablePlotTab(False)
        self.tabWidget.setCurrentIndex(0)  # Config (default)


    def show_sample_model(self):
        print("studio.py: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~show_sample_model(): self.config_file = ", self.config_file)
        # self.config_file = "config_samples/biorobots.xml"
        self.tree = ET.parse(self.config_file)
        self.run_tab.tree = self.tree
        # self.xml_root = self.tree.getroot()
        self.reset_xml_root()
        self.setWindowTitle(self.title_prefix + self.config_file)
        # self.config_tab.fill_gui(self.xml_root)  # 
        # self.microenv_tab.fill_gui(self.xml_root)  # microenv
        # self.celldef_tab.fill_gui("foobar")  # cell defs
        # self.celldef_tab.fill_motility_substrates()

    def save_as_cb(self):
        self.config_tab.fill_xml()
        self.microenv_tab.fill_xml()
        self.celldef_tab.fill_xml()
        self.user_params_tab.fill_xml()

        save_as_file = "mymodel.xml"
        print("studio.py:  save_as_cb: writing to: ",save_as_file) # writing to:  ('/Users/heiland/git/PhysiCell-model-builder/rwh.xml', 'All Files (*)')
        self.tree.write(save_as_file)

    def view_plot_range_cb(self):
        self.vis_tab.show_hide_plot_range()

    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="",  newl="")  # newl="\n"

    def save_cb(self):
        # self.config_file = copy_file
        self.config_tab.fill_xml()
        self.microenv_tab.fill_xml()
        self.celldef_tab.fill_xml()
        self.user_params_tab.fill_xml()

        print("studio.py:  save_cb: writing to: ",self.config_file)

        # self.tree.write(self.config_file)
        # root = ET.fromstring("<fruits><fruit>banana</fruit><fruit>apple</fruit></fruits>""")
        # tree = ET.ElementTree(root)
        # ET.indent(self.tree)  # ugh, only in 3.9
        # root = ET.tostring(self.tree)
        # self.indent(self.tree)
        # self.indent(root)

        # rwh: ARGH, doesn't work
        # root = self.tree.getroot()
        # out_str = self.prettify(root)
        # print(out_str)

        # self.tree.write(outfile)
        self.tree.write(self.config_file)  # does this close the file??

        # rwh NOTE: after saving the .xml, do we need to read it back in to reflect changes.
        # self.tree = ET.parse(self.config_file)
        # self.xml_root = self.tree.getroot()
        # self.reset_xml_root()

    def load_state_cb(self):
        filePath = QFileDialog.getOpenFileName(self,'',".")
        if len(filePath[0]) > 0:
            print("\n\nload_state_cb():  filePath=",filePath)
            print("len(filePath[0])=",len(filePath[0]))
            full_path_pssm_name = filePath[0]
            pssm_tree = ET.parse(full_path_pssm_name)
            pssm_root = pssm_tree.getroot()
            exec_pgm = pssm_root.find(".//exec").text
            print("exec_pgm = ",exec_pgm)
            config_file = pssm_root.find(".//config").text
            print("config_file = ",config_file)
            self.run_tab.exec_name.setText(exec_pgm)
            self.run_tab.config_xml_name.setText(config_file)

def main():
    inputfile = ''
    # show_vis_tab = False
    show_vis_tab = True
    try:
        # opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        opts, args = getopt.getopt(sys.argv[1:],"hv:",["vis"])
    except getopt.GetoptError:
        # print 'test.py -i <inputfile> -o <outputfile>'
        print('getopt exception')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
        #  print 'test.py -i <inputfile> -o <outputfile>'
            print('bin/gui4xml.py [--vis]')
            sys.exit(1)
    #   elif opt in ("-i", "--ifile"):
        elif opt in ("--vis"):
            show_vis_tab = True
    # print 'Input file is "', inputfile
    # print("show_vis_tab = ",show_vis_tab)
    # sys.exit()

    app = QApplication(sys.argv)
    ex = PhysiCellXMLCreator(show_vis_tab)
    # ex.setGeometry(100,100, 800,600)
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()