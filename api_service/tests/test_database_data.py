from api.models import UserRequestHistory
from faker import Faker
from faker.providers import BaseProvider, date_time, company

from tests.test_base_user import GenerateNewRandomSuperUserTestCase


class GenerateDatabaseEntriesTestCase(GenerateNewRandomSuperUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        faker = Faker()
        Faker.seed(0)
        for _ in range(30):
            date = faker.date_time()
            name = faker.company()
            symbol = faker.random_choices(
                elements=("AAPL.US", "A.US", "AAC.US", "AAMC.US", "AAME.US", "AAMX.BR"),
                length=1,
            )[0]
            open = faker.numerify(text="%%%.##")
            high = faker.numerify(text="%%%.##")
            low = faker.numerify(text="%%%.##")
            close = faker.numerify(text="%%%.##")
            user = self.user
            self.db = UserRequestHistory.objects.create(
                date=date,
                name=name,
                symbol=symbol,
                open=open,
                high=high,
                low=low,
                close=close,
                user=user,
            )

    def tearDown(self) -> None:
        UserRequestHistory.objects.all().delete()
        super().tearDown()
