import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.odr import ODR, Model, RealData

def read_nps(filename):
    file = open(filename,"r")
    return float(file.readline().strip().split()[5])

def read_mcnp_output(filename):
    tallies = []
    vals = []
    uncs = []

    with open(filename, 'r') as file:
        data = file.readlines()
    nps = read_nps(filename) # normalizing factor
    tally_pattern = re.compile(r'tally\s+(\d+)\s+-?\d+\s+-?\d+\s+-?\d+')
    vals_pattern = re.compile(r'vals')

    tally_match, vals_match, unc_match = 0,0,0
    for line in data:
        tally_match = tally_pattern.match(line)
        if tally_match:
            tallies.append(int(tally_match.group(1)))

        #print(vals_match)
        if vals_match:
            val,unc = line.strip().split(" ")
            val_f = float(val)
            unc_f = float(val)
            vals.append(val_f)
            uncs.append(unc_f*val_f)
            #vals.append(list(map(float, vals_match.group(1).split())))
            #print(list(map(float, vals_match.group(1).split())))
        vals_match = vals_pattern.match(line)

    return tallies, vals, uncs

def F1_plot(tallies,vals,uncs,dists, fig = True):
    vals_plot,uncs_plot = [],[]
    for ind in range(len(tallies)):
        if tallies[ind] % 10 == 1:
            vals_plot.append(vals[ind])
            uncs_plot.append(uncs[ind])
    if fig: plt.figure()
    for ind in range(len(vals_plot)):
        vals_plot[ind] = vals_plot[ind] / (4*np.pi*dists[ind]*dists[ind])
    plt.xlabel("Distance (cm)")
    plt.ylabel("F2_measures")
    plt.plot(dists,vals_plot)
    return vals_plot, uncs_plot

def F2_plot(tallies,vals,uncs,dists, fig = True):
    vals_plot,uncs_plot = [],[]
    for ind in range(len(tallies)):
        if tallies[ind] % 10 == 2:
            vals_plot.append(vals[ind])
            uncs_plot.append(uncs[ind])
    if fig: plt.figure()
    plt.xlabel("Distance (cm)")
    plt.ylabel("F2_measures")
    plt.plot(dists,vals_plot)
    return vals_plot, uncs_plot

def F4_plot(tallies,vals,uncs,dists, fig = True):
    vals_plot,uncs_plot = [],[]
    for ind in range(len(tallies)):
        if tallies[ind] % 10 == 4:
            vals_plot.append(vals[ind])
            uncs_plot.append(uncs[ind])
    if fig: plt.figure()
    plt.xlabel("Distance (cm)")
    plt.ylabel("")
    plt.plot(dists,vals_plot)

def exp_inv_squared(params,x):
    A, B, C = params
    return A * np.exp(- x/B) / (x*x)

def fit_exp_sphere(tallies,vals,uncs,dists):
    vals_plot,uncs_plot = [],[]
    for ind in range(len(tallies)):
        if tallies[ind] % 10 == 2:
            vals_plot.append(vals[ind])
            uncs_plot.append(uncs[ind])

    x_err = [0.5] * len(vals_plot)
    y_err = []
    for tal in range(len(vals_plot)):
        y_err.append(vals_plot[tal]*0.1)
        print(vals_plot[tal],dists[tal])

    data = RealData(vals_plot,dists, sx = x_err, sy = y_err)
    model = Model(exp_inv_squared)
    odr = ODR(data, model, beta0 = [15138,100,12])
    output = odr.run()

    x_fit = np.linspace(min(dists),max(dists),int((max(dists)-min(dists))*20))
    y_fit = exp_inv_squared(output.beta,x_fit)

    print("Fitted parameters: A = {:.2f}, B = {:.4f}, C = {:.2f}".format(*output.beta))
    print("Standard errors: σA = {:.2f}, σB = {:.4f}, σC = {:.2f}".format(*output.sd_beta))
    plt.plot(x_fit,y_fit)

def geo_check(file_name):
    df_geo = pd.read_csv (file_name)

    geo_n = df_geo.iloc[:, 0].values.tolist()
    geo_x = df_geo.iloc[:, 1].values.tolist()
    geo_y = df_geo.iloc[:, 2].values.tolist()
    geo_z = df_geo.iloc[:, 3].values.tolist()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(geo_x,geo_y,geo_z)
    cyl_x=[]
    cyl_y=[]
    cyl_z=[]
    for cir in range(100):
        cyl_x.append(0.5*np.cos(cir/12.5*np.pi))
        cyl_y.append(0.5*np.sin(cir/12.5*np.pi))
        cyl_z.append(-3 + cir*0.06)
    ax.scatter(cyl_x,cyl_y,cyl_z)
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(-3,3)



# Reading data for plotting different shielding materials -----------
file_Pb  = "mctal/test_Pb.m"
file_BeO = "mctal/test_BeO.m"
file_Fe  = "mctal/test_Fe.m"
file_H2O = "mctal/test_H2O.m"

# tallies_Pb, vals_Pb, uncs_Pb    = read_mcnp_output(file_Pb)
# tallies_BeO, vals_BeO, uncs_BeO = read_mcnp_output(file_BeO)
# tallies_Fe, vals_Fe, uncs_Fe    = read_mcnp_output(file_Fe)
# tallies_H2O, vals_H2O, uncs_H2O = read_mcnp_output(file_H2O)

# Defining the distances to origin by hand
dists = [5,6,7,8,9,10]
dist2 = [5,6,7,8,9]
# -------------------------------------------------------------------

tallies, vals, uncs    = read_mcnp_output("mctal/test_ficha_1i.m")
vals_F1, uncs_F1 = F1_plot(tallies, vals, uncs   ,dists)
vals_F2, uncs_F2 = F2_plot(tallies, vals, uncs   ,dists, fig = False)
plt.legend(["F1","F2"])

mu = []
for i in range(len(vals_F1)):
    mu.append(vals_F1[i]/vals_F2[i])
print(mu)
# fit_exp_sphere(tallies_Pb, vals_Pb, uncs_Pb   ,dists)
# F2_plot(tallies_BeO, vals_BeO, uncs_BeO,dists,fig=False)
# F2_plot(tallies_Fe, vals_Fe, uncs_Fe   ,dists,fig=False)
# F2_plot(tallies_H2O, vals_H2O, uncs_H2O,dists,fig=False)
#plt.legend(["Pb","fit"]) # ,"BeO","Fe","H₂O"
# F4_plot(tallies,vals,uncs,dist2,fig=False)
# plt.yscale("log")

#   ## geometry check
# geo_name = "geo_check.txt"
# geo_check(geo_name)

plt.show()
# for tally, val, uncertainty in zip(tallies, vals, uncs):
#     print(f"Tally Number: {tally}")
#     print("Vals:", val)
#     print("Uncertainties:", uncertainty)
#     print()