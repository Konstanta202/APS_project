from APS_project.Kursovik.Models.Configurate.config import Config
from APS_project.Kursovik.Models.Modeling.modeling import Modeling
import warnings
warnings.filterwarnings("ignore")

def main():
    for i in range(1,11):
        print(f"Количество приборов:{i}")
        print(f"Размер буффера: 10")
        config = Config(1000,5,i,10,1.1,2,1.5,'auto')
        model = Modeling(config.to_dict())
        model.auto_simulation()

    for i in range(1,11):
        print("Количество приборов: 10")
        print(f"Размер буффера: {i}")
        config = Config(2000,5,10,i,1.1,2,1.5,'auto')
        model = Modeling(config.to_dict())
        model.auto_simulation()



if __name__ == '__main__':

    mode = 'auto'
    if mode == 'auto':
        # config = Config(1000, 10, 10, 10, 1.3, 2, 1.5, 'auto')
        # model = Modeling(config.to_dict())
        # model.auto_simulation()
        main()
    elif mode == 'step':
        config = Config(1000, 10, 10, 10, 1.3, 2, 1.5, 'auto')
        model = Modeling(config.to_dict())
        model.step_simulation()
    else:
        raise 'Invalid set mode'
