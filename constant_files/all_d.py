'''
Always defect -- most suboptimal play.
'''
def allD(agent, action):
    # always defect
    return agent.defect()
defaultPerformAction = allD
