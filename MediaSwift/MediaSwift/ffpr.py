# ffpr.py
# ---------

import os
import gc
import json
import subprocess
from functools import lru_cache
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED

console = Console()


class FFProbeResult:
    """
    >>> REPRESENTS THE INFO OF "FFPR" ANALYSIS ON MULTIMEDIA FILE.

    ⇨ ATTRIBUTE'S
    ---------------
    >>> INFO : DICT
        >>> INFORMATION OBTAINED FROM FFPR.

    ⇨ METHOD'S
    -----------
    >>> DURATION() ⇨  OPTIONAL FLOAT:
        >>> GET THE DURATION OF THE MULTIMEDIA FILE.
    >>> BIT_RATE() ⇨  OPTIONAL FLOAT:
        >>> GET THE BIT RATE OF THE MULTIMEDIA FILE.
    >>> NB_STREAMS() ⇨  OPTIONAL INT:
        >>> GET THE NUMBER OF STREAMS IN THE MULTIMEDIA FILE.
    ⇨ STREAMS():
        >>> GET THE DETAILS OF INDIVIDUAL STREAMS IN THE MULTIMEDIA FILE.

        >>> EXAMPLE:


        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpr

        >>> FFPR = ffpr()
        >>> INFO = FFPR.probe(r"PATH_TO_MEDIA_FILE")
        >>> FFPR.pretty(INFO)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

    >>> USE "PRETTY()" FOR MORE BEAUTIFY CONTENT SHOW.
    >>> RETURN NONE
    """

    def __init__(self, info):
        self.info = info

    @property
    def DURATION(self) -> Optional[float]:
        try:
            return float(self.info["format"]["duration"])
        except (KeyError, ValueError):
            return None

    @property
    def BIT_RATE(self) -> Optional[float]:
        try:
            return int(self.info["format"]["bit_rate"]) / 1000
        except (KeyError, ValueError):
            return None

    @property
    def NB_STREAMS(self) -> Optional[int]:
        return self.info["format"].get("nb_streams")

    @property
    def STREAMS(self):
        return self.info["streams"]


class ffpr:
    """
    >>> CLASS FOR INTERFACING WITH FFPR TO ANALYZE MULTIMEDIA FILES.

    ⇨ METHOD'S
    -----------
    PROBE INPUT_FILE ⇨ OPTIONAL:
    --------------------------------
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.
    ⇨ PRETTY( INFO )
    -----------------
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY CONTENT.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpr

        >>> DETAILS = ffpr()
        >>> INFO = DETAILS.probe(r"PATH_TO_MEDIA_FILE")
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
    >>> RETURN: NONE
    """

    console = Console()  # DECLARE CONSOLE AT THE CLASS LEVEL.

    def __init__(self):
        self._ffprobe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffpr.exe"
        )
        self.info = None

    @property
    def ffprobe_path(self):
        return self._ffprobe_path

    @lru_cache(maxsize=None)
    def probe(self, input_file) -> Optional[FFProbeResult]:
        """
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.

        ⇨ PARAMETER'S
        --------------
        INPUT_FILE : STR
        -----------------
            >>> PATH TO THE MULTIMEDIA FILE.

        ⇨ OPTIONAL
        -----------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        try:
            # Check if the input file exists
            if not os.path.isfile(input_file):
                raise FileNotFoundError(f"FILE '{input_file}' NOT FOUND")

            command = [
                self.ffprobe_path,
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                input_file,
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            self.info = FFProbeResult(json.loads(result.stdout.decode("utf-8")))
            gc.collect()
            self.pretty(self.info)
            return self.info
        except FileNotFoundError as e:
            error_message = Text(f"ERROR: {e}", style="bold red")
            console.print(error_message)
            return None
        except subprocess.CalledProcessError as e:
            error_message = Text(f"ERROR: {e}", style="bold red")
            console.print(error_message)
            return None
        except Exception as e:
            error_message = Text(
                f"ERROR: AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red"
            )
            console.print(error_message)
            return None

    @lru_cache(maxsize=None)
    def pretty(self, info: FFProbeResult):
        """
        >>> PLEASE ENHANCE THE FORMATTING USING THE PRETTY() FUNCTION TO PROVIDE MORE POLISHED INFORMATION .
        """
        if not info:
            console.print(
                "[bold magenta]WARNING: NO INFORMATION AVAILABLE.[/bold magenta]"
            )
            return

        os.system("cls")
        console.print("\n[bold magenta]MEDIA FILE ANALYSIS SUMMARY:[/bold magenta]")
        console.print("[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        table = Table(show_header=True, header_style="bold magenta", box=ROUNDED)
        table.add_column("[bold magenta]PROPERTY[/bold magenta]", style="cyan")
        table.add_column("[bold magenta]VALUE[/bold magenta]", style="cyan")

        table.add_row(
            "[bold magenta]FILENAME[/bold magenta]",
            info.info["format"]["filename"].upper(),
        )
        table.add_row(
            "[bold magenta]NB_STREAMS[/bold magenta]",
            str(info.info["format"]["nb_streams"]).upper(),
        )
        table.add_row(
            "[bold magenta]NB_PROGRAMS[/bold magenta]",
            str(info.info["format"]["nb_programs"]).upper(),
        )
        table.add_row(
            "[bold magenta]FORMAT_NAME[/bold magenta]",
            info.info["format"]["format_name"].upper(),
        )
        table.add_row(
            "[bold magenta]FORMAT_LONG_NAME[/bold magenta]",
            info.info["format"]["format_long_name"].upper(),
        )
        table.add_row(
            "[bold magenta]START_TIME[/bold magenta]",
            str(info.info["format"]["start_time"]).upper(),
        )
        table.add_row(
            "[bold magenta]DURATION[/bold magenta]",
            str(info.info["format"]["duration"]).upper(),
        )
        table.add_row(
            "[bold magenta]SIZE[/bold magenta]",
            str(info.info["format"]["size"]).upper(),
        )
        table.add_row(
            "[bold magenta]BIT_RATE[/bold magenta]",
            str(info.info["format"]["bit_rate"]).upper(),
        )
        table.add_row(
            "[bold magenta]PROBE_SCORE[/bold magenta]",
            str(info.info["format"]["probe_score"]).upper(),
        )

        console.print(table)

        for stream_number, stream_info in enumerate(info.STREAMS, start=1):
            stream_table = Table(
                show_header=True, header_style="bold magenta", box=ROUNDED
            )
            stream_table.add_column(
                "[bold magenta]STREAM {} [/bold magenta]".format(stream_number),
                style="cyan",
            )
            stream_table.add_column("[bold magenta]VALUE[/bold magenta]", style="cyan")

            stream_type = (
                "VIDEO STREAM: "
                if stream_info["codec_type"] == "video"
                else "AUDIO STREAM: "
            )
            stream_table.add_row(f"[bold magenta]{stream_type}[/bold magenta]", "")

            for key, value in stream_info.items():
                if isinstance(
                    value, dict
                ):  # If the value is a dictionary, format it nicely
                    formatted_value = ", ".join(f"{k}: {v}" for k, v in value.items())
                    stream_table.add_row(
                        f"[bold magenta]{key.upper()}[/bold magenta]",
                        formatted_value.upper(),
                    )
                else:
                    stream_table.add_row(
                        f"[bold magenta]{key.upper()}[/bold magenta]",
                        str(value).upper(),
                    )

            console.print(stream_table)

        gc.collect()
