'''
2x2 board with 150 agents and a low transition likelihood with no
quitting.
'''
N_COLS = 3
N_ROWS = 3
NUM_AGENTS = 150
def transProbFcn():
    return 0.1
def onlyCD(agent, action):
    if not action:
        return agent.cooperate()
    else:
        return agent.defect()
defaultPerformAction = onlyCD
N_POS_ACTIONS = 2
