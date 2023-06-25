"""
    Script para gerar um notebook, nescessário que cada folder em --path
    possua um subfolder chamado notebook com as implementações.

    Agradecimento especial a @Tiagofs00 (github) pelo script original.
"""
from pathlib import Path
from typing import Tuple
import subprocess
import argparse
import shutil
import os


def get_args():
    """
    Receber argumentos via linha de comando
    """
    parser = argparse.ArgumentParser(
        description="Create a notebook from given files.")
    parser.add_argument(
        "--source",
        type=str,
        default=os.path.dirname(__file__) + "/../../",
        help="diretório com para as implementações",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.dirname(__file__) + "/../../",
        help="diretório que será salvo o notebook",
    )
    parser.add_argument(
        "--rmaux", type=bool, default=True,
        help="remover ou não aqrquivos auxiliares"
    )
    args = parser.parse_args()
    return args


def remove_aux() -> None:
    """
    Remove os arquivos auxiliares gerados no processo
    """
    to_remove = [
        "notebook.aux",
        "notebook.log",
        "notebook.toc",
        "notebook.tex",
        "texput.log",
    ]
    for item in to_remove:
        if os.path.exists(item):
            os.remove(item)


def get_codes(path: Path,
              valid_exts: Tuple[str, str, str] = (".cpp", ".py", ".h")):
    """
    Gera uma lista com as implementações que serão adicionadas ao notebook.
    Args:
        path (Path): Caminho para o diretório do notebook.tex
        valid_exts (Tuple[str, str, str], optional): Extensões válidas para implementações
    """
    section_list = [
        "Geometria_Computacional",
        "Estruturas_de_Dados",
        "Matematica",
        "Paradigmas",
        "Strings",
        "Grafos",
    ]

    section = []

    for section_name in section_list:
        subsection = list()
        section_path = path / section_name / "notebook"
        files = os.listdir(section_path)
        for file_name in files:
            print("  ", file_name)
            if file_name.endswith(valid_exts):
                subsection.append(file_name)
        section.append((section_name, subsection))

    return section


def gen_tex(sections: list, path: Path) -> None:
    """
    Gera o notebook.tex com o template e implementações
    """

    # Copia o template para o noteboo.tex
    shutil.copyfile(
        Path(os.path.dirname(__file__)) / "template.tex", path / "notebook.tex"
    )

    # Gerar o tex em uma string
    aux = ""
    for item, subsection in sections:
        aux += "\\section{%s}\n" % item.replace("_", " ")
        for file in subsection:
            name, ext = os.path.splitext(file)
            name = os.path.split(name)[1]  # Remove Segtree/ prefix
            file_name = " ".join([x.capitalize() for x in name.split("_")])
            file_path = os.path.join(path, item, "notebook", file)

            aux += "\\includes{%s}{%s}\n" % (file_name, file_path)

    aux += "\n\\end{multicols}\n\\end{document}\n"

    # Salvar em disco
    with open(path / "notebook.tex", "a") as texfile:
        texfile.write(aux)


def gen_pdf(tex_path: Path) -> None:
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        tex_path / "notebook.tex",
    ]

    subprocess.check_call(cmd)


if __name__ == "__main__":
    args = get_args()

    sections = get_codes(path=Path(args.source))

    gen_tex(sections=sections, path=Path(args.output))

    gen_pdf(tex_path=Path(args.output))

    if args.rmaux:
        remove_aux()
