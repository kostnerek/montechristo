#from tests.TestUser import TestUserResource
#from models.User.UserModel import UserModel

#from tests.TestUser import TestUserResource
#unittest.main()
#from test.TestUserResource import TestUserRes
import unittest
import test.TestUserResource

suite = unittest.TestLoader().loadTestsFromModule(test.TestUserResource)
unittest.defaultTestLoader.sortTestMethodsUsing = lambda *args: -1
unittest.TextTestRunner(verbosity=3).run(suite)
#unittest.main()