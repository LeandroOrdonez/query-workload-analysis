import prettyplotlib as ppl
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib as mpl
from prettyplotlib import brewer2mpl
from prettyplotlib.colors import set1 as cs
from prettyplotlib.colors import set2 as pcs
from matplotlib.ticker import FuncFormatter


def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    return str(int(100 * y))

    # The percent symbol needs escaping in latex
    if mpl.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'


formatter = FuncFormatter(to_percent)


def read_csv(headers, sdss):
    if sdss:
        return read_data(headers, 'sdss')
    else:
        return read_data(headers, 'sqlshare')


def read_data(headers, source):
    with open('../results/' + source + '/' + '_'.join(headers) + '.csv') as f:
        return np.recfromcsv(f)


def query_length_cdf():
    fig, ax = plt.subplots(1)

    data = read_csv(['lengths', 'counts'], True)
    c = data['counts'].astype(float)
    c /= sum(c)
    ppl.plot(ax, data['lengths'], np.cumsum(c), label="SDSS", color=cs[0], linewidth=2, ls='-.')

    data = read_csv(['lengths'], False)
    data.sort(order='length')
    c = data['count'].astype(float)
    c /= sum(c)
    ppl.plot(ax, data['length'], np.cumsum(c), label="SQLShare", color=cs[1], linewidth=2, ls='--')

    data = read_data(['lengths', 'counts'], 'tpch')
    data.sort(order='lengths')
    c = data['counts'].astype(float)
    c /= sum(c)
    ppl.plot(ax, data['lengths'], np.cumsum(c), label="TPC-H", color=cs[2], linewidth=2, ls=':')

    ppl.legend(ax, loc='lower right')

    plt.gca().yaxis.set_major_formatter(formatter)

    ax.set_xlabel('Query length in characters')
    ax.set_ylabel('% of queries')

    ax.set_ylim(0, 1.01)
    ax.set_xlim(0, 2000)

    ax.yaxis.grid()

    plt.show()

    fig.savefig('plot_lengths.pdf', format='pdf', transparent=True)
    fig.savefig('plot_lengths.png', format='png', transparent=True)


def runtime_cdf():
    fig, [ax1, ax2] = plt.subplots(1, 2, sharey=True, figsize=(8, 4))

    data = read_csv(['actual', 'counts'], True)
    c = data['counts'].astype(float)
    c /= sum(c)
    ppl.plot(ax1, data['actual'], np.cumsum(c), label="SDSS", color=cs[0], linewidth=2, ls='-.')

    data = read_csv(['time_taken'], False)
    data.sort(order='time_taken')
    c = data['count'].astype(float)
    c /= 1000  # ms to seconds
    c /= sum(c)
    ppl.plot(ax2, data['time_taken'], np.cumsum(c), label="SQLShare", color=cs[1], linewidth=2, ls='--')

    ppl.legend(ax1, loc='lower right')
    ppl.legend(ax2, loc='lower right')

    plt.gca().yaxis.set_major_formatter(formatter)

    #ax.set_xlabel('Runtime in seconds')
    ax1.set_ylabel('% of queries')
    fig.text(0.5, 0.02, "Runtime in seconds", ha='center')

    ax1.yaxis.grid()
    ax2.yaxis.grid()

    fig.subplots_adjust(wspace=0.1)

    ax1.set_xlim(0, 6)
    ax2.set_xlim(0, 500)

    ax1.set_ylim(0, 1.01)
    ax2.set_ylim(0, 1.01)

    fig.tight_layout(rect=[0, .03, 1, 1])

    plt.show()

    fig.savefig('plot_runtimes_cdf.pdf', format='pdf', transparent=True)
    fig.savefig('plot_runtimes_cdf.png', format='png', transparent=True)


def table_touch(dataset = True):
    fig, ax = plt.subplots(1)

    ax.set_yscale('log')

    data = read_csv(['touch', 'counts'], True)
    #ppl.bar(ax, range(len(data['touch'])), data['counts'], xticklabels=data['touch'], grid='y', log=True)
    ppl.scatter(ax, data['touch'], data['counts'], label="SDSS", marker="o", s=100)

    if dataset:
        data = read_csv(['dataset_touch'], False)
        ppl.scatter(ax, data['dataset_touch'], data['count'], label="SQLShare (Dataset)", marker="v", s=100, color=pcs[0])
    else:
        data = read_csv(['touch'], False)
        ppl.scatter(ax, data['touch'], data['count'], label="SQLShare", marker="v", s=100, color=pcs[1])

    ax.set_xlabel('Table touch')
    ax.set_ylabel('# of queries')

    ppl.legend(ax)

    ax.set_ylim(0)

    plt.show()

    if dataset:
        fig.savefig('plot_touch_dataset.pdf', format='pdf', transparent=True)
        fig.savefig('plot_touch_dataset.png', format='png', transparent=True)
    else:
        fig.savefig('plot_touch.pdf', format='pdf', transparent=True)
        fig.savefig('plot_touch.png', format='png', transparent=True)



