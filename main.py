### Class Imports
from tkinter import *
from tkinter import ttk, filedialog, font
from matplotlib import cm, widgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Application():

    ### Generic 
    wavelength = None
    timepoints = None
    intensity = None
    corrIntensity = None
    
   
    ### ============================================================================================================
    ### ======================================== Main Program Specification ========================================
    ### ============================================================================================================
    def __init__(self, master):

        ### ===========================================================================================
        ### ======================================== Variables ========================================
        ### ===========================================================================================

        
        ### ==================== Monitored Variables ====================
        self.openFileLabelVariable = StringVar(value="No File Loaded") # Controls the label for file loading
        self.filenameVariable = StringVar() # Controls the Entry for the file path.
        self.wavelengthLocationVariable = StringVar()
        self.timepointsLocationVariable = StringVar()
        self.vminVariable = IntVar(value=-1)
        self.vmaxVariable = IntVar(value=1)
        self.storedClickWavelengthPositionVariable = DoubleVar(value=0.0)
        self.storedClickKineticsPositionVaribale = DoubleVar(value=0.0)
        self.wavelengthPositionVariable = IntVar(value=0)
        self.kineticsPositionVariable = IntVar(value=0)
        self.wavelengthSpecifiedVariable = StringVar(value="No Data")
        self.timpointSpecifiedLabelVariable = StringVar(value="No Data")
        self.goToTimepointVariable = DoubleVar(value=0.0)
        self.goToWavelengthVariable = DoubleVar(value=0.0)
        self.drawLinesOnHeatmapVariable = BooleanVar(value=False)
        self.fileContainsMetadataVariable = BooleanVar(value=False)
        self.metadataRowLocationVariable = StringVar()
        self.metadataRowsVariable = IntVar(value=0)


        ### ==================== Plot Options Variables ====================
        self.timeScaleVariable = StringVar(value="linear")
        self.timeUnitVariable = StringVar(value="ns")
        self.timeLowerLimitVariable = DoubleVar(value=0.0)
        self.timeUpperLimitVariable = DoubleVar(value=1000.0)
        self.energyUnitVariable = StringVar(value="nm")
        self.energyLowerLimitVariable = DoubleVar(value=0.0)
        self.energyUpperLimitVariable = DoubleVar(value=0.0)
        self.lockIntensityToHeatmapVariable = BooleanVar(value=False)


        ### ==================== Background Spectra Variables ====================
        self.spectraAverageSpinboxValueVariable = IntVar(value=0)
        self.timpointBackgroundTextVariable = StringVar(value="")
        self.overlayAverageVariable = BooleanVar(value=False)
        self.dataIsBackgroundCorrected = BooleanVar(value=False)


        ### Begins construction of program.
        self.root = master


        ### ==================== Main Window Specicification ====================
        ### Root window configuration.
        self.root.geometry("1280x720")#"1280x720+1900+200") #"640x360")
        self.root.title("TAS View")
        self.root.resizable(height=True, width=True)
        self.root.minsize(640, 360)
        self.root.maxsize(1280, 720)
        self.defaultFont = font.nametofont("TkDefaultFont")

        ### Constructs the main window which will contain all elements.
        self.mainWindow = ttk.Frame(self.root, borderwidth=5, relief="sunken")
        self.mainWindow.pack(fill=BOTH, expand=True)

        ### Configures the column and row settings so expansion can occur. 
        self.mainWindow.columnconfigure(index=0, weight=2)
        self.mainWindow.columnconfigure(index=1, weight=1)
        self.mainWindow.rowconfigure(index=0, weight=1)
        self.mainWindow.rowconfigure(index=1, weight=1)

        ### Constructs the four frames that will contain plots and information.
        self.heatmapWindow = ttk.LabelFrame(self.mainWindow, height=180, width=320, text="No File Loaded - Heatmap")
        self.kineticsWindow = ttk.LabelFrame(self.mainWindow, height=180, width=320, text="No File Loaded - Kinetics")
        self.spectrumWindow = ttk.LabelFrame(self.mainWindow, height=180, width=320, text="No File Loaded - Spectrum")
        self.miscWindow = ttk.LabelFrame(self.mainWindow, height=180, width=320, text="No File Loaded - Information")

        ### Places the frames using the grid manager.
        self.heatmapWindow.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW")
        self.kineticsWindow.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="NSEW")
        self.spectrumWindow.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="NSEW")
        self.miscWindow.grid(row=1, column=1, rowspan=1, columnspan=1, sticky="NSEW")


        ### ==================== Miscellaneous Frame Specicification ====================
        ### Collection of widgets for the information window.
        self.openFileButton = ttk.Button(self.miscWindow, text="Open File", command=self.openFile)
        self.openFileLabel = ttk.Label(self.miscWindow, textvariable=self.openFileLabelVariable, anchor="center", justify="center")
        self.fileContainsMetadataLabel = ttk.Label(self.miscWindow, text="File Contains Metadata:", width=23, anchor="e", justify="center")
        self.fileContainsMetadataCheckbox = ttk.Checkbutton(self.miscWindow, variable=self.fileContainsMetadataVariable, onvalue=True, offvalue=False)
        self.openFilePathText = Text(self.miscWindow, state="disabled", wrap="char", width=5, height=3)        
        self.fileWavelengthLabel = ttk.Label(self.miscWindow, text="Wavelengths are on:", width=19, anchor="e", justify="center")
        self.fileWavelengthCombobox = ttk.Combobox(self.miscWindow, values=["Rows", "Columns"], width=10, textvariable=self.wavelengthLocationVariable)
        self.fileTimepointsLabel = ttk.Label(self.miscWindow, text="Timepoints are on:", width=18, anchor="e", justify="center")
        self.fileTimepointsCombobox = ttk.Combobox(self.miscWindow, values=["Rows", "Columns"], width=10, textvariable=self.timepointsLocationVariable)
        self.fileMetadataLocationLabel = ttk.Label(self.miscWindow, text="Metadata is on:", width=15, anchor="e", justify="center")
        self.fileMetadataLocationCombobox = ttk.Combobox(self.miscWindow, values=["N/A", "Top", "Bottom"], width=8, textvariable=self.metadataRowLocationVariable)
        self.fileMetadataRowsLabel = ttk.Label(self.miscWindow, text="Metadata has rows:", width=18, anchor="e", justify="center")
        self.fileMetadataRowsSpinbox = ttk.Spinbox(self.miscWindow, from_=0, to=1000, textvariable=self.metadataRowsVariable, width=4)
        self.updateParametersButton = ttk.Button(self.miscWindow, text="Update Parameters", command=self.updateConfiguration)
        self.updateParamtersEntry = ttk.Entry(self.miscWindow, state="readonly")
        self.viewDataButton = ttk.Button(self.miscWindow, text="View My Data!", command=self.plotHeatmapData)
        self.plotOptionsWindowButton = ttk.Button(self.miscWindow, text="Open Plot Management Window", command=self.plottingOptionsMenu)
        self.backgroundCorrectionWindowButton = ttk.Button(self.miscWindow, text="Background Correction of Data", command=self.correctBackground)

        ### Places the widgets using the grid manager.
        self.openFileButton.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="EW", padx=(20, 5), pady=(10, 0))
        self.openFileLabel.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="EW", padx=(5, 0), pady=(10, 0))
        self.fileContainsMetadataLabel.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="EW", padx=(20, 5), pady=(10, 0))
        self.fileContainsMetadataCheckbox.grid(row=0, column=3, rowspan=1, columnspan=1, sticky="EW", padx=(5, 20), pady=(10, 0))
        self.openFilePathText.grid(row=1, column=0, rowspan=3, columnspan=4, sticky="NSEW", padx=(20, 20), pady=(10, 0))
        self.fileWavelengthLabel.grid(row=4, column=0, rowspan=1, columnspan=1, sticky="EW", padx=(20, 5), pady=(10, 0))
        self.fileWavelengthCombobox.grid(row=4, column=1, rowspan=1, columnspan=1, sticky="EW", padx=(0, 0), pady=(10, 0))
        self.fileTimepointsLabel.grid(row=4, column=2, rowspan=1, columnspan=1, sticky="EW", padx=(20, 5), pady=(10, 0))
        self.fileTimepointsCombobox.grid(row=4, column=3, rowspan=1, columnspan=1, sticky="EW", padx=(0, 20), pady=(10, 0))
        self.fileMetadataLocationLabel.grid(row=5, column=0, rowspan=1, columnspan=1, sticky="EW", padx=(20, 5), pady=(10, 0))
        self.fileMetadataLocationCombobox.grid(row=5, column=1, rowspan=1, columnspan=1, sticky="EW", padx=(0, 0), pady=(10, 0))
        self.fileMetadataRowsLabel.grid(row=5, column=2, rowspan=1, columnspan=1, sticky="EW", padx=(20, 5), pady=(10, 0))
        self.fileMetadataRowsSpinbox.grid(row=5, column=3, rowspan=1, columnspan=1, sticky="EW", padx=(0, 20), pady=(10, 0))
        self.updateParametersButton.grid(row=6, column=0, rowspan=1, columnspan=1, sticky="EW", padx=(20, 10), pady=(10, 0))
        self.updateParamtersEntry.grid(row=6, column=1, rowspan=1, columnspan=3, sticky="EW", padx=(10, 20), pady=(10, 0))
        self.viewDataButton.grid(row=7, column=0, rowspan=1, columnspan=4, sticky="NSEW", padx=(20, 20), pady=(10, 0))
        self.plotOptionsWindowButton.grid(row=8, column=0, rowspan=1, columnspan=4, sticky="NSEW", padx=(20, 20), pady=(10, 0))
        self.backgroundCorrectionWindowButton.grid(row=9, column=0, rowspan=1, columnspan=4, sticky="NSEW", padx=(20, 20), pady=(10, 10))

        ### Configures the columns in the miscellaneous frame.
        self.miscWindow.columnconfigure(index=0, weight=1)
        self.miscWindow.columnconfigure(index=1, weight=1)
        self.miscWindow.columnconfigure(index=2, weight=1)
        self.miscWindow.columnconfigure(index=3, weight=1)
        
        ### configures the rows in the miscellaneoues frame.
        self.miscWindow.rowconfigure(index=0, weight=1)
        self.miscWindow.rowconfigure(index=1, weight=1)
        self.miscWindow.rowconfigure(index=2, weight=1)
        self.miscWindow.rowconfigure(index=3, weight=1)
        self.miscWindow.rowconfigure(index=4, weight=1)
        self.miscWindow.rowconfigure(index=5, weight=1)
        self.miscWindow.rowconfigure(index=6, weight=1)
        self.miscWindow.rowconfigure(index=7, weight=1)
        self.miscWindow.rowconfigure(index=8, weight=1)
        self.miscWindow.rowconfigure(index=9, weight=1)
            
        
        ### ==================== Heatmap Frame Specicification ====================    
        self.figureHeatmap = Figure(figsize=(2.5, 1.5), dpi=100, facecolor="white")
        self.figureHeatmap.set_tight_layout(True)
        self.heatmapCanvas = FigureCanvasTkAgg(self.figureHeatmap, master=self.heatmapWindow)
        self.heatmapCanvas.get_tk_widget().place(relheight=1.0, relwidth=1.0)
        #self.heatmapCanvas.get_tk_widget().pack(fill=BOTH, expand=True)
        self.figureHeatmap.canvas.mpl_connect('button_press_event', self.plotKineticsAndSpectrumData)

        self.heatmapWindowContainerFrame = ttk.Frame(self.heatmapWindow, relief="ridge", border=2)
        self.drawLinesOnHeatmapLabel = ttk.Label(self.heatmapWindowContainerFrame, text="Draw Lines:",  background="lightgrey", foreground="black", font=(self.defaultFont, 12, "bold"), borderwidth=5, relief="ridge", anchor="se", justify="right")
        self.drawLinesOnHeatmapCheckbox = ttk.Checkbutton(self.heatmapWindowContainerFrame, variable=self.drawLinesOnHeatmapVariable, onvalue=True, offvalue=False)
        
        self.heatmapWindowContainerFrame.place(anchor="se", relx=1.0, rely=1.0)
        self.drawLinesOnHeatmapLabel.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 10), pady=(0, 0))
        self.drawLinesOnHeatmapCheckbox.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))
        

        ### ==================== Kinetics Frame Specicification ====================
        ### Figure canvas creation
        self.figureKinetics = Figure(figsize=(2.5, 1.5), dpi=100, facecolor="white")
        self.figureKinetics.set_tight_layout(True)
        self.kineticsCanvas = FigureCanvasTkAgg(self.figureKinetics, master=self.kineticsWindow)
        self.kineticsCanvas.get_tk_widget().place(relheight=1.0, relwidth=1.0)
        #self.kineticsCanvas.get_tk_widget().pack(fill=BOTH, expand=True)

        ### Other widget creation
        self.wavelengthSpecifiedLabel = ttk.Label(self.kineticsWindow,  background="lightgrey", foreground="black", font=(self.defaultFont, 12, "bold"), borderwidth=5, relief="ridge", anchor="ne", justify="right", textvariable=self.wavelengthSpecifiedVariable)
        self.kineticsWindowContainerFrame = ttk.Frame(self.kineticsWindow, relief="ridge", border=2)
        self.goToWavelengthLabel = ttk.Label(self.kineticsWindowContainerFrame, text="Go to:",  background="lightgrey", foreground="black", font=(self.defaultFont, 12, "bold"), borderwidth=5, relief="ridge", anchor="nw", justify="left")
        self.goToWavelengthEntry = ttk.Entry(self.kineticsWindowContainerFrame, width=8, textvariable=self.goToWavelengthVariable)
        self.goToWavelengthButton = ttk.Button(self.kineticsWindowContainerFrame, text="Update", command=self.goToWavelength)# command=pass)

        ### Other widget placement
        self.wavelengthSpecifiedLabel.place(anchor="ne", relx=1.0, rely=0.0)
        self.kineticsWindowContainerFrame.place(anchor="nw", relx=0.0, rely=0.0, width=200)
        self.goToWavelengthLabel.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))    #anchor="nw", relx=0.0, rely=0.0, width=200)
        self.goToWavelengthEntry.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))    #in_=self.goToWavelengthLabel, anchor="e", relx=0.58, rely=0.5)
        self.goToWavelengthButton.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))   #in_=self.goToWavelengthLabel, anchor="e", relx=1.0, rely=0.5)

        ### Configure the rows and columns
        self.kineticsWindowContainerFrame.rowconfigure(index=0, weight=1)
        self.kineticsWindowContainerFrame.columnconfigure(index=0, weight=1)
        self.kineticsWindowContainerFrame.columnconfigure(index=1, weight=1)
        self.kineticsWindowContainerFrame.columnconfigure(index=2, weight=1)


        ### ==================== Spectrum Frame Specicification ====================
        ### Figure canvas creation
        self.figureSpectrum = Figure(figsize=(2.5, 1.5), dpi=100, facecolor="white")
        self.figureSpectrum.set_tight_layout(True)
        self.spectrumCanvas = FigureCanvasTkAgg(self.figureSpectrum, master=self.spectrumWindow)
        self.spectrumCanvas.get_tk_widget().place(relheight=1.0, relwidth=1.0)
        #self.spectrumCanvas.get_tk_widget().pack(fill=BOTH, expand=True)

        ### Other widget creation
        self.timpointSpecifiedLabel = ttk.Label(self.spectrumWindow,  background="lightgrey", foreground="black", font=(self.defaultFont, 12, "bold"), borderwidth=5, relief="ridge", anchor="ne", justify="right", textvariable=self.timpointSpecifiedLabelVariable)
        self.spectrumWindowContainerFrame = ttk.Frame(self.spectrumWindow, relief="ridge", border=2)
        self.goToTimepointLabel = ttk.Label(self.spectrumWindowContainerFrame, text="Go to:",  background="lightgrey", foreground="black", font=(self.defaultFont, 12, "bold"), borderwidth=5, relief="ridge", anchor="nw", justify="left")
        self.goToTimepointEntry = ttk.Entry(self.spectrumWindowContainerFrame, width=8, textvariable=self.goToTimepointVariable) #10
        self.goToTimepointButton = ttk.Button(self.spectrumWindowContainerFrame, text="Update", command=self.goToTimepoint)

        ### Other widget placement
        self.timpointSpecifiedLabel.place(anchor="ne", relx=1.0, rely=0.0)
        self.spectrumWindowContainerFrame.place(anchor="nw", relx=0.0, rely=0.0, width=200)
        self.goToTimepointLabel.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))   # place(anchor="nw", relx=0.0, rely=0.0, width=105) #118)  
        self.goToTimepointEntry.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))   # place(in_=self.goToTimepointLabel, anchor="e", relx=1.0, rely=0.5)
        self.goToTimepointButton.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0)) 

        ### Configure the rows and columns
        self.spectrumWindowContainerFrame.rowconfigure(index=0, weight=1)
        self.spectrumWindowContainerFrame.columnconfigure(index=0, weight=1)
        self.spectrumWindowContainerFrame.columnconfigure(index=1, weight=1)
        self.spectrumWindowContainerFrame.columnconfigure(index=2, weight=1)


       ### ==================== Context Menu Specicification ====================
        self.kineticsContextMenu = Menu(self.kineticsWindow, tearoff=0)
        self.kineticsContextMenu.add_command(label="Copy Spectrum Data to Clipboard", command=lambda: self.copyDataToClipboard(self.figureSpectrum))
        self.kineticsContextMenu.add_command(label="Copy Kinetics Data to Clipboard", command=lambda: self.copyDataToClipboard(self.figureKinetics))
        self.root.bind("<Button-3>", lambda event: self.kineticsContextMenu.post(event.x_root, event.y_root))




    ### ========================================================================================================
    ### ======================================== Function Specification ========================================
    ### ========================================================================================================
    ### Allows a user to select a file to open and sets a few indicators to reflect
    ### that the file path has been successfully taken by the program.
    def openFile(self):
        
        ### Opens the TK filedialog
        self.fullFilePath = filedialog.askopenfile()

        ### Sets the internal watch variables.
        self.dataIsBackgroundCorrected.set(False); print("Background data flag unset") # resets the flag
        self.filenameVariable.set(self.fullFilePath.name)
        self.openFileLabelVariable.set("File Loaded")

        ### Updates the Entry widget with the file loaded
        self.openFilePathText.configure(state="normal")
        self.openFilePathText.delete("1.0", "end")
        self.openFilePathText.insert("1.0", str(self.fullFilePath.name))
        self.openFilePathText.configure(state="disabled")

        ### Updates LabelFrames
        self.heatmapWindow.configure(text="File Loaded - Heatmap")
        self.kineticsWindow.configure(text="File Loaded - Kinetics")
        self.spectrumWindow.configure(text="File Loaded - Spectrum")
        self.miscWindow.configure(text="File Loaded - Information")
        return 1


    ### Sets up the parameters. Extracts the wavelength, timpoint, and intensity matrices
    ### to separate variable for ease of plotting/manipulation later on.
    def updateConfiguration(self):
        if not self.dataIsBackgroundCorrected.get():
            print("Background data flag unset")
            try: # Takes the dataset chosen and extracts the desired information.
                if self.fileContainsMetadataVariable.get():
                    print(self.metadataRowLocationVariable.get())
                    if self.metadataRowLocationVariable.get() == "Top":
                        dataset = np.genfromtxt(self.filenameVariable.get(), delimiter=",", skip_header=self.metadataRowsVariable.get())
                        print(self.metadataRowsVariable.get())
                    elif self.metadataRowLocationVariable.get() == "Bottom":
                        dataset = np.genfromtxt(self.filenameVariable.get(), delimiter=",", skip_footer=self.metadataRowsVariable.get())
                else:
                    dataset = np.genfromtxt(self.filenameVariable.get(), delimiter=",")
                self.intensity = np.delete(np.delete(dataset, 0, 0), 0, 1)*1000 # Convert to mOD
            except FileNotFoundError:
                self.updateParamtersEntry.configure(state="normal")
                self.updateParamtersEntry.delete(0, "end")
                self.updateParamtersEntry.insert(0, "A file must be loaded first.")
                self.updateParamtersEntry.configure(state="readonly")
                return 0
        else:
            print("Background data flag set")

            self.intensity = self.intensity * 1000 # Convert to mOD
            return 1

        ### Separates the wavelength and timepoint matrices.
        if self.wavelengthLocationVariable.get() == "Rows" and self.timepointsLocationVariable.get() == "Columns":
            self.wavelength = dataset[1:, 0]
            self.timepoints = dataset[0, 1:]
        elif self.wavelengthLocationVariable.get() == "Columns" and self.timepointsLocationVariable.get() == "Rows":
            self.wavelength = dataset[0, 1:]
            self.timepoints = dataset[1:, 0]
        else:
            self.updateParamtersEntry.configure(state="normal")
            self.updateParamtersEntry.delete(0, "end")
            self.updateParamtersEntry.insert(0, "Wavelength or Timepoints not set.")
            self.updateParamtersEntry.configure(state="readonly")
            return 0

        ### Updates the Entry box to reflect changes.
        self.updateParamtersEntry.configure(state="normal")
        self.updateParamtersEntry.delete(0, "end")
        self.updateParamtersEntry.insert(0, "Parameters updated successfully.")
        self.updateParamtersEntry.configure(state="readonly")

        ### Updates the initial plotting variable values
        self.timeScaleVariable.set("linear")
        self.timeLowerLimitVariable.set(self.timepoints[0])
        self.timeUpperLimitVariable.set(self.timepoints[-1])
        self.energyLowerLimitVariable.set(self.wavelength[0])
        self.energyUpperLimitVariable.set(self.wavelength[-1])


    ### Plots the heatmap data. This is plotted first as the spectrum and kinetics data are
    ### then plotted in relation to a point selected by the user when they place their cursor.
    def plotHeatmapData(self):

        ### Clears the heatmap figure of data.
        self.figureHeatmap.clear()

        ### Plots the heatmpa data.
        self.axHeatmap = self.figureHeatmap.add_subplot(1, 1, 1)
        axPlotHeatmap = self.axHeatmap.pcolormesh(self.wavelength, self.timepoints, np.transpose(self.intensity), vmin=self.vminVariable.get(), vmax=self.vmaxVariable.get(), cmap=cm.jet, shading="gouraud", antialiased=True)

        ### Heatmap figure formatting
        self.axHeatmap.set_yscale(self.timeScaleVariable.get())
        self.axHeatmap.set_ylabel("Time Delay / {unit}".format(unit=self.timeUnitVariable.get()))
        self.axHeatmap.set_xlabel("Wavelength / {unit}".format(unit=self.energyUnitVariable.get()))
        self.axHeatmap.set_ylim(self.timeLowerLimitVariable.get(), self.timeUpperLimitVariable.get())
        self.axHeatmap.set_xlim(self.energyLowerLimitVariable.get(), self.energyUpperLimitVariable.get())
        self.axHeatmap.axes.xaxis.set_ticklabels([])
        self.axHeatmap.axes.yaxis.set_ticklabels([])
        self.axHeatmap.set(xlabel=None) 
        self.axHeatmap.set(ylabel=None) 

        ### Assigns the colorbar and updates the frame
        self.cbar = self.figureHeatmap.colorbar(axPlotHeatmap, ax=self.axHeatmap, label="ΔA / mOD", ticklocation="left", location="left")

        ### Constructs the cursor widget from which to retrieve values.
        self.cursor = widgets.Cursor(self.axHeatmap, useblit=True, color='black', linewidth=1)


    ### Plots the spectrum and the kinetics at the mouse click position. Using np.argmin allows
    ### for grabbing the indices for the nearest actual value to the click position.
    def plotKineticsAndSpectrumData(self, event):

        ### Sets the current x- and y-axis positions of the mouse cursor.
        self.storedClickWavelengthPositionVariable.set(event.xdata)
        self.storedClickKineticsPositionVaribale.set(event.ydata)

        ### Retrieves the indices of the nearest actual datapoint to the cursor.
        wavelengthIndex = np.argmin(np.abs(self.wavelength - self.storedClickWavelengthPositionVariable.get()))
        kineticsIndex = np.argmin(np.abs(self.timepoints - self.storedClickKineticsPositionVaribale.get()))

        ### Sets the actual wavelength and timpoints indices.
        self.wavelengthPositionVariable.set(wavelengthIndex)
        self.kineticsPositionVariable.set(kineticsIndex)  

        ### Clears the kinetics and spectrum figures of data.
        self.figureKinetics.clear()
        self.figureSpectrum.clear()

        ### Plots the kinetics and spectrum data.
        axKinetics = self.figureKinetics.add_subplot(1, 1, 1)
        axSpectrum = self.figureSpectrum.add_subplot(1, 1, 1)
        axKinetics.plot(self.timepoints, self.intensity[self.wavelengthPositionVariable.get(), :], "k-")
        axSpectrum.plot(self.wavelength, self.intensity[:, self.kineticsPositionVariable.get()], "k-")

        ### Kinetics figure formatting
        axKinetics.set_xscale(self.timeScaleVariable.get())
        axKinetics.set_ylabel("ΔA / mOD")
        axKinetics.set_xlabel("Time Delay / {unit}".format(unit=self.timeUnitVariable.get()))
        axKinetics.set_xlim(self.timeLowerLimitVariable.get(), self.timeUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axKinetics.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axKinetics.xaxis.set_visible(True)
        axKinetics.yaxis.set_visible(True)

        ### Spectrum figure formatting.
        axSpectrum.set_xlabel("Wavelength / {unit}".format(unit=self.energyUnitVariable.get()))
        axSpectrum.set_ylabel("ΔA / mOD")
        axSpectrum.set_xlim(self.energyLowerLimitVariable.get(), self.energyUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axSpectrum.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axSpectrum.xaxis.set_visible(True)
        axSpectrum.yaxis.set_visible(True)

        ### Updates the canvases
        self.kineticsCanvas.draw()
        self.spectrumCanvas.draw()

        ### Draws lines at the click position on the heatmap
        self.drawLinesOnHeatmap()

        ### Updates the corner labels
        self.wavelengthSpecifiedVariable.set(str(self.wavelength[self.wavelengthPositionVariable.get()]) + " nm")
        self.timpointSpecifiedLabelVariable.set(str(self.timepoints[self.kineticsPositionVariable.get()]) + " " + str(self.timeUnitVariable.get()))


    ### Retrieves the user input into the Entry widget, finds the nearest timepoint, and updates
    ### the spectrum figure to display the spectrum at the chosen timepoint. 
    def goToTimepoint(self):
        ### Retrieves the index of the nearest actual datapoint.
        kineticsIndex = np.argmin(np.abs(self.timepoints - self.goToTimepointVariable.get()))

        ### Sets the actual timepoint index.
        self.kineticsPositionVariable.set(kineticsIndex)  

        ### Clears the spectrum figure of data.
        self.figureSpectrum.clear()

        ### Plots the spectrum data.
        axSpectrum = self.figureSpectrum.add_subplot(1, 1, 1)
        axSpectrum.plot(self.wavelength, self.intensity[:, self.kineticsPositionVariable.get()], "k-")

        ### Spectrum figure formatting.
        axSpectrum.set_xlabel("Wavelength / {unit}".format(unit=self.energyUnitVariable.get()))
        axSpectrum.set_ylabel("ΔA / mOD")
        axSpectrum.set_xlim(self.energyLowerLimitVariable.get(), self.energyUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axSpectrum.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axSpectrum.xaxis.set_visible(True)
        axSpectrum.yaxis.set_visible(True)

        ### Updates the canvas
        self.spectrumCanvas.draw()

        ### Draws lines at the click position on the heatmap
        self.drawLinesOnHeatmap()

        ### Updates the corner labels
        self.timpointSpecifiedLabelVariable.set(str(self.timepoints[self.kineticsPositionVariable.get()]) + " " + str(self.timeUnitVariable.get()))


    ### Retrieves the user input into the Entry widget, finds the nearest wavelength, and updates
    ### the kinetics figure to display the kinetics trace at the chosen wavelength. 
    def goToWavelength(self):
        ### Retrieves the index of the nearest actual datapoint.
        wavelengthIndex = np.argmin(np.abs(self.wavelength - self.goToWavelengthVariable.get()))

        ### Sets the actual wavelength.
        self.wavelengthPositionVariable.set(wavelengthIndex)

        ### Clears the kinetics figure of data.
        self.figureKinetics.clear()

        ### Plots the kinetics data.
        axKinetics = self.figureKinetics.add_subplot(1, 1, 1)
        axKinetics.plot(self.timepoints, self.intensity[self.wavelengthPositionVariable.get(), :], "k-")

        ### Kinetics figure formatting
        axKinetics.set_xscale(self.timeScaleVariable.get())
        axKinetics.set_ylabel("ΔA / mOD")
        axKinetics.set_xlabel("Time Delay / {unit}".format(unit=self.timeUnitVariable.get()))
        axKinetics.set_xlim(self.timeLowerLimitVariable.get(), self.timeUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axKinetics.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axKinetics.xaxis.set_visible(True)
        axKinetics.yaxis.set_visible(True)

        ### Updates the canvas
        self.kineticsCanvas.draw()

        ### Draws lines at the click position on the heatmap
        self.drawLinesOnHeatmap()

        ### Updates the corner label
        self.wavelengthSpecifiedVariable.set(str(self.wavelength[self.wavelengthPositionVariable.get()]) + " nm")
    

    ### Draws lines on the heatmap canvas
    def drawLinesOnHeatmap(self):
        ### Removes any existing lines except for the cursor lines. If redrawing the lines then this path is followed.
        if len(self.axHeatmap.get_lines()) > 2 and self.drawLinesOnHeatmapVariable.get():
            for i in range(len(self.axHeatmap.get_lines())-1, 1, -1):
                self.axHeatmap.lines.remove(self.axHeatmap.get_lines()[i])
        
        ### Does the same as above, but for when new lines are not being drawn (only re-draws the canvas once).
        elif len(self.axHeatmap.get_lines()) > 2 and not self.drawLinesOnHeatmapVariable.get():
            for i in range(len(self.axHeatmap.get_lines())-1, 1, -1):
                self.axHeatmap.lines.remove(self.axHeatmap.get_lines()[i])
            self.heatmapCanvas.draw()
        
        ### Only draws the lines if the checkbox is checked
        if self.drawLinesOnHeatmapVariable.get():
            self.axHeatmap.axvline(self.wavelength[self.wavelengthPositionVariable.get()], 0, 1, color="black", linewidth=2)
            self.axHeatmap.axhline(self.timepoints[self.kineticsPositionVariable.get()], 0, 1, color="black", linewidth=2)
            self.heatmapCanvas.draw()
        

    ### Closes the a window properly.
    def closeWindow(self, window):
        window.destroy()


    ### Updates the heatmap (and subsequent plots on click) by pushing the view data button.
    def updatePlots(self):
        self.viewDataButton.invoke()


    ### Gets the current x- and y-data from the selected figure and appends this to the clipboard for plotting externally.
    def copyDataToClipboard(self, figureObject):
        ### Retireve the x- and y-data of the selected figure
        figureData = figureObject.gca().get_lines()[0].get_xydata()
        print(figureData, np.shape(figureData))

        ### Clears the clipboard
        self.root.clipboard_clear()

        ### Appends the data to the clipboard
        for i in range(len(figureData)):
            self.root.clipboard_append(str(str(figureData[i][0]) + "\t" + str(figureData[i][1]) + "\n"))




    ### ===========================================================================================================================
    ### =========================================== Plotting Options Menu Specification ===========================================
    ### ===========================================================================================================================
    ### Creates the plotting options window which allows the user to set paramters for all of
    ### the plots. This includes energy range and time range, as well as displaying the time on
    ### a logarithmic scale.
    def plottingOptionsMenu(self):
        self.plotManagementWindow = Toplevel(self.root)
        self.plotManagementWindow.title("Plot Management Options")
        self.plotManagementWindow.geometry("520x450")# ("510x405") #("510x335") #+3200+200")
        self.plotManagementWindow.resizable(height=False, width=False)
        
        ### Creates the two panes to simulate a paned window inside a top-level.    
        self.plotSpecifierPane = ttk.Frame(self.plotManagementWindow)
        self.plotOptionsPane = ttk.Frame(self.plotManagementWindow)

        ### Places the pseudo-PanedWindow frames.
        self.plotSpecifierPane.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))
        self.plotOptionsPane.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))

        ### Configures the rows and columns in the plotManagementWindow frame.
        self.plotManagementWindow.columnconfigure(index=0, weight=1)
        self.plotManagementWindow.columnconfigure(index=1, weight=1)
        self.plotManagementWindow.rowconfigure(index=0, weight=1)

        ### For the three plots, use separate frames to hold the options - The frames can be raised and lowered.
        self.globalOptions = ttk.Frame(self.plotOptionsPane, width=400, height=400, relief="sunken", borderwidth=5)
        self.heatmapOptions = ttk.Frame(self.plotOptionsPane, width=400, height=400)
        self.spectrumOptions = ttk.Frame(self.plotOptionsPane, width=400, height=400)
        self.kineticsOptions = ttk.Frame(self.plotOptionsPane, width=400, height=400)
        self.globalOptions.grid(row=0, column=0, sticky="NSEW")

        ### Configures the grid.
        self.plotSpecifierPane.columnconfigure(index=0, weight=1)
        self.plotSpecifierPane.rowconfigure(index=0, weight=1)
        self.plotOptionsPane.columnconfigure(index=0, weight=1)
        self.plotOptionsPane.rowconfigure(index=0, weight=1)


        ### ==================== Plot Specifier Treeview Specicification ====================
        ### Generates the treeview for the plot options handling.
        self.plotSpecifierTreeview = ttk.Treeview(self.plotSpecifierPane, columns=["availPlots"], show="headings", height=4)
        self.plotSpecifierTreeview.heading("availPlots", text="Plots")
        self.plotSpecifierTreeview.insert("", "end", iid="global", values="Global")
        #self.plotSpecifierTreeview.insert("", "end", iid="heatmap", values="Heatmap")      # Add in later revision?
        #self.plotSpecifierTreeview.insert("", "end", iid="spectrum", values="Spectrum")    # Add in later revision?
        #self.plotSpecifierTreeview.insert("", "end", iid="kinetics", values="Kinetics")    # Add in later revision?
        self.plotSpecifierTreeview.pack(fill=BOTH, expand=True)

        ### Allows for user interaction
        self.plotSpecifierTreeview.bind("<<TreeviewSelect>>", self.selectPlotOptions)


        ### ==================== Plot Options - Global - Specification ====================
        ### Title
        titleLabel = ttk.Label(self.globalOptions, text="Options for All Plots", font=(self.defaultFont, 16, "underline", "bold"))
        titleLabel.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="NSEW", padx=(20,20), pady=(10,10))

        ### Time axis options
        self.timeScaleVariableLabel = ttk.Label(self.globalOptions, text="Time Axis Scaling")
        self.timeScaleVariableCombobox = ttk.Combobox(self.globalOptions, values=["linear", "log", "symlog"], width=20, textvariable=self.timeScaleVariable)
        self.timeUnitVariableLabel = ttk.Label(self.globalOptions, text="Time Axis Unit:")
        self.timeUnitVariableCombobox = ttk.Combobox(self.globalOptions, values=["fs", "ps", "ns"], width=20, textvariable=self.timeUnitVariable)
        self.timeLowerLimitVariableLabel = ttk.Label(self.globalOptions, text="Lower Time Value:")
        self.timeLowerLimitVariableEntry = ttk.Entry(self.globalOptions, state="normal", textvariable=self.timeLowerLimitVariable)
        self.timeUpperLimitVariableLabel = ttk.Label(self.globalOptions, text="Upper Time Value:")
        self.timeUpperLimitVariableEntry = ttk.Entry(self.globalOptions, state="normal", textvariable=self.timeUpperLimitVariable)

        ### Separator for cleaner GUI
        self.separator1 = ttk.Separator(self.globalOptions, orient='horizontal')

        ### Energy axis options
        self.energyUnitsVariableLabel = ttk.Label(self.globalOptions, text="Energy Axis Unit:")
        self.energyUnitsVariableCombobox = ttk.Combobox(self.globalOptions, values=["nm", "eV", "$cm^{-1}$"], width=20, textvariable=self.energyUnitVariable, state="disabled")
        self.energyLowerLimitVariableLabel = ttk.Label(self.globalOptions, text="Lower Energy Value:")
        self.energyLowerLimitVariableEntry = ttk.Entry(self.globalOptions, state="normal", textvariable=self.energyLowerLimitVariable)#, validate="key", validatecommand=vcmd)
        self.energyUpperLimitVariableLabel = ttk.Label(self.globalOptions, text="Upper Energy Value:")
        self.energyUpperLimitVariableEntry = ttk.Entry(self.globalOptions, state="normal", textvariable=self.energyUpperLimitVariable)#, validate="key", validatecommand=vcmd)

        ### Separator for cleaner GUI
        self.separator2 = ttk.Separator(self.globalOptions, orient='horizontal')

        ### Intensity axis options
        self.heatmapVminLabel = ttk.Label(self.globalOptions, text="Low ΔA Value (mOD):")
        self.heatmapVminSpinbox = ttk.Spinbox(self.globalOptions, from_=-15, to=15, textvariable=self.vminVariable, width=4)
        self.heatmapVmaxLabel = ttk.Label(self.globalOptions, text="High ΔA Value (mOD):")
        self.heatmapVmaxSpinbox = ttk.Spinbox(self.globalOptions, from_=-15, to=15, textvariable=self.vmaxVariable, width=4)
        self.lockIntensityToHeatmapLabel = ttk.Label(self.globalOptions, text="Lock Kinetics and\nSpectrum Intensity:")
        self.lockIntensityToHeatmapCheckButton = ttk.Checkbutton(self.globalOptions, variable=self.lockIntensityToHeatmapVariable, onvalue=True, offvalue=False)

        ### Placement of all widgets
        self.timeScaleVariableLabel.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 10), pady=(10, 0))
        self.timeScaleVariableCombobox.grid(row=1, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.timeUnitVariableLabel.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 10), pady=(10, 0))
        self.timeUnitVariableCombobox.grid(row=2, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.timeLowerLimitVariableLabel.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.timeLowerLimitVariableEntry.grid(row=3, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.timeUpperLimitVariableLabel.grid(row=4, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.timeUpperLimitVariableEntry.grid(row=4, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.separator1.grid(row=5, column=0, rowspan=1, columnspan=2, sticky="NSEW", padx=(20, 20), pady=(10, 0))
        self.energyUnitsVariableLabel.grid(row=6, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 10), pady=(10, 0))
        self.energyUnitsVariableCombobox.grid(row=6, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.energyLowerLimitVariableLabel.grid(row=7, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.energyLowerLimitVariableEntry.grid(row=7, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.energyUpperLimitVariableLabel.grid(row=8, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.energyUpperLimitVariableEntry.grid(row=8, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.separator2.grid(row=9, column=0, rowspan=1, columnspan=2, sticky="NSEW", padx=(20, 20), pady=(10, 0))
        self.heatmapVminLabel.grid(row=10, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.heatmapVminSpinbox.grid(row=10, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.heatmapVmaxLabel.grid(row=11, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.heatmapVmaxSpinbox.grid(row=11, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 20), pady=(10, 0))
        self.lockIntensityToHeatmapLabel.grid(row=12, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 0))
        self.lockIntensityToHeatmapCheckButton.grid(row=12, column=1, rowspan=1, columnspan=1, stick="NSEW", padx=(0, 20), pady=(10, 0))

        ### Updates the plots
        self.updatePlotsButton = ttk.Button(self.globalOptions, text="Update Plots", command=self.updatePlots)
        self.updatePlotsButton.grid(row=13, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 10))

        ### Close window
        self.closeWindowButton = ttk.Button(self.globalOptions, text="Close Window", command=lambda: self.closeWindow(self.plotManagementWindow))
        self.closeWindowButton.grid(row=13, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(5, 20), pady=(10, 10))


    ### Allows for frames of the options to be hidden and shown selection in the treeview. This
    ### Currently serves no purpose as there are no options to control for the individual plots
    ### just yet. This will be of convenience in later iteractions.
    def selectPlotOptions(self, event):
        if self.plotSpecifierTreeview.selection()[0] == "global":
            self.heatmapOptions.grid_forget()
            self.spectrumOptions.grid_forget()
            self.kineticsOptions.grid_forget()
            self.globalOptions.grid(row=0, column=0, sticky="NSEW")   
        elif self.plotSpecifierTreeview.selection()[0] == "heatmap":
            self.globalOptions.grid_forget()
            self.spectrumOptions.grid_forget()
            self.kineticsOptions.grid_forget()
            self.heatmapOptions.grid(row=0, column=0, sticky="NSEW")
        elif self.plotSpecifierTreeview.selection()[0] == "spectrum":
            self.globalOptions.grid_forget()
            self.heatmapOptions.grid_forget()
            self.kineticsOptions.grid_forget()
            self.spectrumOptions.grid(row=0, column=0, sticky="NSEW")
        elif self.plotSpecifierTreeview.selection()[0] == "kinetics":
            self.globalOptions.grid_forget()
            self.heatmapOptions.grid_forget()
            self.spectrumOptions.grid_forget()
            self.kineticsOptions.grid(row=0, column=0, sticky="NSEW")




    ### ==========================================================================================================================
    ### ======================================= Background Correction Window Specification =======================================
    ### ==========================================================================================================================
    ### Performs the background correction on the intensity matrix by averaging negative time delays and subtracting
    ### from the whole matrix - Since negative times aren't usually plotted, we can subtract from the whole matrix
    ### without issue. If negative times are desired then this function can be altered to only do positive time subtraction.
    def correctBackground(self):
        ### ==================== Background Correction Specicification ====================
        ### Creates a new top-level window for bakcground correction.
        self.backgroundCorrectionWindow = Toplevel(self.root)
        self.backgroundCorrectionWindow.title("Background Correction")
        self.backgroundCorrectionWindow.geometry("1200x400")
        self.backgroundCorrectionWindow.resizable(height=False, width=False)
        
        ### Creates the three frames.    
        self.plottingFrame = ttk.Frame(self.backgroundCorrectionWindow, relief="sunken", border=2)
        self.optionsFrame = ttk.Frame(self.backgroundCorrectionWindow, relief="sunken", border=2)
        self.correctedFrame = ttk.Frame(self.backgroundCorrectionWindow, relief="sunken", border=2)

        ### Places the frames.
        self.plottingFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))
        self.optionsFrame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))
        self.correctedFrame.grid(row=0, column=1, rowspan=2, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))

        ### Configures the rows and columns in the top-level window.
        self.backgroundCorrectionWindow.columnconfigure(index=0, weight=0)
        self.backgroundCorrectionWindow.columnconfigure(index=1, weight=1)
        self.backgroundCorrectionWindow.rowconfigure(index=0, weight=1)
        self.backgroundCorrectionWindow.rowconfigure(index=1, weight=0)


        ### ==================== Plotting Frame Specicification ====================
        ### Splits the plottingFrame into two more frames containing timepoint info and the plot.
        self.timepointsDisplayFrame= ttk.Frame(self.plottingFrame, relief="sunken", border=2)
        self.timepointsSelectedFrame= ttk.Frame(self.plottingFrame, relief="sunken", border=2)

        ### Places the frames.
        self.timepointsDisplayFrame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))
        self.timepointsSelectedFrame.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="NSEW", padx=(0, 0), pady=(0, 0))
        
        ### Configures the rows and columns.
        self.plottingFrame.columnconfigure(index=0, weight=0)
        self.plottingFrame.columnconfigure(index=1, weight=0)
        self.plottingFrame.rowconfigure(index=0, weight=1)


        ### ==================== Corrected Plot Frame Specicification ====================
        ### Adds the figure canvas to the plot display frame
        self.figureCorrectedSample = Figure(figsize=(1, 1), dpi=100, facecolor="white")
        self.figureCorrectedSample.set_tight_layout(True)
        self.correctedSampleCanvas = FigureCanvasTkAgg(self.figureCorrectedSample, master=self.correctedFrame)
        self.correctedSampleCanvas.get_tk_widget().pack(fill=BOTH, expand=True)


        ### ==================== Timepoint Display Frame Specicification ====================
        ### Adds the figure canvas to the plot display frame
        self.figureBackground = Figure(figsize=(4.5, 2), dpi=100, facecolor="white")
        self.figureBackground.set_tight_layout(True)
        self.backgroundCanvas = FigureCanvasTkAgg(self.figureBackground, master=self.timepointsDisplayFrame)
        self.backgroundCanvas.get_tk_widget().pack(fill=BOTH, expand=True)


        ### ==================== Timepoint Selected Frame Specicification ====================
        ### Adds the timepoint selectionwidgets
        self.timepointSelectedHeaingLabel = ttk.Label(self.timepointsSelectedFrame, text="Timepoints:", font=(self.defaultFont, 16, "underline", "bold"), width=11, anchor="center", justify="center")
        self.timepointSelectedValuesContainerFrame = ttk.Frame(self.timepointsSelectedFrame, relief="solid", borderwidth=3)
        self.timepointSelectedValuesText= Text(self.timepointSelectedValuesContainerFrame, width=18, height=4, wrap=None, bg="white", state="disabled")
        self.timepointSelectedValuesScrollbar = ttk.Scrollbar(self.timepointSelectedValuesContainerFrame, orient=VERTICAL, command=self.timepointSelectedValuesText.yview)
        self.timepointSelectedValuesText.configure(yscrollcommand=self.timepointSelectedValuesScrollbar.set)
        self.timepointSelectedValuesText.config(state="disabled")
        #self.timepointSelectedValuesLabel = ttk.Label(self.timepointSelectedValuesContainerFrame, textvariable=self.timpointBackgroundTextVariable, background="white")

        ### Places the widgets
        self.timepointSelectedHeaingLabel.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20,20), pady=(20,10))
        self.timepointSelectedValuesContainerFrame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20,20), pady=(10,20))
        self.timepointSelectedValuesScrollbar.pack(side="right", fill="y", expand=True)        
        self.timepointSelectedValuesText.pack(fill=BOTH, expand=True)
        #self.timepointSelectedValuesLabel.pack(fill=BOTH, expand=True)

        ### Configures the columns and rows
        self.timepointsSelectedFrame.columnconfigure(index=0, weight=1)
        self.timepointsSelectedFrame.rowconfigure(index=0, weight=0)
        self.timepointsSelectedFrame.rowconfigure(index=1, weight=1)


        ### ==================== Options Frame Specicification ====================
        ### Creates style to center text in a single button
        styleButtonCenter = ttk.Style()
        styleButtonCenter.configure("W.TButton", anchor="center", justify="center")

        ### Adds the options widgets
        self.spectrumSelectionLabel = ttk.Label(self.optionsFrame, text="Spectra to Average:", width=20, anchor="e", justify="right")
        self.spectrumSelectionSpinbox = ttk.Spinbox(self.optionsFrame, from_=0, to=len(self.timepoints), textvariable=self.spectraAverageSpinboxValueVariable, width=5, command=lambda: self.plotBackgroundSpectra(self.spectraAverageSpinboxValueVariable.get()))
        self.overlayAverageLabel = ttk.Label(self.optionsFrame, text="Overlay the Average\nBackground:", anchor="e", justify="right")
        self.overlayAverageCheckbox = ttk.Checkbutton(self.optionsFrame, variable=self.overlayAverageVariable, onvalue=True, offvalue=False)
        self.saveCorrectedTA = ttk.Button(self.optionsFrame, text="Apply Correction and\nSave New File", style="W.TButton", command=lambda: self.saveCorrectedSpectra(self.spectraAverageSpinboxValueVariable.get()))

        ### Places the options widgets
        self.spectrumSelectionLabel.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 10))
        self.spectrumSelectionSpinbox.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="EW", padx=(5, 0), pady=(10, 10))
        self.overlayAverageLabel.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 5), pady=(10, 10))
        self.overlayAverageCheckbox.grid(row=0, column=3, rowspan=1, columnspan=1, sticky="NSEW", padx=(5, 0), pady=(10, 10))    
        self.saveCorrectedTA.grid(row=0, column=4, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 0), pady=(10, 10))  
        
        ### Configures the rows and columns
        self.optionsFrame.rowconfigure(index=0, weight=1)
        self.optionsFrame.columnconfigure(index=0, weight=1)
        self.optionsFrame.columnconfigure(index=1, weight=1)
        self.optionsFrame.columnconfigure(index=2, weight=1)
        self.optionsFrame.columnconfigure(index=3, weight=1)
        self.optionsFrame.columnconfigure(index=4, weight=1)
        self.optionsFrame.columnconfigure(index=5, weight=1)

        ### Close window
        self.closeWindowButton = ttk.Button(self.optionsFrame, text="Close Window", command=lambda: self.closeWindow(self.backgroundCorrectionWindow))
        self.closeWindowButton.grid(row=0, column=5, rowspan=1, columnspan=1, sticky="NSEW", padx=(20, 20), pady=(10, 10))


    ### Plots spectra at each timepoint. The spectrum are plotted to a value which is takne from
    ### The spinbox. This just updates the plots
    def plotBackgroundSpectra(self, bkgSpcVal):

        ### Clears the figures of data.
        self.figureBackground.clear()
        self.figureCorrectedSample.clear()

        ### Plots the selected subtraction spectra.
        axBackgroundSpectra = self.figureBackground.add_subplot(1, 1, 1)
        if bkgSpcVal == 0: return 1 # Don't plot if no spectra are selected
        for i in range(bkgSpcVal):
            axBackgroundSpectra.plot(self.wavelength, self.intensity[:, i], label=None)

        ### Computes the mean average intensity of selected spectra
        zeroNanIntensity = np.nan_to_num(self.intensity)
        summedIntensity = 0
        backgroundAverage = None
        for i in range(bkgSpcVal):
            summedIntensity = summedIntensity + zeroNanIntensity[:, i]
            backgroundAverage = summedIntensity / bkgSpcVal 

        ### If desired, the average can be plotted
        if self.overlayAverageVariable.get():     
            axBackgroundSpectra.plot(self.wavelength, backgroundAverage, "k-", linewidth=2, label="Average Spectrum")
            axBackgroundSpectra.legend(loc="upper right")
        
        ### Applies the background correction, converts the result to a numpy array
        corrIntens = []
        for i in range(len(self.timepoints)):
            timepointIntensityCorrect = self.intensity[:, i] - backgroundAverage # Pick each column, do subtraction
            corrIntens.append(np.asarray(timepointIntensityCorrect)) # append as row
        corrIntens = np.transpose(np.asarray(corrIntens)) # transpose back to usual format
        
        ### Plots a sample of normal and spectra with subtracted background
        axCorrectedSample = self.figureCorrectedSample.add_subplot(2,1,1)
        axNormalSample = self.figureCorrectedSample.add_subplot(2,1,2)
        timepointIdx = np.linspace(20, len(self.timepoints), 6, endpoint=False)
        for i in timepointIdx:
            i = int(round(i))
            axCorrectedSample.plot(self.wavelength, corrIntens[:, i])
            axNormalSample.plot(self.wavelength, self.intensity[:, i])

        ### Corrected data figure formatting.
        axCorrectedSample.set_title("Sample Spectrum: Applied Background Correction")
        axCorrectedSample.set_xlabel("Wavelength / {unit}".format(unit=self.energyUnitVariable.get()))
        axCorrectedSample.set_ylabel("ΔA / mOD")
        axCorrectedSample.set_xlim(self.energyLowerLimitVariable.get(), self.energyUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axCorrectedSample.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axCorrectedSample.axes.xaxis.set_ticklabels([])
        axCorrectedSample.set(xlabel=None) 
        axCorrectedSample.yaxis.set_visible(True)

        ### Normal data figure formatting.
        axNormalSample.set_title("Sample Spectrum: No Background Correction")
        axNormalSample.set_xlabel("Wavelength / {unit}".format(unit=self.energyUnitVariable.get()))
        axNormalSample.set_ylabel("ΔA / mOD")
        axNormalSample.set_xlim(self.energyLowerLimitVariable.get(), self.energyUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axNormalSample.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axNormalSample.xaxis.set_visible(True)
        axNormalSample.yaxis.set_visible(True)

        ### Background figure formatting.
        axBackgroundSpectra.set_title("Averaged Background Spectra")
        axBackgroundSpectra.set_xlabel("Wavelength / {unit}".format(unit=self.energyUnitVariable.get()))
        axBackgroundSpectra.set_ylabel("ΔA / mOD")
        axBackgroundSpectra.set_xlim(self.energyLowerLimitVariable.get(), self.energyUpperLimitVariable.get())
        if self.lockIntensityToHeatmapVariable.get():
            axBackgroundSpectra.set_ylim(self.vminVariable.get(), self.vmaxVariable.get())
        axBackgroundSpectra.xaxis.set_visible(True)
        axBackgroundSpectra.yaxis.set_visible(True)

        ### Updates the canvases
        self.backgroundCanvas.draw()
        self.correctedSampleCanvas.draw()  

        ### Creates the text used to update the text widget
        genString = ""
        for i in range(bkgSpcVal):
            genString = genString + str(self.timepoints[i]) + " " + str(self.timeUnitVariable.get()) + "\n"
        self.timpointBackgroundTextVariable.set(genString)

        ### Updates the Text widget
        self.timepointSelectedValuesText.config(state="normal")
        self.timepointSelectedValuesText.delete("1.0", END)
        self.timepointSelectedValuesText.insert("1.0", self.timpointBackgroundTextVariable.get()) 
        self.timepointSelectedValuesText.config(state="disabled")


    ### Saves the background-corrected TA spectrum. The corrected file is output as a csv which has been reconstructed
    ### to the default input of wavelengths on the columns and timepoints on the rows.
    def saveCorrectedSpectra(self, bkgSpcVal):
        ### Toggles the internal flag to trigger intensity loading internally by the update method.
        self.dataIsBackgroundCorrected.set(True)

        ### Computes the mean average intensity of selected spectra
        summedIntensity = 0
        backgroundAverage = None
        for i in range(bkgSpcVal):
            summedIntensity = summedIntensity + self.intensity[:, i]
            backgroundAverage = summedIntensity / bkgSpcVal 
        
        ### Applies the background correction, converts the result to a numpy array
        corrIntens = []
        for i in range(len(self.timepoints)):
            timepointIntensityCorrect = self.intensity[:, i] - backgroundAverage # Pick each column, do subtraction
            corrIntens.append(np.asarray(timepointIntensityCorrect)) # append as row
        corrIntens = np.transpose(np.asarray(corrIntens)) # transpose back to usual format

        ### Internally sets the intensity variable to the corrected matrix
        self.intensity = corrIntens / 1000 # Return to OD unit

        ### Reconstructs the original TA matrix
        fullArray = self.timepoints # 1D timepoints
        fullArray = np.insert(fullArray, 0, 0.0, axis=0) # insert the buffer character
        tempArray = np.insert(self.intensity, 0, self.wavelength, axis=1) # insert wavelength into the intensity matrix as first column
        fullArray = np.insert(tempArray, 0, fullArray, axis=0) # insert the timepoints into the intensity matrix as the first row
        print(fullArray)

        ### Promps user to save the new corrected matrix to a new file so they don't have to do this repeatedly
        filePath = filedialog.asksaveasfilename(filetypes=[("Comma-Separated Values", "*.csv"), ("Text File", "*.txt"), ("All files", "*.*")], defaultextension=".csv")
        np.savetxt(filePath, fullArray, delimiter=",")




def main():
    root = Tk()
    app = Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()