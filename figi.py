import unittest
from stdnum import figi

class MyFigi:

    # Map letters to numbers: A=10, B=11, ..., Z=35
    @classmethod
    def char_to_num(cls,c: str) -> int:
        if c.isdigit():
            return int(c)
        return ord(c.upper()) - ord('A') + 10

    @classmethod
    def calc_check_digit(cls,figi: str) -> int:
        if len(figi) < 11:
            raise ValueError("FIGI must be at least 11 characters long")
        figi_11 = figi[:11]  # First 11 characters
        digits = ''.join([str(cls.char_to_num(c) * (1,2)[i % 2]) for i,c in enumerate(figi_11)])
        total = sum(int(d) for d in digits)
        return (10 - total) % 10

    @classmethod
    def validate_figi(cls, figi_id: str, use_stdnum: bool = False) -> bool:
        """
        Validates a Financial Instrument Global Identifier (FIGI).
        Returns True if valid, False otherwise.
        """
        if use_stdnum:
            return figi.is_valid(figi_id)

        if len(figi_id) != 12:
            return False

        figi_id = figi_id.upper()
        if not all(c.isalnum() for c in figi_id):
            return False

        check_digit = cls.calc_check_digit(figi_id)
        # print(f"Calculated check digit: {check_digit}, FIGI check digit: {figi_id[-1]}")
        return str(check_digit) == figi_id[-1]

class TestValidateFIGI(unittest.TestCase):
    use_stdnum = False  # Set to True to use stdnum validation
    
    def test_valid_figi(self):
        # Valid FIGI examples (from Bloomberg documentation)
        self.assertTrue(MyFigi.validate_figi("BBG000BLNNH6", use_stdnum=self.use_stdnum))
        self.assertTrue(MyFigi.validate_figi("BBG000C3Q974", use_stdnum=self.use_stdnum))
        self.assertTrue(MyFigi.validate_figi("BBG000CL9VN6", use_stdnum=self.use_stdnum))
        # self.assertTrue(True)

    def test_invalid_length(self):
        self.assertFalse(MyFigi.validate_figi("BBG000BLNNH", use_stdnum=self.use_stdnum))  # 11 chars
        self.assertFalse(MyFigi.validate_figi("BBG000BLNNH66", use_stdnum=self.use_stdnum))  # 13 chars

    def test_invalid_characters(self):
        self.assertFalse(MyFigi.validate_figi("BBG000BLN*H6", use_stdnum=self.use_stdnum))  # Invalid character
        self.assertFalse(MyFigi.validate_figi("BBG000BLNNH!", use_stdnum=self.use_stdnum))  # Invalid character

    def test_invalid_check_digit(self):
        self.assertFalse(MyFigi.validate_figi("BBG000BLNNH0", use_stdnum=self.use_stdnum))  # Wrong check digit
        self.assertFalse(MyFigi.validate_figi("BBG000C3Q970", use_stdnum=self.use_stdnum))  # Wrong check digit

if __name__ == "__main__":
    unittest.main()

