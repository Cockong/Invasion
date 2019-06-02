import Tkinter as tk
import tkFileDialog
import random
import world



class WorldView(tk.Canvas):

	def __init__(self, parent):
		tk.Canvas.__init__(self, parent, width = 400, height = 400, highlightthickness=0, bg = "black")
		self.size_in_pixels = 400
		self.ovals = []

	def draw_grid(self, grid_size):
		self.w = grid_size
		self.h = grid_size
		self.pixels_per_slot = int(self.size_in_pixels)/self.w
		for i in range(self.h + 1):
			self.create_line(0, i*self.pixels_per_slot, self.w*self.pixels_per_slot, i*self.pixels_per_slot, fill="#3c3c3c")
		for j in range(self.w + 1):
			self.create_line(j*self.pixels_per_slot, 0, j*self.pixels_per_slot, self.h*self.pixels_per_slot, fill="#3c3c3c", width=0)

	
	@staticmethod
	def get_color(ag):
		if ag.nP+ ag.nR+ ag.nV != 0:
			if (max(ag.nP, ag.nR, ag.nV) == ag.nP):
				color = "yellow"
			elif (max(ag.nP, ag.nR, ag.nV) == ag.nR):
				color = "red"
			elif (max(ag.nP, ag.nR, ag.nV) == ag.nV):
				color = "green"
	
		else:
			color = "black"
		return color


	def draw_ovals(self, pop):
		self.ovals_radius = int(self.pixels_per_slot/3)
		for ag in pop:
			for indiv in ag:
				index = self.create_oval((indiv.x+0.5)*self.pixels_per_slot - self.ovals_radius, 
										(indiv.y+0.5)*self.pixels_per_slot - self.ovals_radius, 
										(indiv.x+0.5)*self.pixels_per_slot + self.ovals_radius,
										(indiv.y+0.5)*self.pixels_per_slot + self.ovals_radius, 
										fill=self.get_color(indiv))
				self.ovals.append(index)

	def update_ovals(self, pop):
		for i in range(len(pop)):
			for j in range(len(pop[i])):
				ag = pop[i][j]
				oval = self.ovals[len(pop[i])*i + j]
				self.itemconfig(oval, fill=self.get_color(ag))
				self.coords(oval, (ag.x+0.5)*self.pixels_per_slot - self.ovals_radius, 
									(ag.y+0.5)*self.pixels_per_slot - self.ovals_radius, 
									(ag.x+0.5)*self.pixels_per_slot + self.ovals_radius, 
									(ag.y+0.5)*self.pixels_per_slot + self.ovals_radius)

	def erase(self):
		del self.ovals[:]
		self.ovals = []
		self.delete("all")


