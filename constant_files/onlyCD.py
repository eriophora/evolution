'''
Agents may either cooperate or defect -- there is no option to quit a
game.
'''
def onlyCD(agent, action):
    if not action:
        return agent.cooperate()
    else:
        return agent.defect()
defaultPerformAction = onlyCD
