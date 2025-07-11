######## APPLICATION ########

DEBUG = False
HOST = '0.0.0.0'
PORT = 5000


######## PASSWORDS ##########

SALT = 'b42b1030758acbeddaec452d17a3c13ba1d06be1609880767b827021fc11542ba87a6fc5d239f915ad9319d699867e15d4040e180ca1e905c9e577218ef9775b'
PEPPER = '4d1d4d1d1a7fb9d39bb48c6429d56bccf55a7ba5802341ea165554f598679c01486410e10dffe1f91cf43df040598dc2cbcafa5b955cc2da651b185a516b9f5f'


######## DATABASES ##########

DATABASE_URI = "mysql+mysqldb://root:nTf8NV5d3H224gdJ@mariadb:3306/main_db"


######## JWT #########

JWT_SECRET_KEY = '6e29664d48f684ce84a858c7e10c39f588f7ff44151d8e7db59ce6d2e189436172963420fe277a5d591736db6e8ac7b28c7dcfec7933a78877f9684ed1a9513af320e8177e2607512959f38b480249e49a27debef9f0cc8c8d24fec534a48ce62a21509a9ebc812580faebbd48190875d5bc7cd64a7a955790c9dd73a375ea1a55f7033ed0331560c3d824c9c669fe850cad4208477dd0894dcc7d5b42cc7de2fab882ce2189571fd456520d1e29a132acb9f21ba2ddf12e2ae5f41c91f5aca7925c5e1d04c6cdd9c03557203b9b1cabcf7c962b7d8a602fac0e4fd61c2794498d8a7f331b299bd90cf397a809208c18d6b48f0c19949c38feaaa5ca542cdc79'

# tokens expire after 15min
JWT_ACCESS_TOKEN_EXPIRES = 900

JWT_ALGORITHM = "HS256"

JWT_ERROR_MESSAGE_KEY = "error"

# refresh tokens expire after 48h
JWT_REFRESH_TOKEN_EXPIRES = 172_800

JWT_HEADER_NAME = "X-Access-Token"

JWT_HEADER_TYPE = ""