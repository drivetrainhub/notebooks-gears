# Copyright 2019 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://www.drivetrainhub.com.

"""Helper module for tooling notebooks."""

from IPython.display import display, Latex, HTML


def print_latex(str_list):
    """Display a comma-separated list of LaTeX strings in a Jupyter notebook.

    :param str_list: List of LaTeX string, e.g. ['$\\alpha$', '$\\beta$']
    :return: None
    """

    display(Latex('$, \\;\\;$'.join(str_list)))


def html_table(headings, rows):
    """Display an HTML table in a Jupyter notebook.

    :param headings: List of heading strings.  Can include MathJax notation.
    :param rows: List of lists to represent rows of data.
    :return: None
    """

    html_str = '<table style="margin-left: 0">'

    html_str += '<tr>'

    for h in headings:
        html_str += f'<th>{h}</th>'

    html_str += '</tr>'

    for row in rows:
        html_str += '<tr>'
        for c in row:
            html_str += f'<td>{c}</td>'

        html_str += '</tr>'

    html_str += '</table>'
    display(HTML(html_str))
