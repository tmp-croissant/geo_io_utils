from collections import UserDict
from pathlib import Path
from typing import Tuple

import rasterio
from affine import Affine
from numpy.typing import NDArray


def read_geotiff(file_path: str) -> NDArray:
    if Path(file_path).exists():
        with rasterio.open(file_path, "r") as src:
            array = src.read(src)
        return array
    else:
        raise ValueError(f"Specified file does not exist at: {file_path}")


def read_geotiff_with_profile(file_path: str) -> Tuple[NDArray, UserDict]:
    if Path(file_path).exists():
        with rasterio.open(file_path, "r") as src:
            array = src.read(src)
            profile = src.profile
        return array, profile
    else:
        raise ValueError(f"Specified file does not exist at: {file_path}")


def save_geotiff(array: NDArray, file_path: str, profile: UserDict) -> None:
    Path(file_path).mkdir(parents=True, exist_ok=True)
    with rasterio.open(file_path, "w", **profile) as dst:
        dst.write(array)


def create_geotiff_profile(
    width: int,
    height: int,
    transform: Affine,
    driver: str = "Gtiff",
    nodata: float = -9999.0,
    dtype: str = "float32",
    count: int = 1,
    crs: str = "EPSG:4326",
    tiled: bool = True,
    interleave: str = "band",
    compress: str = "deflate",
) -> UserDict:
    """Create a profile dict containing the metadata describing the geographic
    properties of an array.
    """
    return UserDict(
        {
            "width": width,
            "height": height,
            "nodata": nodata,
            "transform": transform,
            "driver": driver,
            "dtype": dtype,
            "count": count,
            "crs": crs,
            "tiled": tiled,
            "interleave": interleave,
            "compress": compress,
        }
    )


def create_geotransform(lon_min: float, lat_max: float, resolution: float) -> Affine:
    return Affine(resolution, 0.0, lon_min, 0.0, resolution, lat_max)
