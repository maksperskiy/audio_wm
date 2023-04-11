import random
import math
from matplotlib import pyplot as plt 

class ParamsOptimizer:
    x1 = 0
    x2 = 0
    x3 = 0
    class_list = ["music", "speach", "silence"]
    class_params = {el: {"freq_b": [0,], "freq_t": [0,], "dur": [0,], "reward": 0, "freq_b_grad": 0, "freq_t_grad": 0, "dur_grad": 0, "freq_b_step": 512, "freq_t_step": 512, "dur_step": 10, "direction": 1, "param_n": 0} for el in class_list} 


    def make_step(self, sound_type, new_reward):
        params = self.class_params[sound_type]

        if not params["reward"]:
            params["reward"] = new_reward
            params["freq_b"].append(params["freq_b"][-1] + params["freq_b_step"])
            return

            
        if params["param_n"] % 3 == 0:
            params["freq_b_grad"] = -(new_reward - params["reward"])
            params["freq_b"].pop()
            params["freq_t"].append(params["freq_t"][-1] + params["freq_t_step"])
        elif params["param_n"] % 3 == 1:
            params["freq_t_grad"] = -(new_reward - params["reward"])
            params["freq_t"].pop()
            params["dur"].append(params["dur"][-1] + params["dur_step"])
        elif params["param_n"] % 3 == 2:
            params["dur_grad"] = -(new_reward - params["reward"])
            params["dur"].pop()

            params["freq_b"].append(params["freq_b"][-1] + params["freq_b_grad"] * params["freq_b_step"])
            params["freq_t"].append(params["freq_t"][-1] + params["freq_t_grad"] * params["freq_t_step"])
            params["dur"].append(params["dur"][-1] + params["dur_grad"] * params["dur_step"])
            
            print(params["freq_b"], params["freq_t"], params["dur"])
            params["freq_b_step"] /= 2
            params["freq_t_step"] /= 2
            params["dur_step"] /= 2

            params["reward"] = 0

        params["param_n"] = params["param_n"] + 1
    

        
        # grad = -(new_reward - params["reward"][-1])
        # params["reward"].append(new_reward)

        # grad_sign = 1 if grad > 0 else -1
        # if grad_sign == -1:
        #     params["direction"] = -params["direction"]
        #     if params["param_n"] % 3 == 0:
        #         params["freq_b_step"] /= 2
        #     if params["param_n"] % 3 == 1:
        #         params["freq_t_step"] /= 2
        #     if params["param_n"] % 3 == 2:
        #         params["dur_step"] /= 2
        
        # if params["param_n"] % 3 == 2:
        #     params["freq_b"].append(params["freq_b"][-1] + params["freq_b_step"])
        # elif params["param_n"] % 3 == 0:
        #     params["freq_t"].append(params["freq_t"][-1] + params["freq_t_step"])
        # elif params["param_n"] % 3 == 1:
        #     params["dur"].append(params["dur"][-1] + params["dur_step"])

    def analyze(self, sound_type, reward=None):
        params = self.class_params[sound_type]
        reward = reward or math.sqrt((params["freq_b"][-1]-self.x1)**2+(params["freq_t"][-1]-self.x2)**2+(params["dur"][-1]-self.x3)**2)
        print(reward)
        self.make_step(sound_type, reward)
        return reward
  

  

if __name__ == "__main__":
    
    result = {}
    optimizer = ParamsOptimizer()
    optimizer.x1 = 4000
    optimizer.x2 = 17000
    optimizer.x3 = 120
    for i in range(212):
        optimizer.analyze("music")
        if i % 9 == 2:
            # optimizer.class_params["music"]["param_n"] = optimizer.class_params["music"]["param_n"] + 1
            optimizer.x1 = 4000 + random.random()*500
            optimizer.x2 = 17000 + random.random()*1000
            optimizer.x3 = 120 + random.random()*10
        if i % 27 == 2:
            optimizer.class_params["music"]["freq_b_step"] = 512
            optimizer.class_params["music"]["freq_t_step"] = 512
            optimizer.class_params["music"]["dur_step"] = 10

    def draw(x1_hist, x2_hist, x3_hist, x1, x2, x3):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot3D(x1_hist, x2_hist, x3_hist, 'b')
        ax.set_xlabel('freq_b')
        ax.set_ylabel('freq_t')
        ax.set_zlabel('duration')
        
        ax.scatter(x1, x2, x3, c='red')
        return plt.show()

    draw(optimizer.class_params["music"]["freq_b"][:64], optimizer.class_params["music"]["freq_t"][:64], optimizer.class_params["music"]["dur"][:64], optimizer.x1, optimizer.x2, optimizer.x3)