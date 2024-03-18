# ffpl.py
# ---------

from rich.panel import Panel
from rich.console import Console
import gc
import subprocess
from functools import lru_cache
import time
from pathlib import Path

console = Console(width=40)


class ffpl:
    """
    >>> CLASS FOR INTERFACING TO PLAY MULTIMEDIA FILES.

    ATTRIBUTES
    ----------
    >>> ⇨ FFPL_PATH : STR
        >>> PATH TO THE FFPL EXECUTABLE.

    METHODS
    -------
    >>> ⇨ PLAY(MEDIA_FILE)
        >>> PLAY MULTIMEDIA FILE.
    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >>> from MediaSwift import ffpl
    >>> play = ffpl()

    # INCREASE VOLUME BY 5 DB
    >>> volume = 5
    >>> media_file = r"PATH_TO_MEDIA_FILE"
    >>> play.play(media_file)

    >>> play.play(media_file, noborder=True)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ```
    >>> RETURNS: NONE
    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPL INSTANCE.
        >>> SETS THE DEFAULT PATH TO THE FFPL EXECUTABLE.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"
        >>> play.play(media_file)

        >>> play.play(media_file, noborder=True)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURN: NONE
        """
        self.ffplay_path = Path(__file__).resolve().parent / "bin" / "ffpl.exe"

    @lru_cache(maxsize=None)  # SETTING MAXSIZE TO NONE MEANS AN UNBOUNDED CACHE
    def play(self, media_file, volume=0, noborder=False):
        """
        >>> PLAY MULTIMEDIA FILE USING FFPL WITH SPECIFIED VIDEO FILTERS.

        ⇨ PARAMETER'S
        ------------
        >>> MEDIA_FILE : STR
           >>> PATH TO THE MULTIMEDIA FILE TO BE PLAYED.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"

        # INCREASE VOLUME BY 10 DB
        >>> volume = 5
        >>> play.play(media_file, volume)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURNS: NONE

        """
        console_1 = Console(width=100)
        if not Path(media_file).exists():
            console_1.print(
                Panel(
                    f"ERROR: THE FILE PATH [bold green]{media_file.upper()}[/bold green] DOES NOT EXIST.",
                    style="bold red",
                )
            )
            return

        if not Path(media_file).is_file():
            console_1.print(
                Panel(
                    f"ERROR: [bold green]{media_file.upper()}[/bold green] IS NOT A FILE PATH.",
                    style="bold red",
                )
            )
            return

        # Modify the command to include the options for setting.
        command = [
            str(self.ffplay_path),
            "-hide_banner",
            "-vf",
            "hqdn3d,unsharp",
            "-loglevel",
            "panic",  # Adjusted log level here
            "-af",
            f"volume={volume}dB",
        ]

        if noborder:
            command.append("-noborder")

        command.append(str(media_file))

        console.clear()
        console.print(Panel("MEDIA PLAYER. NOW PLAYING 🎵", style="bold green"))

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            console.print(
                f"AN ERROR OCCURRED WHILE PLAYING THE MEDIA FILE: {e}", style="bold red"
            )
        except Exception as e:
            console.print(f"AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red")
        finally:
            console.clear()
            console.print(Panel("MEDIA PLAYER EXITED..", style="bold yellow"))
            time.sleep(2)
            console.clear()
            gc.collect()
