'''
This lets you specify an experiment to run. You must provide it with:
    - an experiment name
    - the number of iterations to run for
    - the constants file to use
    - the statistics to write out
Each one of these may be a list. If you want to use the same statistics
or number of iterations, then they will be duplicated over and over
for each experimental run.
'''
import os
import sys
import shutil
import cPickle
from numpy import mean
import numpy as np
import pdb, sys
########################################################################
##########CONFIGURATION OPTIONS#########################################
########################################################################
# experiment_list is a list of experiments to perform. It must be a
# list.
pre_experiment_list = ['baseline','always_play','no_world',
                   'only_CD','only_CD_always_play',
                   'symmetric_payoff','long_genes',
                   'traitor_superpayoff','nonnegative_payoff',
                   'bigsim']
experiment_list = [x + '_1' for x in pre_experiment_list]
experiment_list += [x + '_2' for x in pre_experiment_list]
experiment_list += [x + '_3' for x in pre_experiment_list]
# iteration_list is a list of the number of iterations to run for each
# experiment.
iteration_list = [400,400,400,400,400,400,600,400,400,400]*3
# constants_list is a list of files containing constants.
constants_list = ['baseline','always_play','high_permeability',
                  'onlyCD','always_play_onlyCD',
                  'symmetric_payoff','long_genes','traitor_megapayoff',
                  'nonnegative_payoff','bigsim']*3
# statistics_list is a list of all the statistics to write out each
# iteration. It must be a list, but may also be a list of lists.
statistics_list = ['mean_fitness', 'die_offs','num_agents','fitness',
                   'vengeful','sucker','collaborator','cruel',
                   'selective','traitor','retreating','popular',
                   'forgiving','prisoner','timid','nice','tot_games',
                   'per_game_fitness','mean_per_game_fitness',
                   'tot_games_played']
save_the_world = [True, False, False, False, False, False, True,
                  False, False, False] * 3
save_tile_stats = True
########################################################################
##########CONSTANT PARAMETERS###########################################
########################################################################
# DO NOT CHANGE THESE
home = os.getenv("HOME")
subdirs = ''
root = os.path.join(home, subdirs, 'evolution/experiments')
constant_dir = os.path.join(home, subdirs, 'evolution/constant_files') # the directory that contains all the constants
abs_root = os.path.join(home, subdirs, 'evolution/')
########################################################################
########################################################################
########################################################################
# elaborate the stuff into a list
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

mkdir(root)

if not type(iteration_list) == list:
    iteration_list = [iteration_list]
if not type(constants_list) == list:
    constants_list = [constants_list]
if not type(statistics_list[0]) == list:
    statistics_list = [statistics_list]
if not type(save_the_world) == list:
    save_the_world = [save_the_world]
if not type(save_tile_stats) == list:
    save_tile_stats = [save_tile_stats]

if not len(experiment_list) == len(iteration_list):
    iteration_list *= len(experiment_list)
if not len(experiment_list) == len(constants_list):
    iteration_list *= len(experiment_list)
if not len(experiment_list) == len(statistics_list):
    statistics_list *= len(experiment_list)
if not len(experiment_list) == len(save_the_world):
    save_the_world *= len(experiment_list)
if not len(experiment_list) == len(save_tile_stats):
    save_tile_stats *= len(experiment_list)

experiments = zip(experiment_list, iteration_list, constants_list, statistics_list)

def cleanModules():
    # removes all the goddamn modules from pythons goddamn namespace
    # WHY IS THIS SO HARD TO DO!?
    modules = ['agent','constants','gameMaster','genome',
               'tile','trust','world','constants_override']
    for m in modules:
        if m in sys.modules:
            del(sys.modules[m])

for exp, iters, const, stats in experiments:
    # create a directory for the files to go in
    cleanModules()
    # this is the best way to do the constant file reloading. i know,
    # it's ridiculous, but whatever.
    constant_file = os.path.join(constant_dir, const + '.py')
    target_constant_file = os.path.join(abs_root, 'constants_override.py')
    shutil.copy(constant_file, target_constant_file)
    exp_root = os.path.join(root, exp)
    exp_iter_root = os.path.join(exp_root, 'iterations')
    mkdir(exp_root)
    mkdir(exp_iter_root)
    # write out some parameters
    f = open(os.path.join(exp_root, 'experiment_params'),'w')
    f.write('Constants file: %s\n'%const)
    f.write('Statistics: %s\n'%str(stats))
    f.write('Iterations: %s\n'%str(iters))
    module = __import__('constants_override', globals(), locals(), ['*'])
    for k in dir(module):
        if not hasattr(getattr(module, k), '__call__') and '__' not in k:
            f.write('%s : %s\n'%(k, str(getattr(module, k))))
    f.close()
    import world
    w = world.World()
    for i in range(iters-1):
        w.iterate()
    w.iterate(regen_children=False)
    for stat in stats:
        if stat == 'mean_fitness':
            fname = os.path.join(exp_root, stat)
            np.save(fname, w.mean_fitness)
        elif stat == 'mean_trust':
            fname = os.path.join(exp_root, stat)
            np.save(fname, w.mean_trust)
        elif stat == 'die_offs':
            fname = os.path.join(exp_root, stat)
            np.save(fname, w.die_offs)
        elif stat == 'mean_per_game_fitness':
            fname = os.path.join(exp_root, stat)
            np.save(fname, w.mean_per_game_fitness)
        elif stat == 'tot_games_played':
            fname = os.path.join(exp_root, stat)
            np.save(fname, w.tot_games_played)
        else:
            if save_tile_stats:
                fname = os.path.join(exp_iter_root,stat)
                np.save(fname, w.statistics[stat])
            if stat in w.global_statistics:
                fname = os.path.join(exp_root, 'global_'+stat)
                np.save(fname, w.global_statistics[stat])
    f = open(os.path.join(exp_root, 'lineages'),'w')
    for x in w.agents:
        f.write('%s\n'%x.parents)
    f.close()
    if save_the_world:
        # finally, pickle the world
        world_dest = os.path.join(exp_root, 'world.pkl')
        f = open(world_dest,'w')
        cPickle.dump(w, f)
        f.close()




















