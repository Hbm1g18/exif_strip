from PIL import Image, ExifTags
import os
import csv
import argparse

def dms_to_decimal(degrees, minutes, seconds):
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    return decimal_degrees

def main():

    parser = argparse.ArgumentParser(description="Generates an exif CSV for GPS data from a folder")
    
    parser.add_argument('--i', help="Input folder path", required=True)
    parser.add_argument('--o', help="Output folder path", required=True)


    args = parser.parse_args()

    image_folder = args.i

    output_csv = os.path.join(args.o, 'gps_data.csv')

    extensions = ('.jpeg', '.jpg', '.tif', '.tiff')

    gps_tag = 34853


    with open(output_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Image', 'Latitude', 'Longitude', 'Altitude', 'Direction', 'Time'])

        for file in os.listdir(image_folder):
            if file.lower().endswith(extensions):
                image_path = os.path.join(image_folder, file)
                image = Image.open(image_path)
                exif_data = image._getexif()

                if exif_data is not None:
                        if gps_tag in exif_data:
                            gps_info = exif_data[gps_tag]

                            latitude = gps_info[2]
                            latitude_ref = gps_info[1]
                            longitude = gps_info[4]
                            longitude_ref = gps_info[3]
                            altitude = gps_info[6]

                            if 17 in gps_info:
                                direction = gps_info[17]
                            else:
                                direction = ' '

                            if type(latitude) == tuple:  
                                degrees, minutes, seconds = latitude
                                latitude = dms_to_decimal(degrees, minutes, seconds)
                                if latitude_ref.upper() == 'S':
                                    latitude = -latitude
                                degrees, minutes, seconds = longitude
                                longitude = dms_to_decimal(degrees, minutes, seconds)
                                if longitude_ref.upper() == 'W':
                                    longitude = -longitude
                            
                            csv_writer.writerow([file, latitude, longitude, altitude, direction, exif_data[306]])    

                        else:
                            print(f"GPS info not found in {image_path}")


            else:
                continue

if __name__ == "__main__":
    main()