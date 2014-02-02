# Analysis script
import numpy as np
# filter for cases in which superdesign has fewer nodes than subdesign:

t = np.array(times)
sbn = np.array(subnodes)
spn = np.array(supernodes)

filtered_t = t[np.where(sbn<spn)]
filtered_sbn = sbn[np.where(sbn<spn)]
filtered_spn = spn[np.where(sbn<spn)]

# Generate mean, lower, and upper bound by number of nodes.
num_nodes = []
lowers = []
uppers = []
means = []
for i in xrange(60):
    indices = np.where(filtered_sbn==i)
    tt = filtered_t[indices]
    if len(tt)==0:
        continue
    num_nodes.append(i)
    lowers.append(np.min(tt))
    uppers.append(np.max(tt))
    means.append(np.average(tt))




