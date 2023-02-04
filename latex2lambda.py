from latex2sympy2 import latex2sympy
from sympy import lambdify
import re


class TexWithoutArgumentsError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class TexMalformattedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


def validate_input(tex: str) -> tuple[str, list]:
    tex = tex.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")

    if len(tex.split("=")) != 2:
        raise TexMalformattedError(
            "Invalid tex format. Provide a tex string on format r'f(<args>) = <...>'."
        )

    fargs_tex, tex = tex.split("=")

    args_tex = re.findall(r"(?<=\().+?(?=\))", fargs_tex)
    if len(args_tex) != 1:
        raise TexMalformattedError(
            "Invalid tex format. Provide the arguments between a single pair of parenthesis, that is on format '(<args>)'."
        )

    args = args_tex[0].split(",")

    if len(args) < 1:
        raise TexWithoutArgumentsError(
            "No arguments provided. Either pass the arguments as the args list or with the tex on format r'f(<args>) = <...>'."
        )

    return tex, args


def latex2lambda(
    tex: str,
    variable_values={},
    args=None,
    modules=None,
    printer=None,
    use_imps=True,
    dummify=False,
):
    if args is None:
        tex, args = validate_input(tex)

    sympy_form = latex2sympy(tex, variable_values)
    lambda_form = lambdify(
        args=args,
        expr=sympy_form,
        modules=modules,
        printer=printer,
        use_imps=use_imps,
        dummify=dummify,
    )

    return lambda_form


if __name__ == "__main__":
    test = r"f(x,a) = a*\sin(x)"
    func = latex2lambda(test)

    print(func)
