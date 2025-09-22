import argparse
import random
import string
import sys
import time

import requests

from app.core.log import logger

# Configuration
BASE_URL = "http://127.0.0.1:8000"
USERS_ENDPOINT = "/api/users"
ITEMS_ENDPOINT = "/api/items"
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

###############
#    Users    #
###############

FIRST_NAMES = [
    "James",
    "Mary",
    "John",
    "Patricia",
    "Robert",
    "Jennifer",
    "Michael",
    "Linda",
    "William",
    "Elizabeth",
    "David",
    "Barbara",
    "Richard",
    "Susan",
    "Joseph",
    "Jessica",
    "Thomas",
    "Sarah",
    "Christopher",
    "Karen",
    "Charles",
    "Nancy",
    "Daniel",
    "Lisa",
    "Matthew",
    "Betty",
    "Anthony",
    "Helen",
    "Mark",
    "Sandra",
    "Donald",
    "Donna",
    "Steven",
    "Carol",
    "Paul",
    "Ruth",
    "Andrew",
    "Sharon",
    "Joshua",
    "Michelle",
    "Kenneth",
    "Laura",
    "Kevin",
    "Sarah",
    "Brian",
    "Kimberly",
    "George",
    "Deborah",
    "Timothy",
    "Dorothy",
    "Ronald",
    "Lisa",
    "Jason",
    "Nancy",
    "Edward",
    "Karen",
    "Jeffrey",
    "Betty",
    "Ryan",
    "Helen",
    "Jacob",
    "Sandra",
    "Gary",
    "Donna",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
    "Gomez",
    "Phillips",
    "Evans",
    "Turner",
    "Diaz",
]

EMAIL_DOMAINS = [
    "example.com",
    "test.com",
    "demo.org",
    "sample.net",
    "fake.io",
    "placeholder.com",
    "mock.org",
    "dummy.net",
    "temp.com",
    "local.dev",
]

ROLES = ["USER", "ADMIN"]


