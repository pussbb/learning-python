'''


@author: pussbb
'''


from ..models.language import Language
from . import Command

"""
  Get User
"""

class Languages(Command):
    URI = 'languages'
    ALLOWED_METHODS = ['GET']
    TABLE = Language

# 
#     def delete(self, pk): 
#         self.not_allowed()
# 
#     def post(self): 
#         self.not_allowed()
# 
#     def put(self, pk): 
#         self.not_allowed()
