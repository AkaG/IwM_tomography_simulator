import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from ct import *

LARGE_FONT = ("Verdana", 12)


class TomographGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Tomograph")

        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for F in (StartPage,):
            page = F(frame, self)

            self.pages[F] = page

            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.pages[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.ct = ct()

        self._algorithminfo(0, 0)
        self._pinfo(0, 6)
        self._buttons(4, 0)
        self.doAnimation = tk.BooleanVar()
        c = tk.Checkbutton(master=self, text="Animation", variable=self.doAnimation)
        c.grid(row=2, column=2)

        self.fig = Figure(figsize=(15, 5), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()

        toolbar_frame = tk.Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()

        self.canvas.get_tk_widget().grid(row=10, column=0, columnspan=8)
        toolbar_frame.grid(row=11, column=0, columnspan=7)

    def loadImage(self):
        self.ct.loadImage(self._get_read_file_name())
        ax = self.fig.add_subplot(231)
        ax.clear()
        ax.imshow(self.ct.image, cmap=cm.Greys_r, vmin=0, vmax=1)
        self.canvas.draw()

    def saveImage(self):
        self.ct.pname = self.pname.get()
        self.ct.plastname = self.plastname.get()
        self.ct.page = self.pAge.get()
        self.ct.pcomment = self.pcomment.get()

        self.ct.saveAsDICOM(self._get_save_file_name())

    def generateButtonFunc(self):
        self.ct.step = float(self.step.get())
        self.ct.n = int(self.emittercount.get())
        self.ct.phi = int(self.spread.get())

        ax = self.fig.add_subplot(232)
        ax2 = self.fig.add_subplot(233)

        if self.doAnimation.get():
            self.ct.generateSinogram(animate=lambda x,y : self.animate(x, y, [ax, ax2]))
        else:
            self.ct.generateSinogram()

        ax.clear()
        ax.imshow(array(self.ct.sinogram).transpose(), cmap=cm.Greys_r, vmin=amin(self.ct.sinogram), vmax=amax(self.ct.sinogram))
        self.canvas.draw()

        ax2.clear()
        ax2.imshow(self.ct.lines, cmap=cm.Greys_r, vmin=amin(self.ct.lines), vmax=amax(self.ct.lines))
        self.canvas.draw()

    def reconstructButtonFunc(self):
        self.ct.filterSinogram(int(self.mask.get()))

        ax = self.fig.add_subplot(235)
        ax.clear()
        ax.imshow(array(self.ct.filteredsinogram).transpose(), cmap=cm.Greys_r, vmin=amin(self.ct.filteredsinogram), vmax=amax(self.ct.filteredsinogram))
        self.canvas.draw()

        self.ct.reconstruct()

        ax = self.fig.add_subplot(234)
        ax.clear()
        ax.imshow(self.ct.reconstruction, cmap=cm.Greys_r, vmin=amin(self.ct.reconstruction), vmax=amax(self.ct.reconstruction))
        self.canvas.draw()

        self.ct.generateDiff()
        ax = self.fig.add_subplot(236)
        ax.clear()
        ax.imshow(self.ct.reconstructionDiff, cmap=cm.Greys_r, vmin=amin(self.ct.reconstructionDiff), vmax=amax(self.ct.reconstruction))
        self.canvas.draw()

    def animate(self, res, cpy, axis):
        axis[0].clear()
        axis[1].clear()
        axis[0].imshow(array(res).transpose(), cmap=cm.Greys_r, vmin=0, vmax=amax(res))
        axis[1].imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
        self.canvas.draw()

    def _get_read_file_name(self):
        return askopenfilename(filetypes=(("All files", "*.*"),
                                          ("PNG", "*.png"),
                                          ("JPG", "*.jpg"),
                                          ("DICOM", "*.dcm")))

    def _get_save_file_name(self):
        return asksaveasfilename(filetypes=(("DICOM", "*.dcm"),
                                            ("All files", "*.*")
                                            ))

    def _buttons(self, row, col):
        self.readbutton = tk.Button(self, text="Load file", command=lambda: self.loadImage(), width=10)
        self.readbutton.grid(row=row, column=col)

        self.savebutton = tk.Button(self, text="Save file", command=lambda: self.saveImage(), width=10)
        self.savebutton.grid(row=row, column=col+1)

        self.generatebutton = tk.Button(self, text="Sinogram", command=lambda: self.generateButtonFunc(), width=10)
        self.generatebutton.grid(row=row, column=col+2)

        self.reconstructbutton = tk.Button(self, text="Reconstruct", command=lambda: self.reconstructButtonFunc(), width=10)
        self.reconstructbutton.grid(row=row, column=col + 3)

    def _algorithminfo(self, row, col):
        self.steplabel = tk.Label(self, text="Step")
        self.steplabel.grid(row=row, column=col)
        self.step = tk.Entry(self)
        self.step.insert(0, 1)
        self.step.grid(row=row, column=col + 1)

        self.emittercountlabel = tk.Label(self, text="Emitter count")
        self.emittercountlabel.grid(row=row + 1, column=col)
        self.emittercount = tk.Entry(self)
        self.emittercount.insert(0, 200)
        self.emittercount.grid(row=row + 1, column=col + 1)

        self.spreadlabel = tk.Label(self, text="Spread")
        self.spreadlabel.grid(row=row + 2, column=col)
        self.spread = tk.Entry(self)
        self.spread.insert(0, 150)
        self.spread.grid(row=row + 2, column=col + 1)

        self.masklabel = tk.Label(self, text="Mask")
        self.masklabel.grid(row=row + 3, column=col)
        self.mask = tk.Entry(self)
        self.mask.insert(0, 40)
        self.mask.grid(row=row + 3, column=col + 1)

    def _pinfo(self, row, col):
        self.pnamelabel = tk.Label(self, text="Name")
        self.pnamelabel.grid(row=row, column=col)
        self.pname = tk.Entry(self)
        self.pname.grid(row=row, column=col + 1)

        self.plastnamelabel = tk.Label(self, text="Last Name")
        self.plastnamelabel.grid(row=row + 1, column=col)
        self.plastname = tk.Entry(self)
        self.plastname.grid(row=row + 1, column=col + 1)

        self.pAgelabel = tk.Label(self, text="Age")
        self.pAgelabel.grid(row=row + 2, column=col)
        self.pAge = tk.Entry(self)
        self.pAge.grid(row=row + 2, column=col + 1)

        self.pcommentlabel = tk.Label(self, text="Comment")
        self.pcommentlabel.grid(row=row + 3, column=col, rowspan=2)
        self.pcomment = tk.Entry(self)
        self.pcomment.grid(row=row + 3, column=col + 1, rowspan=2)
