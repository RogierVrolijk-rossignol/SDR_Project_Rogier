"""
This python file...
stores all the ata chapters to eventually b e displayed into the gui.py. 
ATA chapters data is being fetched from 'https://en.wikipedia.org/wiki/ATA_100'. 
"""

ata_chapters = {
    "21": "Air Conditioning",
    "22": "Auto Flight",
    "23": "Communications",
    "24": "Electrical Power",
    "25": "Equipment / Furnishings",
    "26": "Fire Protection",
    "27": "Flight Controls",
    "28": "Fuel",
    "29": "Hydraulic Power",
    "30": "Ice and Rain Protection",
    "31": "Indicating / Recording Systems",
    "32": "Landing Gear",
    "33": "Lights",
    "34": "Navigation",
    "35": "Oxygen",
    "36": "Pneumatic",
    "49": "Airborne Auxiliary Power",
    "52": "Doors",
    "53": "Fuselage",
    "54": "Nacelles / Pylons",
    "55": "Stabilizers",
    "56": "Windows",
    "57": "Wings",
    "71": "Powerplant",
    "72": "Engine",
    "73": "Engine Fuel and Control",
    "74": "Ignition",
    "75": "Air",
    "76": "Engine Controls",
    "77": "Engine Indicating",
    "78": "Exhaust",
    "79": "Oil",
    "80": "Starting",
}


def get_ata_chapters():
    # Returns the ATA chapter dictionary.
    return ata_chapters