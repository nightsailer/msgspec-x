import sys
import os

from setuptools import setup
from setuptools.extension import Extension

import versioneer

# Check for 32-bit windows builds, which currently aren't supported. We can't
# rely on `platform.architecture` here since users can still run 32-bit python
# builds on 64 bit architectures.
if sys.platform == "win32" and sys.maxsize == (2**31 - 1):
    import textwrap

    error = """
    ====================================================================
    `msgspec-x` currently doesn't support 32-bit Python windows builds. If
    this is important for your use case, please open an issue on GitHub:

    https://github.com/nightsailer/msgspec-x/issues
    ====================================================================
    """
    print(textwrap.dedent(error))
    exit(1)


SANITIZE = os.environ.get("MSGSPEC_SANITIZE", False)
COVERAGE = os.environ.get("MSGSPEC_COVERAGE", False)
DEBUG = os.environ.get("MSGSPEC_DEBUG", SANITIZE or COVERAGE)

extra_compile_args = []
extra_link_args = []
if SANITIZE:
    extra_compile_args.extend(["-fsanitize=address", "-fsanitize=undefined"])
    extra_link_args.extend(["-lasan", "-lubsan"])
if COVERAGE:
    extra_compile_args.append("--coverage")
    extra_link_args.append("-lgcov")
if DEBUG:
    extra_compile_args.extend(["-O0", "-g", "-UNDEBUG"])

ext_modules = [
    Extension(
        "msgspec._core",
        [os.path.join("msgspec", "_core.c")],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

yaml_deps = ["pyyaml"]
toml_deps = ['tomli ; python_version < "3.11"', "tomli_w"]
doc_deps = ["sphinx", "furo", "sphinx-copybutton", "sphinx-design", "ipython"]
test_deps = [
    "pytest",
    "msgpack",
    "attrs",
    'eval-type-backport ; python_version < "3.10"',
    *yaml_deps,
    *toml_deps,
]
dev_deps = ["pre-commit", "coverage", "mypy", "pyright", *doc_deps, *test_deps]

extras_require = {
    "yaml": yaml_deps,
    "toml": toml_deps,
    "doc": doc_deps,
    "test": test_deps,
    "dev": dev_deps,
}

setup(
    name="msgspec-x",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    maintainer="Night Sailer",
    maintainer_email="nightsailer@gmail.com",
    url="https://nightsailer.github.io/msgspec-x/",
    project_urls={
        "Documentation": "https://nightsailer.github.io/msgspec-x/",
        "Source": "https://github.com/nightsailer/msgspec-x/",
        "Issue Tracker": "https://github.com/nightsailer/msgspec-x/issues",
    },
    description=(
        "A community-driven fork of msgspec: fast serialization and validation library with "
        "builtin support for JSON, MessagePack, YAML, and TOML. Provides dual namespace "
        "architecture - 'msgspec' for full compatibility and 'msgspec_x' for extended features."
    ),
    keywords="JSON msgpack MessagePack TOML YAML serialization validation schema fork community",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    extras_require=extras_require,
    license="BSD",
    packages=["msgspec", "msgspec_x"],
    package_data={"msgspec": ["py.typed", "*.pyi"], "msgspec_x": ["py.typed", "*.pyi"]},
    ext_modules=ext_modules,
    long_description=(
        open("README.md", encoding="utf-8").read()
        if os.path.exists("README.md")
        else ""
    ),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    zip_safe=False,
)
