"""
This program analyzes the log file of the LIGGGHTS simulation
and cleans the data using pandas dataframe ready for data analysis. 
The trajectory and acceleration of monodisperse particles are plotted
to measure flight times. Using a simple root finding method and
locating the local maxima, the launch and collision times are
obtained. From which, the flight times are obtained.
"""

#importing important packages

import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt

#Initialization
gam=4
trial=0.051
start=216
with open("gamma{}\\{}\log.liggghts".format(gam,trial), "r") as file:
    data = file.readlines()[start:100218]
cleaneddata = []
for i in range(len(data)):
    test = data[i]
    cleaneddata.append(re.sub("\s+", ",", test.strip()) +"\n")
with open("gamma{}\\{}\cleaneddata{}.csv".format(gam,trial,gam), "w+") 
as newfile:
    for i in range(len(cleaneddata)):
        newfile.write(cleaneddata[i])
        
df = pd.read_csv("gamma{}\\{}\cleaneddata{}.csv".format(gam,trial,gam))
zpos5 = df["zpos"]

#Plotting the time versus height of the center of mass
tstart = 0
tend = 5
dt = 0.00000625
N1 = int(tstart/dt)
N = int(tend/dt)
ts = np.linspace(0,5,len(df))
g = 9.81
f = 1/0.1
om=2*np.pi*f
A = g*gam/(om**2)

#A = 0.005
#om = np.sqrt((gam*g)/A)
per = 2*np.pi/om
M = 0.2796017461694916
plt.figure(2, figsize = (12,5))
plt.plot(ts[N1:N], zpos5[N1:N], "red", label = "CM of the particles")
plt.plot(ts[N1:N], A*np.sin(om*ts[N1:N]), "dimgrey",
    label = "base of the container")
plt.fill_between(ts[N1:N], A*np.sin(om*ts[N1:N]),
    np.array([min(A*np.sin(om*ts[N1:N])) - 0.001 ]),
    color = "lightgray")
plt.xlabel("time (s)", size = 16)
plt.ylabel("height (m)", size = 16)
plt.xlim(4, tend)
plt.ylim(bottom = min(A*np.sin(om*ts[N1:N])) - 0.001)
plt.legend()
plt.show()

#Plotting the time versus acceleration of the center of mass

tstart =4
tend =5
fig, (ax1, ax2) = plt.subplots(2,1, figsize = (12,10), sharex = True)
plt.subplots_adjust(hspace = 0.015)

ax1.plot(ts[N1:N], df["zpos"][N1:N] , "red")
ax1.plot(ts[N1:N], A*np.sin(om*ts[N1:N]), "dimgrey")
ax1.fill_between(ts[N1:N], A*np.sin(om*ts[N1:N]),
    np.array([min(A*np.sin(om*ts[N1:N])) - 0.001 ]),
    color = "lightgray")
ax1.set_ylabel("height of CM (m)", size = 16)
ax1.set_ylim(bottom = min(A*np.sin(om*ts[N1:N])) - 0.001)
ax1.set_xlim(tstart,tend)
ax1.grid(which = "both", axis = "both")
ax2.set_ylim(bottom=-15, top=300)
ax2.plot(ts[N1:N], (df["zfrc"][N1:N])/M, "r.")
ax2.set_xlabel("time (s)", size = 16)
ax2.set_ylabel("acceleration of CM (m/s\u00b2)", size = 16)
ax2.grid(which = "both", axis = "both")

#Finding the launch and collision times using a root finding method
tstart = 3
tend = 5
dt = 5e-5
N1 = int(tstart/dt)
N = int(tend/dt)

tollg = 0.1
tollc = 1e-6
r = 1500

values = []
collision_times = []
g_times = []
gs = []

for i in range(N-N1):
    if (abs(max(df["zfrc"][N1+i-r:N1+i+r]) - df["zfrc"][N1+i]) < tollc
        and df["zfrc"][N1+i] >0):
        collision_times.append(dt*(N1+i))
        values.append((df["zfrc"][N1+i])/M)
for i in range(N-N1):
    if abs((df["zfrc"][N1+i])/M - -g)< tollg:
        t_ = dt*(N1+i)
        g_times.append(t_)
        gs.append((df["zfrc"][N1+i])/M)
g_times = np.array(g_times)
collision_times = np.array(collision_times)
axs_values = np.array(values)
j = len(collision_times) - 1
i = 0
flight = []
g_values = []
launch_times = []

for j in range(len(collision_times)):
    for i in range(len(g_times)):
        if (g_times[i] < collision_times[j]
            and g_times[i] > collision_times[j-1]):
                t_ = collision_times[j] - g_times[i]
                launch_times.append(g_times[i])
                flight.append(t_)
                break
flight_times = np.array(flight)
g_values = np.array(g_values)

for i in range(len(df["zfrc"])):
    if abs((df["zfrc"][i])/M - -g)< tollg:
        t_ = dt*i
        first = (t_, (df["zfrc"][i])/M)
        break
plt.figure(figsize = (24,5))
plt.plot(ts[0:N],[-g]*len(ts[0:N]),color = "dimgrey", linestyle = "--")
plt.plot(ts[0:N], (df["zfrc"][0:N])/M, color = "gray", marker = ".",
    linestyle = "None")
plt.xlabel("time", size = 16)
plt.ylabel("acceleration of CM(m/s^2)", size = 16)
for i in range(len(collision_times)):
    plt.plot(collision_times[i], axs_values[i], "ro")
    plt.annotate("({})".format(np.around(collision_times[i], 4)),
             (collision_times[i], axs_values[i]), size = 12)

for i in range(len(launch_times)):
    plt.plot(launch_times[i], -g, color = "blue", marker = "o",
        linestyle = "None")
    plt.annotate("({})".format(np.around(launch_times[i], 4)),
        (launch_times[i], -g), size = 12)
    

plt.xlabel("time (s)", size = 16)
plt.ylabel("acceleration (m/s\u00b2)", size = 16)
plt.xlim(tstart, tend)
plt.ylim(-25,200)
plt.show()