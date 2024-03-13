import os
from datetime import datetime

time = datetime.now().strftime("%d-%m-%Y")
os.popen(f'scp sih18pev@linda.rhrk.uni-kl.de:/home/sih18pev/pythonproj/botv3/user_activities.db ./user_activities_{time}.db').read()