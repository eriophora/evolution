'''
2x2 board with 150 agents and a low transition likelihood with no
quitting.
'''
N_COLS = 2
N_ROWS = 2
NUM_AGENTS = 150
def transProbFcn():
    return 0.1
def onlyCD(agent, action):
    if not action:
        return agent.cooperate()
    else:
        return agent.defect()
defaultPerformAction = onlyCD
