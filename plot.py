import json
import sexpdata as sexp
import matplotlib.pyplot as plt

current_plotted = []

def get_dataset(filepath):

    fp = open(filepath, "r")
    # fp = open("scored-disc.json","r")
    all_patterns = json.load(fp)

    cost_accuracies = [{"benchmark": x['name'], "best": x['output'], "data": sexp.loads(x['cost-accuracy'])} for x in all_patterns['tests']]
    cost_accuracies_per_benchmark = []
    for benchmark in cost_accuracies:
        # print(benchmark)
        c_a = []
        best = benchmark['data'][1]
        c_a.append({"cost": best[0], "error": best[1], "expr": benchmark["best"]})
        rest = benchmark['data'][2]
        # print(rest)
        c_a += ([{"cost": x[0], "error": x[1], "expr": sexp.dumps(x[2])} for x in rest])
        cost_accuracies_per_benchmark.append({"benchmark": benchmark["benchmark"], "data": c_a})
    
    print(cost_accuracies_per_benchmark)

    current_benchmark = "quad2p (problem 3.2.1, positive)"
    current_plotted = next(b for b in cost_accuracies_per_benchmark if b["benchmark"] == current_benchmark)["data"]
    xs = [x["cost"] for x in current_plotted]
    ys = [y["error"] for y in current_plotted]

    return (xs, ys, current_plotted)

xs, ys, first_plotted = get_dataset("sample.json")
xs2, ys2, second_plotted = get_dataset("sample2.json")
#TODO: fix multiple scatters with tooltip 
area = 5


fig,ax = plt.subplots()
sc = plt.scatter(xs, ys, s=area, alpha=0.5)

sc2 = plt.scatter(xs2, ys2, s=area, alpha=0.5, marker="*", color="red")


annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind, scatter, points):
    pos = scatter.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    # print(ind)
    # ind is all indices under that point
    # print(cost_accuracies_per_benchmark[ind["ind"][0]])
    first = points[ind["ind"][0]]["expr"]
    text = f"{first}"
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont :
            update_annot(ind, sc, first_plotted)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            cont2, ind2 = sc2.contains(event)
            if cont2:
                update_annot(ind2, sc2, second_plotted)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
