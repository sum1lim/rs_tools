from setuptools import setup

__version__ = (0, 0, 1)

setup(
    name="rs_tools",
    description="Remote Sensing Tools",
    version=".".join(str(d) for d in __version__),
    author="Sangwon Lim",
    author_email="sangwonl@uvic.ca",
    packages=["rs_tools"],
    include_package_data=True,
    scripts="""
        ./scripts/RGB_merge
        ./scripts/RGB_extract
        ./scripts/K_Means
        ./scripts/NDVI
        ./scripts/SOBEL
        ./scripts/ROI
        ./scripts/gaussian
        ./scripts/contrast
    """.split(),
)
