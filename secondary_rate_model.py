import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# plot curve for this
# https://github.com/curvefi/curve-stablecoin/blob/master/contracts/mpolicies/SecondaryMonetaryPolicy.vy

def calculate_rate(u, p, r0):
    if u >= p['u_inf']:
        return float('inf')  # Return infinity for u >= u_inf
    return r0 * p['r_minf'] + (p['A'] * r0) / (p['u_inf'] - u) + p['shift']

def plot_semilog_rate(rate_min, rate_max, *args, **kw):
    u = np.linspace(0, 1, 200)
    r = np.exp(u * (np.log(rate_max) - np.log(rate_min)) + np.log(rate_min))

    plt.plot(u, r, *args, **kw)

    
def plot_final_rate(u_inf, r_minf, A, shift, r0, c):

    p = {
        'u_inf' : u_inf,
        'r_minf' : r_minf,
        'A' : A,
        'shift': shift
    }

    # Generate data
    utilization = np.linspace(0, 1, 1000)  # Increased number of points for smoother curve
    rates = [calculate_rate(u, p, r0) for u in utilization]

    # Remove any infinite values
    valid_data = [(u, r) for u, r in zip(utilization, rates) if np.isfinite(r)]
    utilization, rates = zip(*valid_data)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(utilization, rates, '', color=c)
    plt.title('Interest Rate Model - grey is semilog as reference')
    plt.xlabel('Utilization')
    plt.ylabel('Interest Rate')
    plt.xlim(0, 1)

    # Set y-axis limit dynamically
    max_rate = max(rates)
    if np.isfinite(max_rate):
        plt.ylim(0, max_rate * 1.1)  # Set y-axis limit to 110% of max rate
    else:
        plt.ylim(0, 1)  # Set a default limit if max_rate is infinite

    # Format axes as percentages
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y:.2%}'))

    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # Annotate interest rates at each percentage point
    counter = 0
    for u, r in zip(utilization, rates):
        if counter % 100 == 0:
            plt.plot(u, r, 'x', markersize=8)
            plt.text(u, r, f'{r:.1%}, u: {u:.1%}', fontsize=8, ha='center', va='bottom')
        counter += 1


    # Add text below the x-axis
    plt.text(0.5, -0.1, f'A: {p["A"]}, shift: {p["shift"]}, r_minf: {p["r_minf"]}, u_inf: {p["u_inf"]}, r0: {r0}', ha='center', va='center', transform=plt.gca().transAxes)  # Adjust the y-coordinate as needed
    
    plot_semilog_rate(0.005, max_rate, '--', c='gray')

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Save the plot as a PNG file

    plt.savefig(f'data/{timestamp}_{c}_interest_rate_model_A:{p["A"]}_shift:{p["shift"]}_r_minf:{p["r_minf"]}_u_inf:{p["u_inf"]}_r0:{r0}.png', dpi=300, bbox_inches='tight')

    # Display the plot (optional, if running in an environment that supports it)

    plt.close()
    # Plotting a second file with u range from u_inf to 1
    plt.figure(figsize=(10, 6))
    plt.plot(utilization, rates, '', color=c)

    #plt.plot(np.linspace(p['u_inf'], 1, 1000), [calculate_rate(u, p, r0) for u in np.linspace(p['u_inf'], 1, 1000)], 'r-')
    plt.title('Interest Rate Model (0.7 to 1)- grey is semilog as reference')
    plt.xlabel('Utilization')
    plt.ylabel('Interest Rate')
    plt.xlim(0.7, 1)


    # Set y-axis limit dynamically
    max_rate = max(rates)
    if np.isfinite(max_rate):
        plt.ylim(0, max_rate * 1.1)  # Set y-axis limit to 110% of max rate
    else:
        plt.ylim(0, 1)  # Set a default limit if max_rate is infinite

    # Format axes as percentages
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y:.2%}'))

    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)

    counter = 0
    for u, r in zip(utilization, rates):
        if u >= 0.7:
            if counter % 20 == 0:
                plt.plot(u, r, 'x', markersize=8)
                plt.text(u, r, f'{r:.1%}, u: {u:.1%}', fontsize=8, ha='center', va='bottom')
            counter += 1


    plt.text(0.5, -0.1, f'A: {p["A"]}, shift: {p["shift"]}, r_minf: {p["r_minf"]}, u_inf: {p["u_inf"]}, r0: {r0}', ha='center', va='center', transform=plt.gca().transAxes)  # Adjust the y-coordinate as needed

    plot_semilog_rate(0.005, max_rate, '--', c='gray')

    # Save the plot as a PNG file
    plt.savefig(f'data/{timestamp}_{c}_interest_rate_model_zoom_A:{p["A"]}_shift:{p["shift"]}_r_minf:{p["r_minf"]}_u_inf:{p["u_inf"]}_r0:{r0}.png', dpi=300, bbox_inches='tight')


    # plt.show()
    plt.close()



if __name__ == '__main__':
    pass