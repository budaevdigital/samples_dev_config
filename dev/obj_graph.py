"""
Для использования требуется предварительная настройка и доп. зависимость
sudo apt-get install libgtk-3-dev  |  brew install gtk+3
> pip install PyGObject
> pip install xdot <- для отрисовки графов
"""

import gc
import logging

import objgraph

logger = logging.getLogger(__name__)


async def show_growth_objgraph(classname_for_check: str | None = None, name_png: str | None = None,
                               is_refs: bool = True) -> dict[str, str]:
    gc.collect() # cоберем мусор перед отрисовкой

    objgraph.show_most_common_types(limit=20)  # Топ-20 используемых типов данных
    objgraph.show_growth() # показывает рост объектов после выполнения кода

    if classname_for_check and name_png:
        if is_refs:
            objgraph.show_refs([objgraph.by_type(classname_for_check)], filename=f"refs_{name_png}_list.png")
            objgraph.show_refs([objgraph.by_type(classname_for_check[0])], filename=f"refs_{name_png}_0.png")
        else:
            objgraph.show_backrefs([objgraph.by_type(classname_for_check)], filename=f"backrefs_{name_png}_list.png")
            objgraph.show_backrefs([objgraph.by_type(classname_for_check)[0]], filename=f"backrefs_{name_png}_0.png")
        return {"detail": "See console for graph to growth"}
    return {"detail": "See console"}
