"""Helper module for Jupyter notebooks."""

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
