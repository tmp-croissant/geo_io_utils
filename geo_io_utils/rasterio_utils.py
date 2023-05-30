from collections import UserDict
from pathlib import Path
from typing import Tuple

import rasterio
from affine import Affine
from numpy.typing import NDArray
from rasterio.enums import Resampling


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
    """Save classic Geotiff"""
    Path(file_path).mkdir(parents=True, exist_ok=True)
    with rasterio.open(file_path, "w", **profile) as dst:
        dst.write(array, 1)


def save_cog(array: NDArray, file_path: str, profile: UserDict) -> None:
    """Save Cloud Optimized Geotiff.

    Save a classic geotiff and then build the overviews to create a COG.
    """
    profile.update(
        {
            "interleave": "pixel",
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "deflate",
        }
    )
    save_geotiff(array, file_path, profile)
    with rasterio.open(file_path, "r+") as dst:
        dst.build_overviews([2, 4, 8, 16], Resampling.average)
        dst.update_tags(ns="rio_overview", resampling="average")


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
    """Create a profile dictionary (extended metadata).

    The profile contains the metadata describing the geographic properties of an array
    and some parameters controlling the way it will be saved as a file.
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


def create_transform(lon_min: float, lat_max: float, resolution: float) -> Affine:
    """Create transform for an Array"""
    return Affine(resolution, 0.0, lon_min, 0.0, resolution, lat_max)