def generate_fake_user() -> dict[str, str]:
    """Generate a fake user with random data."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    # Create email from name
    email_prefix = f"{first_name.lower()}.{last_name.lower()}"
    domain = random.choice(EMAIL_DOMAINS)
    email = f"{email_prefix}@{domain}"

    # Add random number to email to avoid duplicates
    email = f"{email_prefix}{random.randint(1, 999)}@{domain}"

    role = random.choice(ROLES)

    return {"first_name": first_name, "last_name": last_name, "email": email, "role": role}


def send_user_request(user_data: dict[str, str]) -> requests.Response:
    """Send POST request to create a user."""
    url = f"{BASE_URL}{USERS_ENDPOINT}"

    try:
        return requests.post(url, headers=HEADERS, json=user_data, timeout=10)

    except requests.exceptions.RequestException as e:
        logger.info(f"Error sending request: {e}")
        return None


def create_fake_users(count: int, delay: float = 0.1) -> None:
    """Create multiple fake users.

    Args:
        count: Number of users to create
        delay: Delay between requests in seconds (to avoid overwhelming the server)
    """
    successful = 0
    failed = 0

    logger.info(f"Creating {count} fake users...")
    logger.info(f"Target URL: {BASE_URL}{USERS_ENDPOINT}")
    logger.info("-" * 50)

    for i in range(count):
        user_data = generate_fake_user()

        logger.info(f"[{i + 1}/{count}] Creating user: {user_data['email']}")

        response = send_user_request(user_data)

        if response is not None:
            if response.status_code in [200, 201]:
                logger.info(f"Success: {response.status_code}")
                successful += 1
            else:
                logger.info(f"Failed: {response.status_code} - {response.text}")
                failed += 1
        else:
            logger.info("Failed: Request error")
            failed += 1

        # Add delay between requests
        if delay > 0 and i < count - 1:
            time.sleep(delay)

    logger.info("-" * 50)
    logger.info("Summary:")
    logger.info(f"> Successful: {successful}")
    logger.info(f"> Failed: {failed}")
    logger.info(f"> Total: {successful + failed}")


###############
#    Items    #
###############


LAPTOP_BRANDS = ["Lenovo", "Dell", "HP", "ASUS", "Acer", "MacBook", "MSI", "Razer"]
LAPTOP_MODELS = {
    "Lenovo": ["ThinkPad X1", "ThinkPad T14", "ThinkPad P1", "IdeaPad 5", "Legion 5"],
    "Dell": ["XPS 13", "XPS 15", "Latitude 7420", "Inspiron 15", "Precision 5560"],
    "HP": ["EliteBook 840", "Pavilion 15", "Spectre x360", "ProBook 450", "Envy 13"],
    "ASUS": ["ZenBook 14", "VivoBook S15", "ROG Strix", "ExpertBook B9", "TUF Gaming"],
    "Acer": ["Aspire 5", "Swift 3", "Predator Helios", "TravelMate P2", "Spin 3"],
    "MacBook": ["Air M2", "Pro 14", "Pro 16", "Air M1", "Pro 13"],
    "MSI": ["Modern 14", "Creator Z16", "GF63 Thin", "Prestige 14", "Summit E13"],
    "Razer": ["Blade 14", "Blade 15", "Book 13", "Blade Stealth", "Blade Pro 17"],
}

DESKTOP_BRANDS = ["Dell", "HP", "Lenovo", "ASUS", "Custom Build"]
DESKTOP_MODELS = {
    "Dell": ["OptiPlex 7090", "Precision 3650", "Inspiron 3880", "XPS 8950", "Vostro 3681"],
    "HP": ["EliteDesk 800", "Pavilion Desktop", "OMEN 45L", "ProDesk 400", "Z2 Mini"],
    "Lenovo": ["ThinkCentre M75q", "IdeaCentre 5", "Legion Tower 5", "ThinkStation P340", "M720q"],
    "ASUS": ["ExpertCenter D5", "Mini PC PN50", "ROG Strix GT15", "VivoPC X", "ProArt Station"],
    "Custom Build": ["Workstation Pro", "Gaming Rig", "Office PC", "Dev Machine", "Media Center"],
}

MONITOR_BRANDS = ["Dell", "LG", "Samsung", "ASUS", "HP", "Acer", "BenQ"]
MONITOR_MODELS = {
    "Dell": ["UltraSharp U2720Q", "S2721DS", "P2414H", "U3821DW", "S3221QS"],
    "LG": ["27UP850", "34WP65C", "24MK430H", "32UN650", "27GL850"],
    "Samsung": ["Odyssey G7", "M7 32", "CF390", "CRG9", "F24T450FQN"],
    "ASUS": [
        "ProArt PA278QV",
        "TUF Gaming VG27AQ",
        "VA24EHE",
        "ROG Swift PG279Q",
        "ZenScreen MB16AC",
    ],
    "HP": ["E24 G5", "Z27", "V24i", "X32c", "E27m G4"],
    "Acer": ["Nitro XV272U", "CB242Y", "Predator X27", "SB220Q", "K272HUL"],
    "BenQ": ["SW271", "EX2780Q", "GW2480", "PD3200U", "ZOWIE XL2411K"],
}

CATEGORIES = {
    "Laptop": (LAPTOP_BRANDS, LAPTOP_MODELS),
    "Desktop": (DESKTOP_BRANDS, DESKTOP_MODELS),
    "Monitor": (MONITOR_BRANDS, MONITOR_MODELS),
}

# Other equipment categories
OTHER_ITEMS = {
    "Mouse": [
        "Logitech MX Master 3",
        "Razer DeathAdder V3",
        "Microsoft Surface Mouse",
        "Apple Magic Mouse",
        "HP X3000",
    ],
    "Keyboard": [
        "Logitech MX Keys",
        "Apple Magic Keyboard",
        "Dell KB216",
        "HP 125",
        "Microsoft Wired 600",
    ],
    "Headset": [
        "Logitech H390",
        "Jabra Evolve 40",
        "SteelSeries Arctis 7",
        "HyperX Cloud II",
        "Sennheiser SC 160",
    ],
    "Webcam": [
        "Logitech C920",
        "Microsoft LifeCam HD-3000",
        "Razer Kiyo",
        "Logitech Brio",
        "Creative Live! Cam",
    ],
    "Printer": [
        "HP LaserJet Pro",
        "Canon PIXMA",
        "Epson EcoTank",
        "Brother HL-L2350DW",
        "HP DeskJet 3755",
    ],
    "Router": [
        "Cisco Meraki MR36",
        "Ubiquiti Dream Machine",
        "ASUS AX6000",
        "Netgear Nighthawk",
        "TP-Link Archer",
    ],
    "Switch": [
        "Cisco SG350-28",
        "Netgear GS108",
        "TP-Link TL-SG1016D",
        "D-Link DGS-1100-24",
        "Ubiquiti UniFi",
    ],
    "Phone": [
        "Cisco IP Phone 8861",
        "Yealink T46S",
        "Poly VVX 411",
        "Grandstream GRP2613",
        "Avaya J169",
    ],
}

# Location codes (building-room format)
BUILDINGS = ["GD", "AD", "RD", "IT", "HR", "FN", "MK", "SL"]
ROOM_RANGES = {
    "GD": range(1, 100),  # General offices
    "AD": range(1, 50),  # Administration
    "RD": range(1, 30),  # R&D
    "IT": range(1, 25),  # IT Department
    "HR": range(1, 20),  # Human Resources
    "FN": range(1, 15),  # Finance
    "MK": range(1, 35),  # Marketing
    "SL": range(1, 60),  # Sales
}


def generate_serial_number() -> str:
    """Generate a fake serial number in format ABC-123-XYZ."""
    part1 = "".join(random.choices(string.ascii_uppercase, k=3))
    part2 = "".join(random.choices(string.digits, k=3))
    part3 = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{part1}-{part2}-{part3}"


def generate_location() -> str:
    """Generate a fake location code."""
    building = random.choice(BUILDINGS)
    room = random.choice(list(ROOM_RANGES[building]))
    return f"{building}-{room:04d}"


def get_existing_users() -> list[dict]:
    """Fetch existing users from the API."""
    url = f"{BASE_URL}{USERS_ENDPOINT}"

    try:
        response = requests.get(url, headers={"accept": "application/json"}, timeout=10)
        if response.status_code == 200:  # noqa: PLR2004
            data = response.json()
            users = data.get("users", [])
            logger.info(f"Found {len(users)} existing users")
            return users

        logger.info(f"Failed to fetch users: {response.status_code}")
        return []  # noqa: TRY300
    except requests.exceptions.RequestException as e:
        logger.info(f"Error fetching users: {e}")
        return []


def generate_fake_item(users: list[dict]) -> dict[str, str] | None:
    """Generate a fake IT item with random data."""
    if not users:
        logger.info("No users available for item assignment!")
        return None

    # Choose category and generate appropriate item
    if random.random() < 0.7:  # 70% chance for main categories  # noqa: PLR2004
        category = random.choice(list(CATEGORIES.keys()))
        brands, models = CATEGORIES[category]
        brand = random.choice(brands)
        model = random.choice(models[brand])
        name = f"{brand} {model}"
    else:  # 30% chance for other items
        category = random.choice(list(OTHER_ITEMS.keys()))
        name = random.choice(OTHER_ITEMS[category])

    # Select random owner
    owner = random.choice(users)
    owner_email = owner["email"]

    return {
        "name": name,
        "category": category,
        "serial_number_1": generate_serial_number(),
        "serial_number_2": generate_serial_number() if random.random() < 0.3 else None,  # noqa: PLR2004
        "serial_number_3": generate_serial_number() if random.random() < 0.1 else None,  # noqa: PLR2004
        "owner": owner_email,
        "location": generate_location(),
    }


def send_item_request(item_data: dict[str, str]) -> requests.Response:
    """Send POST request to create an item."""
    url = f"{BASE_URL}{ITEMS_ENDPOINT}"

    try:
        return requests.post(url, headers=HEADERS, json=item_data, timeout=10)

    except requests.exceptions.RequestException as e:
        logger.info(f"Error sending request: {e}")
        return None


def create_fake_items(count: int, delay: float = 0.1) -> None:
    """Create multiple fake IT items.

    Args:
        count: Number of items to create
        delay: Delay between requests in seconds
    """
    users = get_existing_users()
    if not users:
        logger.info("Cannot create items without existing users. Please create some users first.")
        return

    successful = 0
    failed = 0

    logger.info(f"\nCreating {count} fake IT items...")
    logger.info(f"Target URL: {BASE_URL}{ITEMS_ENDPOINT}")
    logger.info(f"Available users: {len(users)}")
    logger.info("-" * 60)

    for i in range(count):
        item_data = generate_fake_item(users)

        if item_data is None:
            logger.info(f"[{i + 1}/{count}] Failed to generate item data")
            failed += 1
            continue

        logger.info(f"[{i + 1}/{count}] Creating: {item_data['name']}")

        response = send_item_request(item_data)

        if response is not None:
            if response.status_code in [200, 201]:
                logger.info(
                    f"Success: {response.status_code} | Location: {item_data['location']}",
                )
                successful += 1
            else:
                logger.info(f"Failed: {response.status_code} - {response.text}")
                failed += 1
        else:
            logger.info("Failed: Request error")
            failed += 1

        # Add delay between requests
        if delay > 0 and i < count - 1:
            time.sleep(delay)

    logger.info("-" * 60)
    logger.info("Summary:")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Total: {successful + failed}")


def get_existing_items() -> list[dict]:
    """Fetch existing items from the API."""
    url = f"{BASE_URL}{ITEMS_ENDPOINT}"

    try:
        response = requests.get(url, headers={"accept": "application/json"}, timeout=10)
        if response.status_code == 200:  # noqa: PLR2004
            data = response.json()
            items = data.get("items", [])
            logger.info(f"Found {len(items)} existing items")
            return items

        logger.info(f"Failed to fetch items: {response.status_code}")
        return []  # noqa: TRY300
    except requests.exceptions.RequestException as e:
        logger.info(f"Error fetching items: {e}")
        return []


def show_statistics(users: list[dict]) -> None:
    """Show some statistics about what will be generated."""
    total_categories = len(CATEGORIES) + len(OTHER_ITEMS)
    total_brands = sum(len(brands) for brands, _ in CATEGORIES.values())
    total_locations = sum(len(rooms) for rooms in ROOM_RANGES.values())

    logger.info("Generation Statistics:")
    logger.info(f"- Available users: {len(users)}")
    logger.info(f"- Item categories: {total_categories}")
    logger.info(f"- Equipment brands: {total_brands}")
    logger.info(f"- Possible locations: {total_locations}")
    logger.info(f"- Buildings: {', '.join(BUILDINGS)}")


def flush_database(delay: float = 0.1) -> None:
    """Flush the database by deleting all users and items."""
    logger.info("Flushing database...")
    users = get_existing_users()
    items = get_existing_items()

    user_emails = [user["email"] for user in users]
    item_ids = [item["id"] for item in items]

    items_cnt, users_cnt = 0, 0

    url = f"{BASE_URL}{ITEMS_ENDPOINT}"
    for i, item_id in enumerate(item_ids):
        response = requests.delete(f"{url}/{item_id}", timeout=10)
        if response.status_code not in [200, 204]:
            logger.error(f"Failed to delete item {item_id}")
        else:
            items_cnt += 1

        if delay > 0 and i < len(item_ids) - 1:
            time.sleep(delay)

    url = f"{BASE_URL}{USERS_ENDPOINT}"
    for i, user_email in enumerate(user_emails):
        response = requests.delete(f"{url}/{user_email}", timeout=10)
        if response.status_code not in [200, 204]:
            logger.error(f"Failed to delete user {user_email}")
        else:
            users_cnt += 1

        if delay > 0 and i < len(user_emails) - 1:
            time.sleep(delay)

    logger.info(f"Deleted {users_cnt} users and {items_cnt} items")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--flush", action="store_true", help="Delete all existing data")
    parser.add_argument("--users", type=int, default=10, help="Number of fake users to create")
    parser.add_argument("--items", type=int, default=100, help="Number of fake items to create")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between requests")
    args = parser.parse_args()

    if args.flush:
        flush_database()
        sys.exit()

    create_fake_users(count=args.users, delay=args.delay)

    logger.info("Checking for existing users...")
    users = get_existing_users()

    if not users:
        logger.info("No users found in the database!")
        sys.exit()

    show_statistics(users)

    create_fake_items(count=args.items, delay=args.delay)
