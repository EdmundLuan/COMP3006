import numpy as np
from pyglet.window import key

# individual agent policy
class Policy(object):
    def __init__(self):
        pass
    def action(self, obs):
        raise NotImplementedError()

# interactive policy based on keyboard input
# hard-coded to deal only with movement, not communication
class InteractivePolicy(Policy):
    def __init__(self, env, agent_index):
        super(InteractivePolicy, self).__init__()
        self.env = env
        # hard-coded keyboard events
        self.move = [False for i in range(4)]
        # register keyboard events with this environment's window
        env.viewers[agent_index].window.on_key_press = self.key_press
        env.viewers[agent_index].window.on_key_release = self.key_release

    def action(self, obs):
        # observation see "simple_tag.py: line 100" 
        if self.env.discrete_action_input:
            u = 0
            if self.move[0]: u = 1
            if self.move[1]: u = 2
            if self.move[2]: u = 4
            if self.move[3]: u = 3
        else:
            # 本项目中使用非离散 请修改以下代码
            # u[] 1: right; 2: left; 3: up; 4: down; 5: stay?
            u = np.zeros(5) # 5-d because of no-move action
            # if self.move[0]: u[1] += 1.0
            # if self.move[1]: u[2] += 1.0
            # if self.move[3]: u[3] += 1.0
            # if self.move[2]: u[4] += 1.0

            # My test policy
            # 坐标连线朝远处跑，但敌不动我不加速(方便观察调试，别跑出界了) 
            dist = np.sqrt(obs[2]**2 + obs[3]**2)
            if obs[8]:
                # 追方
                u[1] = obs[2] / dist / 1.3 #  unit acceleration
                u[3] = obs[3] / dist / 1.3
                # # 追方由键盘控制
                # if self.move[0]: u[1] += 1.0
                # if self.move[1]: u[2] += 1.0
                # if self.move[3]: u[3] += 1.0
                # if self.move[2]: u[4] += 1.0
            else: 
                if obs[6]!=0:
                    u[1] = -obs[2] / dist / 1 # unit acceleration
                else: 
                    u[1] = 0
                if obs[7]!=0:
                    u[3] = -obs[3] / dist / 1
                else:
                    u[3] = 0
                # print('obs4', obs[1])
                # print('what is self', )
            # no movement 
            if True not in self.move:
                u[0] += 1.0
        return u

    # keyboard event callbacks
    # move[] 0: right; 1: left; 2: down; 3: up
    def key_press(self, k, mod):
        if k==key.RIGHT:  self.move[0] = True
        if k==key.LEFT: self.move[1] = True
        if k==key.DOWN:    self.move[2] = True
        if k==key.UP:  self.move[3] = True
    def key_release(self, k, mod):
        if k==key.RIGHT:  self.move[0] = False
        if k==key.LEFT: self.move[1] = False
        if k==key.DOWN:    self.move[2] = False
        if k==key.UP:  self.move[3] = False
