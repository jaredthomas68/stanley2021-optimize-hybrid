import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from math import sin, cos, radians
import scipy.interpolate
import json

if __name__=='__main__':

    
    fig = plt.figure(figsize=[6,2])


    ax = plt.subplot(131)
    ax.set_title("dimensions",fontsize=8)
    bladeX = np.array([3.,7.,10.,15.,20.,25.,30.,35.,30.,25.,20.,15.,10.,5.,3.,3.])
    bladeY = np.array([0.,0.,0.8,1.5,1.7,1.9,2.1,2.3,2.4,2.4,2.4,2.4,2.4,2.4,2.4,0.])-1.5


    N = 12
    r1 = 5
    r2 = 3
    
    # H = 88.0
    # D = 116.0
    H = 135.0
    D = 200.0
    R = D/2.0
    d = np.array([6.3,5.5,4.])*D/200.0

    circle1 = plt.Circle((0.,H), R, color='C0', fill=False, linestyle = '--', linewidth=1.2*1.5)
    ax.add_artist(circle1)

    c1 = R/35.

    px1 = np.array([0.-d[0]/2,0.-d[1]/2,0.-d[2]/2,0.+d[2]/2,0.+d[1]/2,0.+d[0]/2,0.-d[0]/2])
    py1 = np.array([0,H/2,H-3.*c1,H-3.*c1,H/2,0,0])
    ax.plot(px1,py1,color='C0', linewidth=1.2*1.5)

    #add blades
    hub1 = plt.Circle((0.,H), 3*c1, color='C0', fill=False, linewidth=1*1.5)
    ax.add_artist(hub1)

    angle1 = 92.0

    blade1X = bladeX*cos(radians(angle1))-bladeY*sin(radians(angle1))
    blade1Y = bladeX*sin(radians(angle1))+bladeY*cos(radians(angle1))

    blade2X = bladeX*cos(radians(angle1+120.))-bladeY*sin(radians(angle1+120.))
    blade2Y = bladeX*sin(radians(angle1+120.))+bladeY*cos(radians(angle1+120.))

    blade3X = bladeX*cos(radians(angle1+240.))-bladeY*sin(radians(angle1+240.))
    blade3Y = bladeX*sin(radians(angle1+240.))+bladeY*cos(radians(angle1+240.))

    ax.plot(blade1X*c1+0., blade1Y*c1+H, linewidth=1*1.5, color='C0')
    ax.plot(blade2X*c1+0., blade2Y*c1+H, linewidth=1*1.5, color='C0')
    ax.plot(blade3X*c1+0., blade3Y*c1+H, linewidth=1*1.5, color='C0')

    # plot rotor diameter text
    rot_angle = 50.0
    s = np.sin(np.deg2rad(rot_angle))
    c = np.cos(np.deg2rad(rot_angle))
    ax.plot([-R*c,R*c],[-R*s+H,R*s+H],"-",color="k")

    s2 = np.sin(np.deg2rad(rot_angle+90))
    c2 = np.cos(np.deg2rad(rot_angle+90))
    L = 10
    ax.plot([-R*c-L*c2,-R*c+L*c2],[-R*s+H-L*s2,-R*s+H+L*s2],"-",color="k")
    ax.plot([R*c-L*c2,R*c+L*c2],[R*s+H-L*s2,R*s+H+L*s2],"-",color="k")

    ax.text(R-40,H+15,"%s m"%round(D),horizontalalignment="center",fontsize=8)

    # plot hub height text
    ax.plot([-R-10,-R-10],[0,H],"-k")
    ax.plot([-R-10-L,-R-10+L],[0,0],"-k")
    ax.plot([-R-10-L,-R-10+L],[H,H],"-k")

    ax.text(-R-L*4.5,H/2,"%s m"%round(H),verticalalignment="center",horizontalalignment="center",fontsize=8)

    ax.axis('square')
    ax.axis('off')
    ax.set_xlim(-R-L*2.5,R+L)
    ax.set_ylim(-2,H+R+L)
        

    ax = plt.subplot(132)
    ax.set_title("power curve",fontsize=8)
    filename = "high_7r_200d_135h"
    # filename = "low_2_43r_116d_88h"
    powercurve_filename = '/Users/astanley/Projects/finished_projects/stanley2021-optimize-hybrid/revision/turbine_data/%s.txt'%filename
    powercurve_file = open(powercurve_filename)
    powercurve_data = json.load(powercurve_file)
    powercurve_file.close()

    power_curve = powercurve_data['turbine_powercurve_specification']['turbine_power_output']
    wind_speeds = powercurve_data['turbine_powercurve_specification']['wind_speed_ms']
    A = [a/1E3 for a in power_curve]

    ax.plot(wind_speeds,A,color="C1")
    # ax.set_ylim(-0.1,3.0)
    ax.set_xlim(0.0,28.0)

    ax.set_xticks([3,10,25])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel("wind speed (m/s)",fontsize=8)
    # ax.set_yticks((1,2,2.43,3))
    ax.set_yticks((0,3.5,7))
    ax.tick_params(axis='both', labelsize=8)
    ax.set_ylabel("power (MW)",fontsize=8)
    # ax.set_yticklabels(("1","2","2.43","3"))




    ax = plt.subplot(133)
    ax.set_title("cost curve",fontsize=8)
    # capex_cost_real = np.array([2*1382.0,1382.0,1124.0,966.0,887.0,849.0,792.0,765.0]) # $/kW realistic
    # capex_size = np.array([1.0,20.0,50.0,100.0,150.0,200.0,400.0,1000.0]) # MW
    # cost = capex_size*capex_cost_real*1000.0
    # f = scipy.interpolate.interp1d(capex_size,cost,kind='cubic')

    wind_cost = np.array([5*1786.0,1786.0,1622.0,1528.0,1494.0,1470.0,1421.0,1408.0])*1555.0/1494.0 # $/kW/year realistic
    wind_capacity = np.array([0.0,20.0,50.0,100.0,150.0,200.0,400.0,1000.0]) # MW
    f = scipy.interpolate.interp1d(wind_capacity, wind_cost*wind_capacity, kind='cubic')
    
    x = np.linspace(1E-6,300.0,100)
    ax.plot(x,f(x)/x,color="C2")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(axis='both', labelsize=8)
    ax.set_xlabel("wind capacity (MW)",fontsize=8)

    # ax.set_ylim(1550.0,max(f(x)/x))
    # ax.set_xlim((0,600))

    # ax.set_yticks((0.8,1.0,1.2,1.4,1.6,1.8))
    ax.set_ylabel("capex ($/kW)",fontsize=8)
    # ax.set_yticklabels(("0.8","1.0","1.2","1.4","1.6","1.8"))

        


    plt.subplots_adjust(top = 0.9, bottom = 0.2, right = 0.98, left = 0.04,wspace=0.4)
                # hspace = 0.4, wspace = 0.2)
    plt.savefig("figures/turbine_specs_3.pdf",transparent=True)
    plt.show()
