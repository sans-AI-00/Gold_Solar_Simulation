from matplotlib import pyplot as plt


def hist_plot(data, ylabel, title, color, ec):
    adapted_data = []

    for j in range(len(data)):
        for i in range(int(data[j])):
            adapted_data.append(j)

    bins = [i for i in range(13)]
    fig, ax = plt.subplots(1, 1)
    ax.hist(adapted_data, bins, color=color, ec=ec)
    ax.set_title(title)
    ax.set_xlabel('Mese')
    ax.set_ylabel(ylabel)
    plt.close()

    return fig


if __name__ == '__main__':
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    fig = hist_plot(data, 'ylabel', 'title', color='green', ec='black')
    fig.savefig('fig.png')

