import pylab
import numpy as np
from datetime import datetime
from secondary_rate_model import plot_final_rate, plot_semilog_rate


# create params for this
# https://github.com/curvefi/curve-stablecoin/blob/master/contracts/mpolicies/SecondaryMonetaryPolicy.vy

def plot_rate(alpha, beta, u0, r0, *args, **kw):
    u_inf = (beta - 1) * u0 / ((beta - 1) * u0 - (1 - u0) * (1 - alpha))
    A = (1 - alpha) * (u_inf - u0) * u_inf / u0
    r_minf = alpha - A / u_inf
    printout = (f"""
    alpha = {alpha} # < 1, if 0.01, than rate is 0.1%/0.001 at 0% utilization  (0.01 * 0.1 = 0.001) and r0 = 0.1
    beta = {beta} # > 1, if 2.5, than rate is 25%/0.25 at 100% utilization and r0 = 0.1
    u0 = {u0} # target utilization, at this point rate is 0.10%, as r0 is = 0.1
    r0 = {r0} # base rate of pool, set fixed at 0.1

    'u_inf' : {u_inf},
    'r_minf' : {r_minf},
    'A' : {A},

    """)
    u = np.linspace(0, 1, 100)
    r = r_minf + A / (u_inf - u)
    r = r * r0
    for u_val, r_val in zip(u, r):
        printout += (f"u = {u_val}, r = {r_val}\n")
    pylab.plot(u, r, *args, linewidth=0.8, **kw)  # Set desired linewidth here
    return printout, u_inf, r_minf, A


if __name__ == '__main__':

    r0 = 0.1 # base rate of pool, set fixed at 1, neutral value

    plot_semilog_rate(0.005, 0.25, '--', c='gray')

    printout = ""
    c = "purple"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.01, 2.5, 0.92, r0, '', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, 0, r0, c)
    
    c = "blue"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.01, 2.5, 0.9, r0, '', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, 0, r0, c)

    c = "lightgreen"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.1, 2.5, 0.9, r0 * 1.2, '', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, 0, r0, c)

    c = "red"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.5, 2.5, 0.9, r0, '', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, 1, r0, c)

    c = "black"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.5, 2.5, 0.9, r0, '', c=c)
    printout += temp_printout

    # from Hyperbolic Rate Model output
    # parameters: (1000000000, 1049562682215743440, 148254553799862302, 8746355685131196, 0)
    # parameters: [r_0,u_inf,A,r_minf,shift]

    parameters = (1000000000, 1049562682215743440, 148254553799862302, 8746355685131196, 0)
    printout += f"\n\n{parameters}\n"
    # example output from Hyperbolic Rate Model
    # 'u_inf' : 1.079136690647482,
    # 'r_minf' : -0.18705035971223008,
    # 'A' : 0.2126442730707519,

    u_inf = parameters[1] / 10**18
    r_minf = parameters[3] / 10**18
    A = parameters[2] / 10**18
    r0 = parameters[0] / 10**10
    shift = parameters[4]

    c = "yellow"
    printout += f"\n\n{u_inf}, {r_minf}, {A}, {r0}, {shift}\n"

    plot_final_rate(u_inf, r_minf, A, 0, r0, c)


    


    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = f"{timestamp}_rate_secondary_combined"

    # Save printout to a file
    with open(f'data/{name}.txt', 'w') as f:
        f.write(printout)

    print(printout)
    pylab.title("Secondary Rate Model, grey is semilog as reference")
    pylab.grid()
    pylab.xlabel('Utilization')
    pylab.ylabel('r (%)')
    pylab.xlim(-0.05, 1.05)
    pylab.ylim(-3 * r0 * 0.05, 3 * r0 * 1.05)
    pylab.savefig(f'data/{name}.svg', dpi=300, bbox_inches='tight')  # Change to .svg
    pylab.savefig(f'data/{name}.png', dpi=300, bbox_inches='tight')  # Change to .svg

    pylab.show()

