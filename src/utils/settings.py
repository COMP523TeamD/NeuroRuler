"""Global settings that the user should be able to modify directly, unlike globs.py, via JSON, GUI, CLI, etc.

For now, we modify most of these using CLI args."""

from pathlib import Path
import src.utils.constants as constants

DEBUG: bool = False
"""Whether or not to print debugging information throughout execution.

Defaults to False."""

SMOOTH_BEFORE_RENDERING: bool = False
"""Whether or not to smooth the image before rendering, defaults to False.

Affects MRIImage.resample() and imgproc.contour()."""

IMG_DIR: Path = Path("img")
"""Directory for storing images. Defaults to `./img/`.

TODO: Warn the user that images here may be overwritten in our documentation. It is not a safe directory
to use for file storage and should only be used by the program."""

FILE_BROWSER_START_DIR: Path = Path("ExampleData")
"""The starting directory that is opened in the file browser.

Defaults to ExampleData/ during development, for now.

Will default to the home directory for the user.

Should be configurable via JSON later."""

EXPORTED_FILE_NAMES_USE_INDEX: bool = False
"""If True, then exported files will be named using the index in the program.

E.g. 1_0_0_0_0.png, 2_90_180_0_60.csv, etc., where the first part is the file name and the other parts are settings.

If False (default), then exported files will be named using the file name of the original file.

E.g. MicroBiome_1month_T1w_0_0_0_0.png, MicroBiome_1month_T1w_90_180_0_60.csv."""

IMAGE_STATUS_BAR_SHOWS_FULL_PATH: bool = False
"""If False (default), the GUI will display only the file name of the image instead of the full path."""

CONTOUR_COLOR: str = constants.HCT_MAIN_COLOR
"""Color of the contour. Defaults to constants.HCT_MAIN_COLOR = #b55162 = R 181 G 81 B 98.

This can be a 6-hexit string rrggbb (don't prepend 0x) or a name (e.g. red, blue, etc.).

Internally, this is converted to a QColor using imgproc.string_to_QColor().

QColor supports 8-hexit rrggbbaa but doesn't work in our GUI, i.e. aa=00 appears fully bright in the GUI.

The problem likely lies in :code:`src.GUI.main.render_curr_slice()`? Not a huge deal.

This is considered a setting because the user can modify it via CLI. It's just that the default
value is a constant value from constants.py.

parse_cli.py hardcodes this value to theme colors from BSS JSON files for themes where the theme color
isn't the HCT main color."""

THEME_NAME: str = "dark-hct"
"""Name of theme in src/GUI/themes.

Defaults to 'dark-hct'.

Configurable via -t, --theme CLI option.

The full path to the .qss file is {globs.THEME_DIR}/{THEME_NAME}/stylesheet.qss."""
