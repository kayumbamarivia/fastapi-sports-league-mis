import json
from sqlalchemy.orm import Session
from faker import Faker
from models.users import Users
from models.teams import Teams
from config.database import get_db, engine

# Initialize Faker
fake = Faker()

# Define constants
NUM_USERS = 500000
NUM_TEAMS = 500000

# # Generate random users
# def generate_users(num):
#     for _ in range(num):
#         yield Users(
#             name=fake.name(),
#             email=fake.unique.email(),
#             hashed_password=fake.password(),
#             role=fake.random_element(elements=("player", "coach", "admin")),
#             image_url=fake.image_url()
#         )

# Generate random teams
def generate_teams(num, user_ids):
    for _ in range(num):
        yield Teams(
            name=fake.unique.company(),
            coach=fake.name(),
            players=json.dumps([fake.name() for _ in range(fake.random_int(min=5, max=15))]),
            user_id=fake.random_element(elements=user_ids)
        )

def bulk_insert():
    with Session(engine) as session:
        # Bulk insert users
        # print("Inserting users...")
        # users = list(generate_users(NUM_USERS))
        # session.bulk_save_objects(users)
        # session.commit()
        # print("Users inserted successfully.")

        # Retrieve user IDs for assigning teams
        user_ids = [id for id in range(1,500000)]

        # Bulk insert teams
        print("Inserting teams...")
        teams = list(generate_teams(NUM_TEAMS, user_ids))
        session.bulk_save_objects(teams)
        session.commit()
        print("Teams inserted successfully.")

if __name__ == "__main__":
    bulk_insert()