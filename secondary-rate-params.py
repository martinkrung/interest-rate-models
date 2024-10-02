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
    alpha = {alpha} # 0.01 is 1% at 100% utilization and r0 = 1
    beta = {beta} # 0.01 is 1% at 100% utilization and r0 = 1
    u0 = {u0} # convexness
    r0 = {r0} # scale for beta ? 10 is = 1 

    'u_inf' : {u_inf},
    'r_minf' : {r_minf},
    'A' : {A},

    """)
    u = np.linspace(0, 1, 200)
    r = r_minf + A / (u_inf - u)
    r = r * r0
    pylab.plot(u, r, *args, **kw)
    return printout, u_inf, r_minf, A





if __name__ == '__main__':
    beta = 3
    r0 = 1

    plot_semilog_rate(0.01, 2.5, '', c='gray')

    printout = ""
    c = "purple"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.01, 2.5, 0.9, r0, '--', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, c)
    
    c = "blue"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.005, 2.5, 0.9, r0, '--', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, c)

    c = "lightgreen"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.02, 2.5, 0.95, r0, '--', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, c)

    c = "red"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.02, 2.5, 0.99, r0, '--', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, c)

    c = "black"
    printout += f"\n\n{c}\n"
    temp_printout, u_inf, r_minf, A = plot_rate(0.03, 2.5, 0.8, r0, '--', c=c)
    printout += temp_printout
    plot_final_rate(u_inf, r_minf, A, c)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = f"{timestamp}_rate_secondary_susde"

    # Save printout to a file
    with open(f'data/{name}.txt', 'w') as f:
        f.write(printout)

    print(printout)
    pylab.title("Secondary Rate Model, grey is semilog as reference")
    pylab.grid()
    pylab.xlabel('Utilization')
    pylab.ylabel('r (%)')
    pylab.xlim(-0.05, 1.05)
    pylab.ylim(-beta * r0 * 0.05, beta * r0 * 1.05)
    pylab.savefig(f'data/{name}.png', dpi=300, bbox_inches='tight')
    pylab.show()

