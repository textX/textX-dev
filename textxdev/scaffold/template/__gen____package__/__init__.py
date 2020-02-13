from textx import generator, gen_file


@generator('{{language}}', '{{target}}')
def {{language}}_generate_{{target}}(metamodel, model, output_path,
                                     overwrite, debug, **custom_args):
    """
    Generator for generating {{target}} from {{language}} descriptions.
    """

    gen_file('dot', partial(metamodel_export, model), model.file_name,
             output_path, overwrite,
             success_message=lambda output_file:
                 'To convert to png run "dot -Tpng -O {}"'
                 .format(os.path.basename(output_file)))

