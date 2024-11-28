from scipy.stats import norm

from APS_project.Kursovik.Models.Configurate.config import Config
from APS_project.Kursovik.Models.Modeling.modeling import Modeling
import warnings
warnings.filterwarnings("ignore")


from scipy.optimize import fsolve
if __name__ == '__main__':
    #
    # def equation_to_solve(sigma, a, p):
    #     return 2 * norm.cdf(a / sigma) - 1 - p
    #
    # a = 1
    # b = 2
    # p = 0.15
    # sigma_value = fsolve(equation_to_solve, x0=1, args=(a, p))[0]
    # prob_b = 2 * norm.cdf(b / sigma_value) - 1
    # print(sigma_value, round(prob_b, 4))

    config = Config(5,2,2,2,1.3,2,1.5,'step')
    model = Modeling(config.to_dict())
    if config.mode == 'auto':
        model.auto_simulation()
    elif config.mode == 'step':
        model.step_simulation()
    else:
        raise 'Invalid set mode'
