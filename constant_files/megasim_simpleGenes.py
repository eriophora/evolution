'''
50x50 board with 50,000 agents -- agents can only defect or cooperate, and must always play. In addition, these agents have extremely simple genes.
'''
N_COLS = 50
N_ROWS = 50
NUM_AGENTS = 50000
def onlyCD(agent, action):
    if not action:
        return agent.cooperate()
    else:
        return agent.defect()
defaultPerformAction = onlyCD
N_POS_ACTIONS = 2
GENE_LENGTH = 1
HISTORY_LENGTH = GENE_LENGTH
ALWAYS_PLAY = True


