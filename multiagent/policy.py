import numpy as np
import scipy.optimize as opt
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
            
            if obs[8]:
                # Pursuer 
                # a_p = 2//t (v_e-v_p0) + 2//t^2 p_e 
                # Let t = 1. 
                # x = 2 * (obs[6] - obs[4] + obs[2])
                # y = 2 * (obs[7] - obs[5] + obs[3])
                x = obs[2]
                y = obs[3]
                # # print('v_px:', x)
                # # print('v_py:', y)
                norm = np.sqrt(x**2+y**2)
                u[1] = x/norm  #  unit acceleration, normalization 
                u[3] = y/norm

                # # 追方由键盘控制
                # if self.move[0]: u[1] += 1.0
                # if self.move[1]: u[2] += 1.0
                # if self.move[3]: u[3] += 1.0
                # if self.move[2]: u[4] += 1.0
            else: 
                # Evader 
                # 先猜一个追方的下一时刻位置，然后尽量远离那个地点，转化为一个优化问题
                # r = lambda x: x[0]**2 + x[1]**2 
                # con = opt.NonlinearConstraint(r, 0, 1) 
                # t = 1
                # ra = lambda x: ((obs[4]-obs[6])*t+0.5*x[0]*t**2+obs[2])**2 + ((obs[5]-obs[7])*t+0.5*x[1]*t**2+obs[3])**2 
                # x0 = [0, 0]
                # optRes = opt.minimize(ra, x0, constraints=[con],tol=1e-3)
                # x = optRes.x[0]
                # y = optRes.x[1]
                dist = np.sqrt(obs[2]**2 + obs[3]**2)
                if dist<2.2:
                    x = -obs[3]
                    y = obs[2]
                else:
                    x = -obs[2]
                    y = -obs[3]
                # x = obs[3]
                # y = -obs[2]
                dist = np.sqrt(x**2 + y**2)
                u[1] = x / dist # unit acceleration 
                u[3] = y / dist 
                # print('obs4', obs[1])

                # 逃方由键盘控制
                # if self.move[0]: u[1] += 1.0
                # if self.move[1]: u[2] += 1.0
                # if self.move[3]: u[3] += 1.0
                # if self.move[2]: u[4] += 1.0
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
