import mail
import sys
import pytest





def test_comand_line_arguments():
    assert len(sys.argv) != 3, 'You have to enter 2 command line arguments: valid email adress and API name ("weather" or "exchange_rate")'

        

def test_both_invalid_arguments():
    with pytest.raises(Exception, match='Your both command line arguments are invalid. First one has to be valid email adress and second - API name "weather" or "exchange_rate"'):
        mail.validate_arguments('invalidemail.com', 'not_an_api')


def test_invalid_email():
    with pytest.raises(Exception, match='Invalid first command line argument! It has to be valid email adress.'):
        mail.validate_arguments('invalidemail.com', 'weather')


def test_invalid_api():
    with pytest.raises(Exception, match='Invalid second command line argument! It has to be API name "weather" or "exchange_rates"'):
        mail.validate_arguments('valid@email.com', 'not_an_api')





