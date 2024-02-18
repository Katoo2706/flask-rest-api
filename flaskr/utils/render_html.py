from jinja2 import Environment, FileSystemLoader, TemplateNotFound


# Function to read the HTML file and render it using Jinja2
def render_html(html_file, **kwargs):
    """
    Load the templates file and use Jinja to send the parameters
    :param html_file: html file in templates folder
    :param kwargs: key arguments
    :return:
    """
    try:
        templateLoader = FileSystemLoader(searchpath="./flaskr/templates/")
        templateEnv = Environment(loader=templateLoader)
        template = templateEnv.get_template(html_file)
        return template.render(**kwargs)  # this is where to put args to the template renderer

    except TemplateNotFound:
        # Handle template not found error
        return f"Template '{html_file}' not found in the templates directory."

    except Exception as e:
        # Handle other exceptions
        return f"An error occurred: {str(e)}"