def dataset_touch():
    fig, ax = plt.subplots(1)

    data = read_csv(['dataset_touch'], False)
    ppl.bar(ax, range(len(data['dataset_touch'])), data['count'], xticklabels=data['dataset_touch'], grid='y', log=True)

    plt.xlabel('Dataset touch')
    plt.ylabel('# of queries')

    plt.show()

    fig.savefig('plot_datasettouch_sqlshare.pdf', format='pdf', transparent=True)
    fig.savefig('plot_datasettouch_sqlshare.png', format='png', transparent=True)


def table_touch_cdf():
    fig, [ax2, ax1] = plt.subplots(1, 2, sharey=True, figsize=(8, 4))

    data = read_csv(['touch'], False)
    data.sort(order='touch')
    c = data['count'].astype(float)
    c /= sum(c)
    ppl.plot(ax1, data['touch'], np.cumsum(c), label="SQLShare", color=cs[0], linewidth=2, linestyle='-.')

    data = read_csv(['touch', 'counts'], True)
    c = data['counts'].astype(float)
    c /= sum(c)
    ppl.plot(ax2, data['touch'], np.cumsum(c), label="SDSS", color=cs[1], linewidth=2, linestyle='--')

    ppl.legend(ax1, loc='lower right')
    ppl.legend(ax2, loc='lower right')

    ax1.yaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)

    ax1.set_xlim(0, 500)
    ax1.set_xlim(0, 25)

    ax1.yaxis.grid()
    ax2.yaxis.grid()

    #ax1.set_xlabel('Table touch')
    fig.text(0.5, 0.02, "Table touch", ha='center')
    ax1.set_ylabel('% of queries')

    fig.subplots_adjust(wspace=0.1)

    ax1.set_ylim(0, 1.01)
    ax2.set_ylim(0, 1.01)

    fig.tight_layout(rect=[0, .03, 1, 1])

    plt.show()

    fig.savefig('plot_touch_cdf.pdf', format='pdf', transparent=True)
    fig.savefig('plot_touch_cdf.png', format='png', transparent=True)


def physical_ops():
    fig, ax = plt.subplots(1, figsize=(8, 4))

    data = read_csv(['physical_op', 'count'], True)
    data.sort(order='count')
    #data = data[-14:]

    c = data['count'].astype(float)
    c /= sum(c)
    c *= 100
    ypos = np.arange(len(data['physical_op']))
    ppl.barh(ax, ypos, c, yticklabels=data['physical_op'], grid='x', annotate=True)

    #ax.set_ylabel('Physical operator')
    ax.set_xlabel('% of queries')

    #plt.subplots_adjust(bottom=.2, left=.3, right=.99, top=.9, hspace=.35)

    fig.tight_layout(rect=[0.03, 0, 1, 1])
    fig.text(0.02, 0.55, 'Physical operator', rotation=90, va='center')

    plt.show()

    fig.savefig('plot_physops_sdss.pdf', format='pdf', transparent=True)
    fig.savefig('plot_physops_sdss.png', format='png', transparent=True)

def physical_ops_sqlshare():
    fig, ax = plt.subplots(1, figsize=(8, 4))

    data = read_csv(['physical_ops', 'count'], False)
    data.sort(order='count')
    #data = data[-14:]

    c = data['count'].astype(float)
    c /= sum(c)
    c *= 100
    ypos = np.arange(len(data['physical_op']))
    ppl.barh(ax, ypos, c, yticklabels=data['physical_op'], grid='x', annotate=True)

    #ax.set_ylabel('Physical operator')
    ax.set_xlabel('% of queries')

    #plt.subplots_adjust(bottom=.2, left=.3, right=.99, top=.9, hspace=.35)

    fig.tight_layout(rect=[0.03, 0, 1, 1])
    fig.text(0.02, 0.55, 'Physical operator', rotation=90, va='center')

    plt.show()

    fig.savefig('plot_physops_sqlshare.pdf', format='pdf', transparent=True)
    fig.savefig('plot_physops_sqlshare.png', format='png', transparent=True)

def logical_ops_sdss():
    fig, ax = plt.subplots(1, figsize=(8, 4))

    data = read_csv(['logical_op', 'count'], True)
    data.sort(order='count')
    #data = data[-14:]

    c = data['count'].astype(float)
    c /= sum(c)
    c *= 100
    ypos = np.arange(len(data['logical_op']))
    ppl.barh(ax, ypos, c, yticklabels=data['logical_op'], grid='x', annotate=True)

    #ax.set_ylabel('Physical operator')
    ax.set_xlabel('% of queries')

    #plt.subplots_adjust(bottom=.2, left=.3, right=.99, top=.9, hspace=.35)

    fig.tight_layout(rect=[0.03, 0, 1, 1])
    fig.text(0.02, 0.55, 'Logical operator', rotation=90, va='center')

    plt.show()

    fig.savefig('plot_logops_sdss.pdf', format='pdf', transparent=True)
    fig.savefig('plot_logops_sdss.png', format='png', transparent=True)


