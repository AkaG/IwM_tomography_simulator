import tkinter as tk
from tkinter.filedialog import askopenfilename

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

        self._algorithminfo(0, 0)
        self._pinfo(0, 3)

        self.ct = ct()

        self.fig = Figure(figsize=(10, 5), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        toolbar_frame = tk.Frame(self)
        toolbar = NavigationToolbar2TkAgg(self.canvas, toolbar_frame)
        toolbar.update()

        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=5)
        toolbar_frame.grid(row=6, column=0, columnspan=5)

        self.readbutton = tk.Button(self, text="Load file", command=lambda: self.loadImage(), width=10)
        self.readbutton.grid(row=4, column=0)

        self.savebutton = tk.Button(self, text="Save file", command=lambda: self.saveImage(), width=10)
        self.savebutton.grid(row=4, column=1)

        self.generatebutton = tk.Button(self, text="Generate", command=lambda: self.generateButtonFunc(), width=10)
        self.generatebutton.grid(row=4, column=2)

    def loadImage(self):
        self.ct.loadImage(self._get_file_name())
        ax = self.fig.add_subplot(231)
        ax.clear()
        ax.imshow(self.ct.image, cmap=cm.Greys_r, vmin=0, vmax=1)
        self.canvas.draw()

    def saveImage(self):
        self._get_file_name()

    def generateButtonFunc(self):
        self.ct.step = float(self.step.get())
        self.ct.n = int(self.emittercount.get())
        self.ct.phi = int(self.spread.get())

        ax = self.fig.add_subplot(232)
        ax2 = self.fig.add_subplot(233)

        self.ct.generateSinogram(animate=lambda x,y : self.animate(x, y, [ax, ax2]))

        ax.clear()
        ax.imshow(self.ct.sinogram, cmap=cm.Greys_r, vmin=amin(self.ct.sinogram), vmax=amax(self.ct.sinogram))
        self.canvas.draw()

        ax2.clear()
        ax2.imshow(self.ct.lines, cmap=cm.Greys_r, vmin=amin(self.ct.lines), vmax=amax(self.ct.lines))
        self.canvas.draw()

        ax = self.fig.add_subplot(234)
        ax.clear()
        ax.imshow(self.ct.sinogram, cmap=cm.Greys_r, vmin=amin(self.ct.sinogram), vmax=amax(self.ct.sinogram))
        self.canvas.draw()

    def animate(self, res, cpy, axis):
        axis[0].clear()
        axis[1].clear()
        axis[0].imshow(res, cmap=cm.Greys_r, vmin=0, vmax=amax(res))
        axis[1].imshow(cpy, cmap=cm.Greys_r, vmin=0, vmax=1)
        self.canvas.draw()
        # plt.pause(0.000001)
    def _get_file_name(self):
        return askopenfilename(filetypes=(("JPG", "*.jpg"),
                                          ("PNG", "*.png"),
                                          ("DICOM", "*.dcm"),
                                          ("All files", "*.*")))

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
        self.pAgePage = tk.Entry(self)
        self.pAgePage.grid(row=row + 2, column=col + 1)

        self.pdatelabel = tk.Label(self, text="Date")
        self.pdatelabel.grid(row=row + 3, column=col)
        self.pdatepage = tk.Entry(self)
        self.pdatepage.grid(row=row + 3, column=col + 1)

        self.pcommentlabel = tk.Label(self, text="Comment")
        self.pcommentlabel.grid(row=row + 4, column=col)
        self.pcommentpage = tk.Entry(self)
        self.pcommentpage.grid(row=row + 4, column=col + 1)
