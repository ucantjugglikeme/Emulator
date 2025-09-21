import os
from emul.emul import setup_emul
from emul.utils import programm_to_emul


if __name__ == '__main__':
    emul = setup_emul(
        config_path=os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'config.yaml'
        )
    )
    programm_to_emul(emul=emul,
        programm_path=os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'prog/fact2.asm'
        )
    )
    emul.execute_programm()
    print(emul)
    