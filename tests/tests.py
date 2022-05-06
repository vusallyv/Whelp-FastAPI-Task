import unittest
from db.db_user import create_user
from db.db_ip_address import create_ip_address
from db.hash import Hash
from schemas import UserBase


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.password = "123456"
        self.username = "test"
        self.email = "test@test.com"
        self.user = create_user(request=UserBase(
            username=self.username,
            email=self.email,
            password=Hash.bcrypt(self.password)
        ))
        return super().setUp()

    def test_create_user(self):
        case = create_user(request=UserBase(
            username="test",
            email="test@test.com",
            password=Hash.bcrypt("123456")
        ))
        self.assertEqual(case.email, "test@test.com")
        self.assertEqual(case.username, "test")
        self.assertEqual(Hash.bcrypt_verify(
            "123456", Hash.bcrypt("123456")), True)

    def test_create_ip_data(self):
        case = create_ip_address(response={
            "ip": "78.109.51.151",
            "is_eu": True,
            "city": "London",
            "region": "England",
            "region_code": "ENG",
            "country_name": "United Kingdom",
            "country_code": "GB",
            "continent_name": "Europe",
            "continent_code": "EU",
            "latitude": 51.5085,
            "longitude": -0.1257,
            "postal": "EC2A 4DB",
            "calling_code": "44",
            "flag": "https://lipis.github.io/flag-icon-css/flags/4x3/gb.svg"
        })
        self.assertEqual(case.ip, '78.109.51.151')
        self.assertEqual(case.is_eu, True)
        self.assertEqual(case.city, "London")
        self.assertEqual(case.region, "England")
        self.assertEqual(case.region_code, "ENG")
        self.assertEqual(case.country_name, "United Kingdom")
        self.assertEqual(case.country_code, "GB")
        self.assertEqual(case.continent_name, "Europe")
        self.assertEqual(case.continent_code, "EU")
        self.assertEqual(case.latitude, 51.5085)
        self.assertEqual(case.longitude, -0.1257)
        self.assertEqual(case.postal, "EC2A 4DB")
        self.assertEqual(case.calling_code, "44")
        self.assertEqual(
            case.flag, "https://lipis.github.io/flag-icon-css/flags/4x3/gb.svg")

    def tearDown(self) -> None:
        self.user.delete().execute()


if __name__ == "__main__":
    unittest.main()
