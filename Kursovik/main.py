from Kursovik.Models.Configurate.config import Config
from Kursovik.Models.Modeling.modeling import Modeling
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    config = Config(5,2,2,2,1.3,2,1.5,'step')
    model = Modeling(config.to_dict())
    if config.mode == 'auto':
        model.auto_simulation()
    elif config.mode == 'step':
        model.step_simulation()
    else:
        raise 'Invalid set mode'
