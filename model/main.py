from Rule.apriori import *
from graphclustering.graphdraw import *

root = tk.Tk()
app = fil_and_opt(root)
root.mainloop()

csv_file = 'data/out/association_rules.csv'
data = pd.read_csv(csv_file, encoding="gbk")

df_G = make_G(data)

make_graph(df_G)