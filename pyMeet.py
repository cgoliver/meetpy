#! /Users/carlosgonzalezoliver/anaconda/envs/py35/bin/python

#### TODO ######################
# - Load existing DataFrame
# - Write results 
# - Write DataFrame to file
# - Toggle heats/events
# - Standings
# - Names autocomplete
# - Check time input format, convert to datetime 
#################################

from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd

class Application:
    def __init__(self, master):
        self.master = master

        #meet data
        # self.dfcolumns = ['Name', 'Club', 'Event', 'Heat', 'Lane', 'Time', \ 
        # 'Position', 'Points']
        self.dfcolumns = ['Name', 'Race', 'Swim', 'Lane', 'Time', \
            'Position', 'Points']
        self.data = pd.DataFrame(columns=self.dfcolumns)
        self.swimmers = list() 

        #heat data
        self.names = list()
        self.times = list()
        self.current_event = 1
        self.current_heat = 1
        self.current_race = 1

        #generate display
        master.title("meetpy")
        # self.load_images(master)
        self.create_navigation(master, row=1)
        self.create_lanes(master)
        self.create_update_button(master)
        self.create_load_buttons(master)
        self.create_heat_results(master)
        self.create_rankings(master)


    def create_navigation(self,master, row=1, col=1):
        self.prev_button = Button(master, text="<", command=lambda :\
            self.change_page("prev"))

        self.prev_button.grid(row=row, column=col)

        self.next_button = Button(master, text=">", command=lambda :\
            self.change_page("next"))
        self.next_button.grid(row=row, column=col+4)

        ## EVENT, HEAT TEXT BOXES
        # self.event_number = Entry(master)
        # self.event_number.grid(row=row, column=col+1)

        Label(master, text="Race:").grid(row=row, column=col+1)
        self.race_label = StringVar()
        self.race_label.set("1")
        self.heat_number = Label(master, textvar=self.race_label)
        self.heat_number.grid(row=row, column=col+2)

        ## EVENT TYPE DROPDOWN
        self.swim = StringVar(master)
        self.swim.set("100 IM")
        self.swim_type = OptionMenu(master,self.swim, "50 FR", "100 FR",\
            "100 IM", "4x50 FR", "4x50 IM")
        self.swim_type.grid(row=1, column=col+3)

    def create_lanes(self, master, lanes=6, row=2, col=1):
        """
            Create lane rows
        """

        self.lanes_label = Label(master, text="Lane")
        self.lanes_label.grid(row=row, column=1)
        
        self.name_label = Label(master,text="Name")
        self.name_label.grid(row=row, column=col+1)
        
        self.times_label = Label(master, text="Time (min:sec:ms)")
        self.times_label.grid(row=row, column=col+2)

        for l in range(1, lanes+1):
            #lane labels
            lane_label = Label(master, text=str(l))
            lane_label.grid(row=row+l+1, column=col)
            #name entry
            en = Entry(master)
            en.grid(row=row+l+1, column=col+1)
            self.names.append(en)
            #time entry
            t = Entry(master)
            t.grid(row=row+l+1, column=col+2)
            self.times.append(t)


    def create_update_button(self, master, row=10, col=4):
        self.update_button = Button(master, text="Update",\
            command=self.update_results)
        self.update_button.grid(row=row, column=col)

    def create_load_buttons(self, master):
        self.load_swimmers_button = Button(master, text="Load Swimmers",\
            command=self.load_file)
        self.load_swimmers_button.grid(row=0, column=0)

        self.load_meet_button = Button(master, text="Load Meet", \
            command=self.load_file)
        self.load_meet_button.grid(row=1, column=0)

    def create_heat_results(self, master, row=2, col=7):
        Label(master, text="Position").grid(row=row, column=col)
        Label(master, text="Points").grid(row=row, column=col+1)
        
    def create_rankings(self, master, row=2, col=10):
        Label(master, text="Standings").grid(row=row, \
            column=col)
    def load_file(self):
        fname = askopenfilename()
        print(fname)

    def get_heat_positions(self, times):
        #sort indices by value in array
        indices = list(range(len(times)))
        indices.sort(key=lambda x:times[x])
        positions = [0] * len(indices)
        for i,x in enumerate(indices):
            positions[x] = int(i) + 1
        return positions

    def update_results(self):
    #append each swim in the DataFrame data
        heat_df = pd.DataFrame(columns=self.dfcolumns)
        heat_times = [t.get() for t in self.times]
        heat_positions = self.get_heat_positions(heat_times)
        heat_names = [n.get() for n in self.names]
        current_swim = [self.swim.get() for _ in range(len(self.names))]

        heat_df['Name'] = heat_names
        heat_df['Race'] = [self.current_race for _ in range(len(self.names))]
        heat_df['Lane'] = [i+1 for i in range(len(heat_times))]
        heat_df['Swim'] = current_swim
        heat_df['Time'] = heat_times
        heat_df['Position'] = heat_positions

        #if if current heat and event already in dataframe, update slice 
        if ((self.data['Race'] == self.current_race)).any(): 
            self.data.loc[(self.data.Race== self.current_race) , 'Time'] = \
                heat_times
            self.data.loc[(self.data.Race== self.current_race) , 'Name'] = \
                heat_names
            self.data.loc[(self.data.Race== self.current_race) , 'Position'] = \
                heat_positions
            self.data.loc[(self.data.Race== self.current_race) , 'Swim'] = \
                current_swim
            #else append slice 
        else:
            self.data = pd.concat([self.data, heat_df])
        self.data.to_html("meet.html")
    pass

    def print_names(self):
        for i, n in enumerate(self.times):
            print(i, n.get())
    def change_page(self, direction):
        if direction == "prev":
            self.current_race = max(1, self.current_race - 1)
        else:
            self.current_race = self.current_race + 1
        self.race_label.set(str(self.current_race))

    def load_images(self, master):
        mtc = PhotoImage(file="Images/small.gif")
        mtc_logo = Label(master, image=mtc)
        mtc_logo.pack(side="right")

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
