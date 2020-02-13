import os
import json
import re
import shutil
import click
from jinja2 import Environment, FileSystemLoader
from appdirs import AppDirs
from textx import generator
from txquestionnaire import questionnaire_interpret


THIS_FOLDER = os.path.dirname(__file__)


@generator('questionnaire', 'txproject')
def que_gen_txproject(metamodel, model, output_path, overwrite, debug):
    "Generate textX project from Questionnaire model."

    # 1. Try to load config data from the user folder
    dirs = AppDirs("textX")
    config_file = os.path.join(dirs.user_config_dir, 'scaffolding.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # 2. Interpret model and collect answers
    config = questionnaire_interpret(model, config)

    # 3. Cache collected data for futher use
    try:
        os.makedirs(os.path.dirname(config_file))
    except FileExistsError:
        pass
    with open(config_file, 'w+') as f:
        json.dump(config, f)

    # 4. Do scaffolding with the new data by using template project
    template_folder = os.path.join(THIS_FOLDER, 'template')
    scaffold(template_folder, output_path, config, overwrite)


placeholder_re = re.compile(r'__[^_]\w+?[^_]__')


class FileCount:
    def __init__(self):
        self.created = 0
        self.overwritten = 0
        self.skipped = 0

    def __str__(self):
        return f'{self.created}/{self.overwritten}/{self.skipped}'


def scaffold(templates_path, target_path, config, overwrite=False):
    """
    Args:
        templates_path (str): A path to templates used for scaffolding.
        target_path (str): The path where scaffolding should generate files.
        config (dict): A config for scaffolding contains any data necessary
            for rendering files using jinja2 engine.
        overwrite (bool): If the target files should be overwritten.
    """
    env = Environment(loader=FileSystemLoader(searchpath=templates_path),
                      trim_blocks=True, lstrip_blocks=True)
    file_count = FileCount()

    def should_skip(fname):
        return ('__lang__' in fname and config['type'] == 'gen') \
               or ('__gen__' in fname and config['type'] == 'lang')

    click.echo("\nStarted scaffolding of project in {}".format(target_path))
    for root, dirs, files in os.walk(templates_path):
        if should_skip(root):
            continue
        for f in files:
            if should_skip(f):
                continue

            src_file = os.path.join(root, f)
            src_rel_path = os.path.relpath(src_file, templates_path)
            target_file = os.path.join(target_path, src_rel_path)

            # Replace placeholders in the target file name.
            placeholders = placeholder_re.findall(target_file)
            for placeholder in placeholders:
                ph_value = config.get(placeholder.strip('_'))
                if ph_value is not None:
                    target_file = target_file.replace(placeholder, ph_value)

            # Strip j2 extension from target path.
            if target_file.endswith('.j2'):
                target_file = target_file[:-3]
            # Strip __lang__ / __gen__ from path
            target_file = target_file.replace('__lang__', '')\
                                     .replace('__gen__', '')

            # Create necessary folders.
            try:
                os.makedirs(os.path.dirname(target_file))
            except FileExistsError:
                pass

            if overwrite or not os.path.exists(target_file):

                if os.path.exists(target_file):
                    click.echo(f'Overwriting {target_file}')
                    file_count.overwritten += 1
                else:
                    click.echo(f'Creating {target_file}')
                    file_count.created += 1

                if src_file.endswith('.j2'):
                    # Render using Jinja2 template
                    with open(target_file, 'w') as f:
                        f.write(
                            env.get_template(src_rel_path).render(**config))
                else:
                    # Just copy
                    shutil.copy(src_file, target_file)

            else:
                click.echo(f'Skipping {target_file}')
                file_count.skipped += 1

    click.echo('Done. Files created/overwritten/skipped = {}'
               .format(file_count))
