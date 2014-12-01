'''
Always plays, only able to cooperate or defect
'''
ALWAYS_PLAY = True
def onlyCD(agent, action):
    if not action:
        return agent.cooperate()
    else:
        return agent.defect()
defaultPerformAction = onlyCD
N_POS_ACTIONS = 2
