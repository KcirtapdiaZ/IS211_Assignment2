import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading data: {e}")
        exit(1)

def setup_logger():
    logger = logging.getLogger('assignment2')
    handler = logging.FileHandler('errors.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
    return logger

def processData(file_content):
    personData = {}
    logger = setup_logger()

    lines = file_content.strip().split('\n')
    for linenum, line in enumerate(lines, 1):
        fields = line.split(',')
        if len(fields) != 3:
            continue

        try:
            id = int(fields[0].strip())
            name = fields[1].strip()
            birthday_str = fields[2].strip()

            birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()

            personData[id] = (name, birthday)

        except ValueError:
            logger.error(f"Error processing line #{linenum} for ID #{fields[0].strip()}")

    return personData

def displayPerson(id, personData):

    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")



def main(url):
    print(f"Downloading data from {url}...")
    csvData = downloadData(url)

    print("Processing data...")
    personData = processData(csvData)

    while True:
        try:
            user_input = int(input("Enter an ID to lookup (0 to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, personData)

        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)