# plotting all the various statistics
from glob import glob
import numpy as np
import os
from StringIO import StringIO
# plot all of a
dirs = glob('*')
dirs.remove('old')
params = list(set([x.split('/')[-1] for x in glob(os.path.join('*', 'global_*'))])) + ['die_offs','mean_per_game_fitness','tot_games_played']
stats_d = dict()
stats_p = dict()
for i in dirs:
    stats_d[i] = dict()
for p in params:
    stats_p[p] = dict()
for p in params:
    for i in dirs:
        stats_d[i][p] = np.loadtxt(os.path.join(i,p))
        stats_p[p][i] = np.loadtxt(os.path.join(i,p))
'''
['global_traitor.npy',
 'global_retreating.npy',
 'global_nice.npy',
 'global_cruel.npy',
 'global_optimality.npy',
 'global_popular.npy',
 'global_selective.npy',
 'global_prisoner.npy',
 'global_quitter.npy',
 'global_cooperator.npy',
 'global_forgiving.npy',
 'global_timid.npy',
 'global_vengeful.npy',
 'global_collaborator.npy',
 'global_defector.npy',
 'global_sucker.npy',
 'die_offs',
 'mean_per_game_fitness',
 'tot_games_played']
 '''
s = 'only_CD_always_play_*'
p = 'global_optimality.npy'
close()
z = glob(os.path.join(s,p))
data = []
for i in z:
    data.append(np.load(i))
for i in data:
    plot(i)

j = np.array(stats_p['mean_per_game_fitness']['nd_baseline'])
j *= 1./np.max(j)
k1 = np.array(stats_p['global_cruel']['nd_baseline'])
k2 = np.array(stats_p['global_nice']['nd_baseline'])
k3 = np.array(stats_p['global_timid']['nd_baseline'])
h1 = np.array(stats_p['global_forgiving']['nd_baseline'])
h2 = np.array(stats_p['global_vengeful']['nd_baseline'])
h3 = np.array(stats_p['global_retreating']['nd_baseline'])
close()
plot(j, label = 'fitness')
#plot(k1, label = 'cruelty')
#plot(k2, label = 'nice')
#plot(k3, label = 'timid')
plot(h1, label = 'forgiving')
plot(h2, label = 'vengeful')
plot(h3, label = 'retreating')
legend()

close()
stat = 'global_retreating'
for i in stats_p[stat]:
    j = stats_p[stat][i]
    if len(j) > 100:
        plot(j[:350],label=i)
legend(loc='lower right')


# to read in by-tile data
plot_it = False
draw_it = True
bt_stats = list(set([x.split('_')[-1] for x in glob(os.path.join(dirs[0],'iterations','*'))]))
exp = 'nd_baseline'
stat = 'per_game_fitness'
files = glob(os.path.join(exp,'iterations','*_'+stat))
datas = []
for k in files:
    f = open(k,'r')
    d = f.read().replace(',\n','\n')
    f.close()
    datas.append(np.genfromtxt(StringIO(d),delimiter=','))
data = np.array(datas)
if stat == 'per_game_fitness':
    data *= 10 # due to an error
# to plot it out
close()
if plot_it:
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            plot(data[:350,i,j])
if draw_it:
    # normalize the data
    data *= 1./np.max(data)
    for i in range(data.shape[0]):
        imshow(data[i,:,:],interpolation='none',hold=False,cmap='jet')
        z=raw_input('%s, iteration %i'%(stat,i))
        if len(z):
            break


#y, x = np.mgrid[0:data.shape[1],0:data.shape[2]]
z = data[255,:,:]
imshow(z,interpolation='none',hold=False)
#pcolor(x,y,z)

z = data[1,:,:]
draw()

tg = w.statistics['tot_games'][-1][5][5]
tf = w.statistics['fitness'][-1][5][5] * w.statistics['num_agents'][-1][5][5]
