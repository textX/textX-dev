import os
import click
from textx import metamodel_for_language
import textxdev.scaffold
from textxdev.scaffold import que_gen_txproject


MODEL_FOLDER = os.path.abspath(os.path.dirname(textxdev.scaffold.__file__))


def startproject(textx):
    @textx.command()
    @click.argument('output_path', type=click.Path(), required=True)
    @click.option('--overwrite', is_flag=True, default=False, required=False,
                  help='Should overwrite output files if exist.')
    @click.pass_context
    def startproject(ctx, output_path, overwrite):
        """
        Run questionnaire, collect info and scaffold textX project.
        """
        debug = ctx.obj['debug']
        mm = metamodel_for_language('questionnaire')
        model = mm.model_from_file(os.path.join(MODEL_FOLDER, 'project.que'))
        que_gen_txproject.generator(mm, model, output_path, overwrite, debug)
