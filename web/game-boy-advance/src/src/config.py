######## APPLICATION ########

DEBUG = False
HOST = '0.0.0.0'
PORT = 5000


######## PASSWORDS ##########

SALT = 'b42b1030758acbeddaec452d17a4c13ba1d06be1609880767b827021fc11542ba87a6fc5d239f915ad9319d699867e15d4040e180ca1e905c9e577218ef9775b'
PEPPER = '4d1d4d1a1a7fb9d39bb48c6429d56bccf55a7ba5802341ea165554f598679c01486410e10dffe1f91cf43df040598dc2cbcafa5b955cc2da651b185a516b9f5f'


######## DATABASES ##########

DATABASE_URI = "mysql+mysqldb://root:nTf8NV5d3H224gdJ@mariadb:3306/main_db"


######## JWT #########

# tokens expire after 15min
JWT_ACCESS_TOKEN_EXPIRES = 900

JWT_ALGORITHM = "HS256"

JWT_ERROR_MESSAGE_KEY = "error"

# refresh tokens expire after 48h
JWT_REFRESH_TOKEN_EXPIRES = 172_800

JWT_HEADER_NAME = "X-Access-Token"

JWT_HEADER_TYPE = ""