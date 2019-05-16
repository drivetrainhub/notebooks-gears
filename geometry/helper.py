# Copyright 2019 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://www.drivetrainhub.com.

"""Helper module for geometry notebooks."""

from IPython.display import HTML
import random

from math import degrees


def hide_toggle(for_next=False, toggle_text=None):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    if toggle_text is None:
        if for_next:
            toggle_text = 'Toggle show/hide next cell'  # text shown on toggle link
        else:
            toggle_text = 'Toggle show/hide'  # text shown on toggle link

    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current,
        toggle_text=toggle_text
    )

    return HTML(html)


def round_degrees(rad) -> int:
    """Convert radians to degrees and round to the nearest integer."""

    if rad is not None:
        return int(round(degrees(rad), 0))


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
