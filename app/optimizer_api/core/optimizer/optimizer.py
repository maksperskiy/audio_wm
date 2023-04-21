import math
import random

from matplotlib import pyplot as plt


class ParamsOptimizer:
    def __init__(self) -> None:
        params = {
            "freq_b": 1750,
            "freq_t": 8500,
            "dur": 20,
            "reward": 0,
            "freq_b_grad": None,
            "freq_t_grad": None,
            "dur_grad": None,
            "freq_b_step": 10000,
            "freq_t_step": 10000,
            "dur_step": 10000,
            "param_n": None,
        }
        base_params = {
            "freq_b": 1750,
            "freq_t": 8500,
            "dur": 20,
            "reward": None,
            "freq_b_grad": None,
            "freq_t_grad": None,
            "dur_grad": None,
            "freq_b_step": 10000,
            "freq_t_step": 10000,
            "dur_step": 10000,
            "param_n": None,
        }
        rate = 10000

        target = 1  # min -1 / max 1

    @staticmethod
    def __limit_value(value, min_value=0, max_value=20000):
        if value > max_value:
            return max_value
        elif value < min_value:
            return min_value
        return value

    def make_step(self, last_params, new_reward):
        params = last_params

        if not params["reward"]:
            params["reward"] = new_reward
            params["freq_b"].append(
                self.__limit_value(
                    params["freq_b"][-1] + params["freq_b_step"],
                    max_value=params["freq_t"][-1] + 1,
                )
            )
            return

        if params["param_n"] % 3 == 0:
            params["freq_b_grad"] = self.target * (new_reward - params["reward"])
            params["freq_b"].pop()
            params["freq_t"].append(
                self.__limit_value(
                    params["freq_t"][-1] + params["freq_t_step"],
                    min_value=params["freq_b"][-1] + 1,
                    max_value=20000,
                )
            )
        elif params["param_n"] % 3 == 1:
            params["freq_t_grad"] = self.target * (new_reward - params["reward"])
            params["freq_t"].pop()
            params["dur"].append(
                self.__limit_value(
                    params["dur"][-1] + params["dur_step"], min_value=10, max_value=975
                )
            )
        elif params["param_n"] % 3 == 2:
            params["dur_grad"] = self.target * (new_reward - params["reward"])
            params["dur"].pop()

            print("/________________________________________________________________/")
            print(
                "Step values: ",
                params["freq_b_step"],
                params["freq_t_step"],
                params["dur_step"],
            )
            print(
                "Grad: ",
                params["freq_b_grad"],
                params["freq_t_grad"],
                params["dur_grad"],
            )
            print("Target: ", self.x1, self.x2, self.x3)

            print(
                "Old params: ",
                params["freq_b"][-1],
                params["freq_t"][-1],
                params["dur"][-1],
            )
            print("reward: ", params["reward"])
            params["freq_b"].append(
                self.__limit_value(
                    params["freq_b"][-1] + self.rate * params["freq_b_grad"],
                    max_value=params["freq_t"][-1] + 1,
                )
            )
            params["freq_t"].append(
                self.__limit_value(
                    params["freq_t"][-1] + self.rate * params["freq_t_grad"],
                    min_value=params["freq_b"][-1] + 1,
                    max_value=20000,
                )
            )
            params["dur"].append(
                self.__limit_value(
                    params["dur"][-1] + self.rate * params["dur_grad"],
                    min_value=10,
                    max_value=975,
                )
            )

            print(
                "New params: ",
                params["freq_b"][-1],
                params["freq_t"][-1],
                params["dur"][-1],
            )

            if params["freq_b_grad"] < 0:
                params["freq_b_step"] /= 2
            if params["freq_t_grad"] < 0:
                params["freq_t_step"] /= 2
            if params["dur_grad"] < 0:
                params["dur_step"] /= 2

            params["reward"] = 0

        params["param_n"] = params["param_n"] + 1

    def analyze(self, sound_type, reward=None):
        params = self.class_params[sound_type]
        reward = (
            reward
            or -math.sqrt(
                (params["freq_b"][-1] - self.x1) ** 2
                + (params["freq_t"][-1] - self.x2) ** 2
                + (params["dur"][-1] - self.x3) ** 2
            )
            / 28302
            * 3
            + random.random() * 0.01
        )

        new_params = self.make_step(sound_type, reward)
        return new_params


if __name__ == "__main__":
    optimizer = ParamsOptimizer()
    optimizer.x1 = 4000
    optimizer.x2 = 17000
    optimizer.x3 = 120

    for i in range(212):
        optimizer.analyze("music")
        if i % 28 == 3 and i // 84 >= 1:
            optimizer.class_params["music"]["freq_b_step"] = 100
            optimizer.class_params["music"]["freq_t_step"] = 100
            optimizer.class_params["music"]["dur_step"] = 100

        def draw(x1_hist, x2_hist, x3_hist, x1, x2, x3):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.plot3D(x1_hist, x2_hist, x3_hist, "b")
            ax.set_xlabel("freq_b")
            ax.set_ylabel("freq_t")
            ax.set_zlabel("duration")

            ax.scatter(x1, x2, x3, c="red")
            return plt.show()

    draw(
        optimizer.class_params["music"]["freq_b"][:64],
        optimizer.class_params["music"]["freq_t"][:64],
        optimizer.class_params["music"]["dur"][:64],
        optimizer.x1,
        optimizer.x2,
        optimizer.x3,
    )
