from manipulate import manipulate
from manipulate import actions, sources, destinations


# def test_from_python() -> None:
#     csv = CSV()
#     manipulate(
#         sources.Files('*.csv'),
#         (
#             actions.Parse(csv),
#             actions.Eval('x=int(y)+1'),
#             actions.Drop('z'),
#             actions.Render(csv),
#         ),
#         destinations.Files('.'),
#     )
