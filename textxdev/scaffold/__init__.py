import contextlib
import json
import os

from appdirs import AppDirs
from textx import generator
from textxjinja import textx_jinja_generator
from txquestionnaire import questionnaire_interpret

THIS_FOLDER = os.path.dirname(__file__)


@generator('questionnaire', 'txproject')
def que_gen_txproject(_metamodel, model, output_path, overwrite, _debug):
    "Generate textX project from Questionnaire model."

    # Try to load config data from the user folder
    dirs = AppDirs("textX")
    config_file = os.path.join(dirs.user_config_dir, 'scaffolding.json')
    if os.path.exists(config_file):
        with open(config_file) as f:
            config = json.load(f)
    else:
        config = {}

    # Interpret model and collect answers
    config = questionnaire_interpret(model, config)

    # Configuration
    config['lang'] = config['type'] == 'lang'
    config['gen'] = config['type'] == 'gen'
    config['project_name'] = os.path.basename(os.path.abspath(output_path))

    # Cache collected data for futher use
    with contextlib.suppress(FileExistsError):
        os.makedirs(os.path.dirname(config_file))
    with open(config_file, 'w+') as f:
        json.dump(config, f)

    # Do scaffolding with the new data by using template project
    template_folder = os.path.join(THIS_FOLDER, 'template')
    textx_jinja_generator(template_folder, output_path, config, overwrite)
