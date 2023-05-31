from pathlib import Path
from typing import Tuple

import rioxarray as rxr
import xarray as xr


def read_geotiff_as_da(file_path: str) -> xr.DataArray:
    """Read lazily a Geotiff file as a xarray DataArray.

    One of the main advantage here is to avoid to load the array contained in the file in memory
    but getting access to the metadata.
    It is also possible to leverage Dask computation distribution.
    """
    if Path(file_path).exists():
        return rxr.open_rasterio(file_path).squeeze()
    else:
        raise ValueError(f"Specified file does not exist at: {file_path}")


def read_geotiff_as_da_and_clip(
    file_path: str,
    box: Tuple[float, float, float, float],
) -> xr.DataArray:
    """Read a Geotiff file as a xarray DataArray and clip it.

    Instead of returning the full spatial extent of the array contained in the Geotiff file,
    only the information contained within the bounding box is returned.
    """
    da = read_geotiff_as_da(file_path)
    return da.rio.clip_box(minx=box[0], miny=box[1], maxx=box[2], maxy=box[3])
