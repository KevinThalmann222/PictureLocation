import PIL.Image
import PIL.ExifTags
import gmplot
import webbrowser
from geopy.geocoders import Nominatim
from pathlib import Path


class PictureLocation:
    def __init__(self, picture: str) -> None:
        """_summary_

        Args:
            picture (str): _description_
        """
        self.latitude_coor_dg = None
        self.longitude_coor_dg = None

        self.picture = Path(picture)
        img = PIL.Image.open(str(self.picture))
        exif = {PIL.ExifTags.TAGS[key]: value for key, value in img._getexif().items() if key in PIL.ExifTags.TAGS}
        self.coordinations = exif.get("GPSInfo")
        self.html_name = self.picture.stem + ".html"

    def __del_html(self) -> None:
        """_summary_"""
        html_path = self.picture.parent / self.html_name
        html_path.unlink()

    def get_coordinaten(self, coor="dg") -> tuple:
        """_summary_

        Args:
            coor (str, optional): _description_. Defaults to "dg".

        Raises:
            RuntimeError: _description_

        Returns:
            _type_: _description_
        """
        latitude_directory = self.coordinations[1]
        longitude_directory = self.coordinations[3]

        latitude_coor_gms = self.coordinations[2]
        longitude_coor_gms = self.coordinations[4]

        self.latitude_coor_dg = (int(latitude_coor_gms[2]) / 60 + int(latitude_coor_gms[1])) / 60 + int(latitude_coor_gms[0])
        self.longitude_coor_dg = (int(longitude_coor_gms[2]) / 60 + int(longitude_coor_gms[1])) / 60 + int(longitude_coor_gms[0])

        if latitude_directory == "S":
            self.latitude_coor_dg *= -1
        if longitude_directory == "W":
            self.longitude_coor_dg *= -1

        if coor == "dg":
            return (self.latitude_coor_dg, self.longitude_coor_dg)
        elif coor == "gms":
            return (latitude_coor_gms, longitude_coor_gms)
        else:
            raise RuntimeError("Please choose dg (Dezimalgrad) or gms (Grad, Minuten, Sekunden)")

    def get_address(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        if not self.latitude_coor_dg or not self.longitude_coor_dg:
            self.latitude_coor_dg, self.longitude_coor_dg = self.get_coordinaten(coor="dg")
        geo_loc = Nominatim(user_agent="GetLoc")
        loc_name = geo_loc.reverse(f"{self.latitude_coor_dg}, {self.longitude_coor_dg}").address
        print(f"the location of the picture '{self.picture.name}' is:")
        print(f"         --> {loc_name}")

        return loc_name

    def creat_map(self, openbrowser=True, zoom=15):
        """_summary_

        Args:
            openbrowser (bool, optional): _description_. Defaults to True.
            zoom (int, optional): _description_. Defaults to 15.
        """
        if not self.latitude_coor_dg or not self.longitude_coor_dg:
            self.latitude_coor_dg, self.longitude_coor_dg = self.get_coordinaten(coor="dg")
        gmap = gmplot.gmplot.GoogleMapPlotter(self.latitude_coor_dg, self.longitude_coor_dg, zoom)
        gmap.marker(self.latitude_coor_dg, self.longitude_coor_dg, "cornflowerblue")
        gmap.draw(self.html_name)
        if openbrowser:
            webbrowser.open(self.html_name, new=2)


def get_pic_path() -> str:
    """_summary_

    Yields:
        _type_: _description_
    """
    for path in Path(__file__).parent.iterdir():
        if path.suffix.lower() in [".jpg", ".jpeg", ".gif", ".png", ".tiff", ".raw", ".psd"]:
            yield path


if __name__ == "__main__":
    for pic_path in get_pic_path():
        Picture_location = PictureLocation(pic_path)
        Picture_location.get_address()
        Picture_location.creat_map()
