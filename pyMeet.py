#! /Users/carlosgonzalezoliver/anaconda/envs/py35/bin/python

#### TODO ######################
# - Standings
# - Names database
# - Load names
# - Handle name not in database
# - Close window button
# - Handle message when no file chosen
# - Check time input format, convert to datetime 
#################################

from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd
import AutocompleteEntry

class Application:
    def __init__(self, master):
        self.master = master

        #meet data
        # self.dfcolumns = ['Name', 'Club', 'Event', 'Heat', 'Lane', 'Time', \ 
        # 'Position', 'Points']
        self.dfcolumns = ['Name', 'Race', 'Swim', 'Lane', 'Time', \
            'Position', 'Points']
        self.data = pd.DataFrame(columns=self.dfcolumns)
        self.swimmers = dict()

        #heat data
        self.current_event = 1
        self.current_heat = 1
        self.current_race = 1

        #generate display
        master.title("meetpy -- by cgoliver")
        # self.load_images(master)
        self.create_navigation(master, row=1)
        self.create_lanes(master)
        self.create_update_button(master)
        self.create_load_buttons(master)
        self.create_heat_results(master)
        self.create_rankings(master)
        self.create_swimmer_enter_button(master)
        self.create_export_buttons(master)

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
        self.swim.set("Race type")
        self.swim_type = OptionMenu(master,self.swim, "50 FR", "100 FR",\
            "100 IM", "4x50 FR", "4x50 IM")
        self.swim_type.grid(row=1, column=col+3)

    def create_lanes(self, master, lanes=6, row=2, col=1):
        """
            Create lane rows
        """
        self.names = list()
        self.names_text = list()

        self.times = list()
        self.times_text = list()

        self.lanes_label = Label(master, text="Lane")
        self.lanes_label.grid(row=row, column=1)
        
        self.name_label = Label(master,text="Name")
        self.name_label.grid(row=row, column=col+1)
        
        self.times_label = Label(master, text="Time (min:sec:ms)")
        self.times_label.grid(row=row, column=col+2)

        self.name_entry = list()
        for l in range(1, lanes+1):
            #lane labels
            lane_label = Label(master, text=str(l))
            lane_label.grid(row=row+l+1, column=col)
            #name entry
            name_text = StringVar()

            en = AutocompleteEntry.AutocompleteEntry(master, textvar=name_text)
            en.set_completion_list(self.swimmers.keys())
            name_text.set("")
            en.grid(row=row+l+1, column=col+1)
            self.names.append(en)
            self.names_text.append(name_text)
            self.name_entry.append(en)

            #time entry
            time_text = StringVar()
            t = Entry(master, textvar=time_text)
            time_text.set("")
            t.grid(row=row+l+1, column=col+2)
            self.times.append(t)
            self.times_text.append(time_text)


    def create_update_button(self, master, row=10, col=4):
        self.update_button = Button(master, text="Update",\
            command=self.update_results)
        self.update_button.grid(row=row, column=col)
        self.update_status = StringVar()
        self.update_status.set(" ")
        Label(master, textvar=self.update_status).grid(row=row, column=col+1)


    def create_export_buttons(self, master, row=8, col=0):
        Button(master, text="Export meet", command=\
            lambda : self.file_save('meet')).grid(row=row, column=col)
        Button(master, text="Export swimmers", command=\
            lambda : self.file_save('swimmers')).grid(row=row+1, column=col)

        pass
    def file_save(self, master):
        pass
    def swimmer_entry_window(self, master):
        w = Toplevel()
        w.title("Swimmer Entry")

        Label(w, text="Name").grid(row=0, column=0)
        s = Entry(w)
        s.grid(row=1, column=0)

        club = StringVar(master)
        club.set("Choose club")
        Label(w, text="Club").grid(row=0, column=1)
        OptionMenu(w, club, "MTC", "MUMS").grid(row=1, column=1)

        Button(w, text="Enter", command=lambda : \
            self.append_swimmer(s.get(), club.get())).grid(row=1, column=2)
        pass

    def append_swimmer(self, swimmer, club):
        self.swimmers.setdefault(swimmer, club)
        for n in self.name_entry:
            n.set_completion_list(self.swimmers.keys())
        print(self.swimmers)
        pass

    def create_swimmer_enter_button(self, master, row=10, col=1):
        Button(master, text="Enter swimmer", \
            command=lambda : self.swimmer_entry_window(master)).grid(row=row,\
                column=col)
    def create_load_buttons(self, master):
        self.load_swimmers_button = Button(master, text="Load Swimmers",\
            command=lambda : self.load_file(master))
        self.load_swimmers_button.grid(row=0, column=0)

        self.load_meet_button = Button(master, text="Load Meet", \
            command=self.load_file)
        self.load_meet_button.grid(row=1, column=0)

    def create_heat_results(self, master, lanes=6, row=2, col=7):
        Label(master, text="Position").grid(row=row, column=col)
        Label(master, text="Points").grid(row=row, column=col+1)

        self.position_vars = []
        self.points_vars = []

        for i in range(lanes):
            r = StringVar()
            l = Label(textvar=r)
            l.grid(row=row+2+i, column=col)
            self.position_vars.append(r)

            p = StringVar()
            pl = Label(textvar=p)

            pl.grid(row=row+2+i, column=col+1)

            self.points_vars.append(p)

    def update_text(self):
        """
            Fill values in text boxes for current race
        """
        self.update_status.set(" ")
        race_info = self.data.loc[self.data['Race'] == self.current_race]

        if not race_info.empty:
            for i, (name, time) in enumerate(zip(race_info['Name'],\
                race_info['Time'])):

                self.names_text[i].set(name)
                self.times_text[i].set(time)
        else:
                for i in range(len(self.names_text)):
                    self.names_text[i].set(" ")
                    self.times_text[i].set(" ")

        pass
    def create_rankings(self, master, lanes=6, row=2, col=10):
        Label(master, text="Standings").grid(row=row, \
            column=col)

    def message_window(self, master, message):
        w = Toplevel()
        Label(w, text=message).pack()

    def load_file(self, master):
        fname = askopenfilename()
        try:
            self.data = pd.DataFrame.from_csv(fname)
        except:
            self.message_window(master, "Invalid file. Try again.") 

        print(fname)

    def get_heat_positions(self, times):
        #sort indices by value in array
        indices = list(range(len(times)))
        indices.sort(key=lambda x:times[x])
        positions = [0] * len(indices)
        for i,x in enumerate(indices):
            positions[x] = int(i) + 1
        return positions

    def compute_points(self, positions):
        points = {1: 12, 2: 10, 3: 8, 4: 6, 5: 4, 6: 2}
        return [points[r] for r in positions]
    def update_results(self):
    #append each swim in the DataFrame data
        heat_df = pd.DataFrame(columns=self.dfcolumns)
        heat_times = [t.get() for t in self.times]
        heat_positions = self.get_heat_positions(heat_times)
        heat_names = [n.get() for n in self.names]
        current_swim = [self.swim.get() for _ in range(len(self.names))]
        points = self.compute_points(heat_positions)

        heat_df['Name'] = heat_names
        heat_df['Race'] = [int(self.current_race) for _ in range(len(self.names))]
        heat_df['Lane'] = [i+1 for i in range(len(heat_times))]
        heat_df['Swim'] = current_swim
        heat_df['Time'] = heat_times
        heat_df['Position'] = heat_positions
        heat_df['Points'] = points

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
            self.data.loc[(self.data.Race== self.current_race) , 'Points'] = \
                points 
            #else append slice 
        else:
            self.data = pd.concat([self.data, heat_df])
        #update rankings and points
        for i in range(len(self.names)):
            self.position_vars[i].set(heat_positions[i])
            self.points_vars[i].set(points[i])

        self.update_status.set("Info updated!")
        self.data.to_csv("meet_backup.csv")
    pass

    def print_names(self):
        for i, n in enumerate(self.times):
            print(i, n.get())
    def change_page(self, direction):
        if direction == "prev":
            self.current_race = int(max(1, self.current_race - 1))
        else:
            self.current_race = int(self.current_race + 1)
        self.race_label.set(str(self.current_race))
        self.update_text()

    def load_images(self, master):
        mtc = PhotoImage(file="Images/small.gif")
        mtc_logo = Label(master, image=mtc)
        mtc_logo.pack(side="right")

    def quit(self, root):
        root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
