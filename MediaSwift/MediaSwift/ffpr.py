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
from rich.traceback import install

install(show_locals=True)
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
        >>> print(INFO)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

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

        # ENHANCE THE APPEALING CONTENT
        >>> INFO = DETAILS.probe(r"PATH_TO_MEDIA_FILE", pretty=True)
        >>> print(INFO)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
    >>> USE "pretty=True" MORE VISUALLY APPEALING FORMAT.
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

    # ==========================================================================================================================================================

    # @lru_cache(maxsize=None)
    # def probe(self, input_file) -> Optional[FFProbeResult]:
    #     """
    #     >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.

    #     ⇨ PARAMETER'S
    #     --------------
    #     INPUT_FILE : STR
    #     -----------------
    #         >>> PATH TO THE MULTIMEDIA FILE.

    #     ⇨ OPTIONAL
    #     -----------
    #         >>> RESULT OF THE FFPR ANALYSIS.
    #         >>> RETURN: NONE
    #     """
    #     try:
    #         # Check if the input file exists
    #         if not os.path.isfile(input_file):
    #             raise FileNotFoundError(f"FILE '{input_file}' NOT FOUND")

    #         command = [
    #             self.ffprobe_path,
    #             "-v",
    #             "quiet",
    #             "-print_format",
    #             "json",
    #             "-show_format",
    #             "-show_streams",
    #             input_file,
    #         ]
    #         result = subprocess.run(
    #             command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    #         )
    #         self.info = FFProbeResult(json.loads(result.stdout.decode("utf-8")))
    #         gc.collect()
    #         self.pretty(self.info)
    #         return self.info
    #     except FileNotFoundError as e:
    #         error_message = Text(f"ERROR: {e}", style="bold red")
    #         console.print(error_message)
    #         return None
    #     except subprocess.CalledProcessError as e:
    #         error_message = Text(f"ERROR: {e}", style="bold red")
    #         console.print(error_message)
    #         return None
    #     except Exception as e:
    #         error_message = Text(
    #             f"ERROR: AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red"
    #         )
    #         console.print(error_message)
    #         return None

    # ==========================================================================================================================================================

    @lru_cache(maxsize=None)
    def probe(self, input_file, pretty: bool = False) -> Optional[str]:
        """
        ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT IN JSON FORMAT.

        PARAMETER'S
        --------------
        INPUT_FILE : STR
        -----------------
            PATH TO THE MULTIMEDIA FILE.

        pretty : bool, optional
            Whether to use the pretty format or not. Default is False.

        OPTIONAL
        -----------
            RESULT OF THE FFPR ANALYSIS IN JSON FORMAT OR PRETTY FORMAT DEPENDING ON pretty.
            RETURN: NONE
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
            json_data = result.stdout.decode("utf-8")

            if pretty:
                parsed_info = FFProbeResult(json.loads(json_data))
                self.pretty(parsed_info)
                return "-"
            else:
                console = Console()
                os.system("cls")
                console.print(
                    "[bold magenta]JSON OUTPUT :Receipt:[/bold magenta]"
                )  # Magenta color for header
                console.print("[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                # Split JSON data into key-value pairs and apply rich formatting
                for line in json_data.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().upper()
                        value = value.strip().upper()
                        console.print(
                            f"[bold magenta]{key}[/bold magenta]: [cyan]{value}[/cyan]"
                        )
                    else:
                        console.print(line)
                return "-"

        except FileNotFoundError as e:
            error_message = f"ERROR: {e}"
            console.print(
                f"[bold red]{error_message}[/bold red]"
            )  # Bold red for error message
            return None
        except subprocess.CalledProcessError as e:
            error_message = f"ERROR: {e}"
            console.print(
                f"[bold red]{error_message}[/bold red]"
            )  # Bold red for error message
            return None
        except Exception as e:
            error_message = f"ERROR: AN UNEXPECTED ERROR OCCURRED: {e}"
            console.print(
                f"[bold red]{error_message}[/bold red]"
            )  # Bold red for error message
            return None

    @lru_cache(maxsize=None)
    def pretty(self, info: FFProbeResult):
        """
        >>> FORMATS AND PRINTS A SUMMARY OF THE FFPR ANALYSIS RESULT.

        ARGS:
        -----
            >>> INFO (FFPRRESULT): THE FFPRRESULT OBJECT CONTAINING THE ANALYSIS INFORMATION.

        TAGS:
        ----
            >>> SUMMARY: THIS METHOD FORMATS AND PRINTS A SUMMARY OF THE FFPR ANALYSIS RESULT.
            >>> FORMATTING: THIS METHOD HANDLES THE FORMATTING OF THE ANALYSIS SUMMARY.
            >>> PRINTING: THIS METHOD PRINTS THE FORMATTED ANALYSIS SUMMARY.
            >>> FFPR: THIS METHOD INTERACTS WITH FFPROBERESULT TO OBTAIN ANALYSIS INFORMATION.
            >>> MULTIMEDIA: THIS METHOD DEALS WITH MULTIMEDIA FILE ANALYSIS.
            >>> RICH: THIS METHOD UTILIZES THE RICH LIBRARY FOR CONSOLE OUTPUT FORMATTING.

        """
        if not info:
            console.print(
                "[bold magenta]WARNING: NO INFORMATION AVAILABLE.[/bold magenta]"
            )
            return

        os.system("cls" if os.name == "nt" else "clear")
        console.print(
            "\n[bold magenta]MEDIA FILE ANALYSIS SUMMARY:[/bold magenta] :Bookmark_tabs:"
        )
        console.print("[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

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
            "[bold magenta]FORMAT_NAME[/bold magenta]",
            info.info["format"]["format_name"].upper(),
        )
        table.add_row(
            "[bold magenta]FORMAT_LONG_NAME[/bold magenta]",
            info.info["format"]["format_long_name"].upper(),
        )
        table.add_row(
            "[bold magenta]START_TIME[/bold magenta]",
            f"{float(info.info['format']['start_time']):.2f}",
        )
        table.add_row(
            "[bold magenta]DURATION[/bold magenta]",
            f"{int(float(info.info['format']['duration'])/60):02d}:{int(float(info.info['format']['duration'])%60):02d}",
        )
        table.add_row(
            "[bold magenta]SIZE[/bold magenta]",
            f"{int(info.info['format']['size'])/(1024*1024):.2f} MB",
        )

        table.add_row(
            "[bold magenta]BIT_RATE[/bold magenta]",
            f"{int(info.info['format']['bit_rate'])/1000} kb/s",
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
                "VIDEO STREAM:"
                if stream_info["codec_type"] == "video"
                else "AUDIO STREAM: "
            )
            stream_table.add_row(f"[bold magenta]{stream_type}[/bold magenta]", "")

            for key, value in stream_info.items():
                if isinstance(value, dict):
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
