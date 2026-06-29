import platform
import shlex
import subprocess
from enum import StrEnum
from pathlib import Path

import typer

PROJECT_ROOT = Path(__file__).parent.parent.parent
MONOREPO_ROOT = PROJECT_ROOT.parent.parent
LOCAL_PATH = MONOREPO_ROOT / ".local"
CMAKE_OUT = LOCAL_PATH / "cmake"
CMAKE_BUILD = CMAKE_OUT / "build"
CMAKE_DIST = CMAKE_OUT / "dist"
VCPKG_VERSION = "2024.07.12"
VCPKG_PATH = LOCAL_PATH / "vcpkg"
VCPKG_EXE_PATH = VCPKG_PATH / "vcpkg"

app = typer.Typer()


class BuildMode(StrEnum):
    debug = "debug"
    release = "release"


@app.command()
def setup(mode: BuildMode = BuildMode.debug):
    vcpk_install()
    cmake_prepare(mode=mode)


@app.command()
def build(mode: BuildMode = BuildMode.debug):
    cmake_build(mode=mode)


@app.command()
def ctest(
    rebuild: bool = True,
    mode: BuildMode = BuildMode.debug,
    test: str | None = None,
):
    """
    Run the tests using CTest.
    """
    if not CMAKE_BUILD.exists():
        typer.echo(
            "CMake build directory does not exist. Please run 'setup' or 'build' first."
        )
        raise typer.Exit(code=1)

    cmake_test(rebuild=rebuild, mode=mode, regex=test)


def vcpk_install():
    VCPKG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not (VCPKG_PATH / ".git").exists():
        run_command(
            f"git clone https://github.com/microsoft/vcpkg {VCPKG_PATH.as_posix()}",
        )

    run_command(
        "git fetch --all",
        cwd=VCPKG_PATH,
    )
    run_command(
        f"git checkout {VCPKG_VERSION}",
        cwd=VCPKG_PATH,
    )
    run_command(
        "bash bootstrap-vcpkg.sh -useSystemBinaries",
        cwd=VCPKG_PATH,
        shell=True if platform.system() == "Windows" else False,
    )
    run_command(
        f"{VCPKG_EXE_PATH.as_posix()} upgrade --no-dry-run",
    )
    run_command(
        f"{VCPKG_EXE_PATH.as_posix()} install cmocka",
    )


def cmake_prepare(*, mode: BuildMode):
    run_command(
        f"""
        cmake
            -DCMAKE_TOOLCHAIN_FILE={VCPKG_PATH.as_posix()}/scripts/buildsystems/vcpkg.cmake
            -S {PROJECT_ROOT.as_posix()}
            -B {CMAKE_BUILD.as_posix()}
            -DCMAKE_INSTALL_PREFIX={CMAKE_DIST.as_posix()}
            -DBUILD_TESTING=1
            -DCMAKE_BUILD_TYPE={mode}
        """
    )


def cmake_build(*, mode: BuildMode):
    run_command(
        f"cmake --build {CMAKE_BUILD.as_posix()} --config {mode} --target install"
    )


def cmake_test(*, rebuild: bool, mode: BuildMode, regex: str | None):
    if rebuild:
        cmake_build(mode=mode)
    suffix = f" -R {regex}" if regex else ""
    run_command(
        f"ctest --test-dir {CMAKE_BUILD.as_posix()} --output-on-failure -C {mode} -V{suffix}",
        check=False,
    )


def run_command(cmd: str, *args, **kwargs):
    cmd_ = shlex.split(cmd)
    typer.echo(f"Running command: {cmd_}")
    cp = subprocess.run(
        cmd_,
        *args,
        **{
            "shell": False,
            "check": True,
            "universal_newlines": True,
            **kwargs,
        },
    )
    return cp


if __name__ == "__main__":
    app()