class View(tk.Tk):

	def __init__(self, controller):
		tk.Tk.__init__(self)
		self.controller = controller
		self.title("SIR simulation")
		self.buildUI()

	def buildUI(self):
		tk.Label(self, text='Grid size:', anchor="sw", justify="left").grid(row=0, column=0, sticky="WS")
		self.grid_size_scale = tk.Scale(self, from_=10, to=100, resolution=1, orient='horizontal', length=200)
		self.grid_size_scale.grid(row=0, column=1, sticky="W")

		tk.Label(self, text='Number of agents:', anchor="sw", justify="left").grid(row=0, column=2, sticky="WS")
		self.nb_agents_scale = tk.Scale(self, from_=0, to=500, resolution=10, orient='horizontal', length=200)
		self.nb_agents_scale.grid(row=0, column=3, sticky="W")


		buttons_frame = tk.Frame(self)
		tk.Button(buttons_frame, text='Create grid', command=self.controller.create_world).pack(side="left")
		tk.Button(buttons_frame, text='Select output file name', command=self.controller.select_output_file).pack(side="left")
		tk.Button(buttons_frame, text='Reset', command=self.controller.reset).pack(side="left")
		buttons_frame.grid(row = 5, column = 0, columnspan = 4)


		self.worldview = WorldView(self)
		self.worldview.grid(row=6,column=0, columnspan=2, rowspan=3)

		tk.Button(self, text='Run', command=self.controller.play).grid(row=6, column=2, sticky="wnes")
		tk.Button(self, text='Pause', command=self.controller.pause_action).grid(row=6, column=3, sticky="wnes")

		tk.Label(self, text='Speed:', anchor="sw", justify="left").grid(row=7, column=2, sticky="wn")
		self.speed_scale = tk.Scale(self, from_=5, to=500, resolution=5, orient='horizontal', length=200, showvalue=0)
		self.speed_scale.set(50)
		self.speed_scale.grid(row=7, column=3, columnspan=2, sticky="wn")

		stats_frame = tk.Frame(self)
		self.message0 = tk.Message(stats_frame, text='t = 0', width=200, anchor="w")
		self.message0.pack(anchor="w", expand=1, fill="x")
		self.message1 = tk.Message(stats_frame, foreground="yellow", width=200, anchor="w")
		self.message1.pack(anchor="w", expand=1, fill="x")
		self.message2 = tk.Message(stats_frame, foreground="red", width=200, anchor="w")
		self.message2.pack(anchor="w", expand=1, fill="x")
		self.message3 = tk.Message(stats_frame, foreground="green", width=200, anchor="w")
		self.message3.pack(anchor="w", expand=1, fill="x")
		stats_frame.grid(row = 8, column=2, columnspan=2, sticky="wn")

		for child in self.winfo_children():
			child.grid_configure(padx=10, pady=5)
		self.worldview.grid_configure(padx=10, pady=10)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)

	def reset_scales_values(self, grid_size, nb_agents):
		self.grid_size_scale.set(grid_size)
		self.nb_agents_scale.set(nb_agents)

	def set_counters(self, t=0, nb_susc=0, nb_infect=0, nb_recov=0, nb_dead=0):
		self.message0.config(text="t="+ str(t))
		self.message1.config(text=str(nb_susc)+" Poule")
		self.message2.config(text=str(nb_infect)+" Renard")
		self.message3.config(text=str(nb_recov)+" Vipere")

	def get_speed_value(self):
		return self.speed_scale.get()

	def get_grid_size(self):
		return self.grid_size_scale.get()

	def get_nb_agents(self):
		return self.nb_agents_scale.get()

	def get_p_i(self):
		return self.p_i_scale.get()

	def get_p_r(self):
		return self.p_r_scale.get()

	def get_p_d(self):
		return self.p_d_scale.get()

	def get_init_prop(self):
		return self.init_prop_scale.get()



class Controller(object):
	
	def __init__(self):
		self.pause = False
		self.world = world.World()
		self.filename = ""
		self.output_file = None
		self.t = 0
		self.default_grid_size = 30
		self.default_nb_agents = 100
		self.default_p_i_value = 1.0
		self.default_p_r_value = 0.01
		self.default_p_d_value = 0.001
		self.default_init_prop = 0.2
		self.view = View(self)
		self.view.reset_scales_values(self.default_grid_size, self.default_nb_agents)
		self.view.set_counters()
		self.view.mainloop()

	def create_world(self):
		grid_size = self.view.grid_size_scale.get()
		nb = self.view.nb_agents_scale.get()
		self.world = world.World(grid_size, grid_size, nb, nb, nb)
		self.view.worldview.draw_grid(grid_size)
		self.view.worldview.draw_ovals(self.world.pop)

	def play(self):
		self.pause = False
		self.update()

	def update_stats(self):
		self.view.set_counters(self.t, self.world.nP, self.world.nR, self.world.nV)
		if (self.output_file != None):
			self.output_file.write("{0} {1} {2} {3}\n".format(self.t, self.world.nP, self.world.nR, self.world.nV))

	def update(self):
		self.world.move()
		self.world.eat()
		self.view.worldview.update_ovals(self.world.pop)
		self.update_stats()
		self.t += 1
		if not self.pause:
			waiting_time = int(5000.0/self.view.get_speed_value())
			self.view.after(waiting_time, self.update)

	def create_agents(self):
		self.world.create_agents(self.view.get_nb_agents(), 
									self.view.get_init_prop(), 
									self.view.get_p_i(), 
									self.view.get_p_r(), 
									self.view.get_p_d())
		self.view.worldview.draw_ovals(self.world.pop)
		self.update_stats()

	def pause_action(self):
		self.pause = True

	def reset(self):
		if self.output_file != None:
			self.output_file.close()
			self.output_file = None
		self.filename = ""
		#self.world.erase()
		self.world = None
		self.t = 0
		self.view.worldview.erase()
		self.view.reset_scales_values(self.default_grid_size, self.default_nb_agents)
		self.view.set_counters()


	def select_output_file(self):
		self.filename = tkFileDialog.asksaveasfilename(title = "Select file")
		self.output_file = open(self.filename, "w")
		self.output_file.write("# time nb_susceptibles nb_infectious nb_recovered nb_dead\n")





app = Controller()