def logical_ops_sqlshare():
    fig, ax = plt.subplots(1, figsize=(8, 5))

    data = read_csv(['logical_ops', 'count'], False)
    data.sort(order='count')
    #data = data[-14:]

    c = data['count'].astype(float)
    c /= sum(c)
    c *= 100
    ypos = np.arange(len(data['logical_op']))
    ppl.barh(ax, ypos, c, yticklabels=data['logical_op'], grid='x', annotate=True)

    #ax.set_ylabel('Physical operator')
    ax.set_xlabel('% of queries')

    #plt.subplots_adjust(bottom=.2, left=.3, right=.99, top=.9, hspace=.35)

    fig.tight_layout(rect=[0.03, 0, 1, 1])
    fig.text(0.02, 0.55, 'Logical operator', rotation=90, va='center')

    plt.show()

    fig.savefig('plot_logops_sqlshare.pdf', format='pdf', transparent=True)
    fig.savefig('plot_logops_sqlshare.png', format='png', transparent=True)


def opcounts():
    fig, ax = plt.subplots(1, figsize=(8, 4))

    ax.set_yscale('log')

    data = read_csv(['physops', 'counts'], True)
    #ppl.bar(ax, data['ops'], data['counts'], grid='y', log=True)
    y, x = np.array(np.histogram(data['physops'], 10, weights=data['counts']))
    w = x[1] - x[0]
    x += w/2
    data = [a for a in zip(list(x), list(y)) if a[1]]
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    ppl.scatter(ax, x=x, y=y,  marker="o", color=pcs[0], s=100, label="SDSS")

    data = read_csv(['ops'], False)
    d = data['ops']
    y, x = np.histogram(d, bins=np.linspace(min(d), max(d), (max(d) - min(d)) / w), weights=data['count'])
    x += w/2
    data = [a for a in zip(list(x), list(y)) if a[1]]
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    ppl.scatter(ax, x=x, y=y, marker="v", color=pcs[1], s=100, label="SQLShare")

    ax.set_xlabel('Physical operators used')
    ax.set_ylabel('# of queries')

    ppl.legend(ax, loc='lower right')

    ax.set_xlim(0)
    ax.set_ylim(0)

    fig.tight_layout()
    plt.show()

    fig.savefig('plot_logops_query.pdf', format='pdf', transparent=True)
    fig.savefig('plot_logops_query.png', format='png', transparent=True)


def distopcounts():
    fig, ax = plt.subplots(1, figsize=(8, 4))

    ax.set_yscale('log')

    data = read_csv(['distinct_ops', 'counts'], True)

    #ppl.bar(ax, data['ops'], data['counts'], grid='y', log=True)
    ppl.scatter(ax, data['distinct_ops'], data['counts'], color=pcs[0], marker="o", label="SDSS", s=100)

    data = read_csv(['distinct_physical_ops'], False)
    ppl.scatter(ax, data['distinct_physical_ops'], data['count'], color=pcs[1], marker="v", label="SQLShare", s=100)

    ax.set_xlabel('Distinct physical operators used')
    ax.set_ylabel('# of queries')

    ppl.legend(ax, loc='lower right')

    ax.set_xlim(0)
    ax.set_ylim(0)

    fig.tight_layout()
    plt.show()

    fig.savefig('plot_dist_physops_query.pdf', format='pdf', transparent=True)
    fig.savefig('plot_dist_physops_query.png', format='png', transparent=True)


def new_tables_cdf():
    fig, ax = plt.subplots(1)

    data = read_csv(['query_number', 'num_new_tables'], True)
    c = data['num_new_tables'].astype(float)
    c /= sum(c)
    q = data['query_number'].astype(float)
    q /= q[-1]
    ppl.plot(ax, q, np.cumsum(c), label="SDSS", color=cs[0], linewidth=2, ls='-.', drawstyle='steps-post')
    ppl.scatter(ax, q, np.cumsum(c), color=cs[0], marker="o", s=100)

    data = read_csv(['table_coverage'], False)
    c = data['tables'].astype(float)
    c /= c[-1]
    q = data['query_id'].astype(float)
    q /= q[-1]
    ppl.plot(ax, q, c, label="SQLShare", color=cs[1], linewidth=2, ls='-.', drawstyle='steps-post')
    ppl.scatter(ax, q, c, color=cs[1], marker="o", s=100)

    ppl.legend(ax, loc='lower right')

    plt.gca().yaxis.set_major_formatter(formatter)

    ax.set_xlabel('Query number')
    ax.set_ylabel('% of newly used table')

    ax.set_ylim(0, 1.01)
    ax.set_xlim(0, 1)

    ax.yaxis.grid()

    plt.show()

    fig.savefig('num_new_tables.pdf', format='pdf', transparent=True)
    fig.savefig('num_new_tables.png', format='png', transparent=True)

if __name__ == '__main__':
    plt.rc('font', family='serif')

    # query_length_cdf()
    # table_touch()
    # table_touch(dataset=False)
    # table_touch_cdf()
    # physical_ops()
    # physical_ops_sqlshare()
    # logical_ops_sdss()
    # logical_ops_sqlshare()
    # runtime_cdf()
    # opcounts()
    # distopcounts()
    # new_tables_cdf()
    # new_tables_cdf_sqlshare()
