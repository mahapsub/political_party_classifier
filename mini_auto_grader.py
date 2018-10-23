import ID3, parse, random, unit_tests

def mini_grader():

  data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]

  try:
    tree = ID3.ID3(data, 0)
    if tree != None:
      ans = ID3.evaluate(tree, dict(a=1, b=0))
      if ans != 1:
        print("ID3 test 1 failed.")
      else:
        print("ID3 test 1 succeeded.")
    else:
      print("ID3 test 1 failed -- no tree returned")
  except Exception:
    print("ID3 test 1 failed runtime error")

  data = [dict(a=1, b=0, Class=0), dict(a=1, b=1, Class=1)]

  try:
    tree = ID3.ID3(data, 0)
    if tree != None:
      ans = ID3.evaluate(tree, dict(a=1, b=0))
      if ans != 0:
        print("ID3 test 2 failed.")
      else:
        print("ID3 test 2 succeeded.")
    else:
      print("ID3 test 2 failed -- no tree returned")
  except Exception:
    print("ID3 test 2 failed runtime error")


  data = [dict(a=1, b=0, Class=2), dict(a=1, b=1, Class=1),
          dict(a=2, b=0, Class=2), dict(a=2, b=1, Class=3),
          dict(a=3, b=0, Class=1), dict(a=3, b=1, Class=3)]

  try:
    tree = ID3.ID3(data, 0)
    if tree != None:
      ans = ID3.evaluate(tree, dict(a=1, b=0))
      if ans != 2:
        print("ID3 test 3-1 failed.")
      else:
        print("ID3 test 3-1 succeeded.")
      ans = ID3.evaluate(tree, dict(a=1, b=1))
      if ans != 1:
        print("ID3 test 3-2 failed.")
      else:
        print("ID3 test 3-2 succeeded.")
    else:
      print("ID3 test 3 failed -- no tree returned")
  except Exception:
    print("ID3 test 3 failed runtime error")

  data = [dict(a=1, b=0, c='?', Class=1), dict(a=1, b=3, c=2, Class=1),
         dict(a=2, b='?', c=1, Class=2), dict(a=2, b=1, c=3, Class=2),
         dict(a=3, b=0, c=1, Class=3), dict(a=3, b=2, c='?', Class=3)]

  try:
    tree = ID3.ID3(data, 0)
    if tree != None:
      ans = ID3.evaluate(tree, dict(a=1, b=1, c=1))
      if ans != 1:
        print("ID3 test 4-1 failed.")
      else:
        print("ID3 test 4-1 succeeded.")
      ans = ID3.evaluate(tree, dict(a=2, b=0, c=0))
      if ans != 2:
        print("ID3 test 4-2 failed.")
      else:
        print("ID3 test 4-2 succeeded.")
    else:
      print("ID3 test 4 failed -- no tree returned")
  except Exception:
    print("ID3 test 4 failed runtime error")

'''
data for custom tests from https://www.saedsayad.com/decision_tree.htm
'''
def custom_test():
  data = [dict(outlook='rainy', temp='hot', humidity = 'high', windy='false', Class='no'),
          dict(outlook='rainy', temp='hot', humidity='high', windy='true', Class='no'),
          dict(outlook='overcast', temp='hot', humidity='high', windy='false', Class='yes'),
          dict(outlook='sunny', temp='mild', humidity='high', windy='false', Class='yes'),
          dict(outlook='sunny', temp='cool', humidity='normal', windy='false', Class='yes'),
          dict(outlook='sunny', temp='cool', humidity='normal', windy='true', Class='no'),
          dict(outlook='overcast', temp='cool', humidity='normal', windy='true', Class='yes'),
          dict(outlook='rainy', temp='mild', humidity='high', windy='false', Class='no'),
          dict(outlook='rainy', temp='cool', humidity='normal', windy='false', Class='yes'),
          dict(outlook='sunny', temp='mild', humidity='normal', windy='false', Class='yes'),
          dict(outlook='rainy', temp='mild', humidity='normal', windy='true', Class='yes'),
          dict(outlook='overcast', temp='mild', humidity='high', windy='true', Class='yes'),
          dict(outlook='overcast', temp='hot', humidity='normal', windy='false', Class='yes'),
          dict(outlook='sunny', temp='mild', humidity='high', windy='true', Class='no')
          ]
  tree = ID3.ID3(data, 'no')
  if tree != None:
    if ID3.evaluate(tree, dict(outlook='sunny', temp='cool', humidity='normal', windy='true')) != 'no':
      print('test1 failed')
    elif ID3.evaluate(tree, dict(outlook='sunny', temp='cool', humidity='normal', windy='false')) != 'yes':
      print('test 2 failed')
    elif ID3.evaluate(tree, dict(outlook='overcast', temp='cool', humidity='normal', windy='false')) != 'yes':
      print('test 3 failed')
    elif ID3.evaluate(tree, dict(outlook='overcast', temp='cool', humidity='normal', windy='true')) != 'yes':
      print('test 4 failed')
    elif ID3.evaluate(tree, dict(outlook='rainy', temp='cool', humidity='normal', windy='false')) != 'yes':
      print('test 5 failed')
    elif ID3.evaluate(tree, dict(outlook='rainy', temp='cool', humidity='high', windy='false')) != 'no':
      print('test 6 failed')
    else:
      print('custom tests passed')

if __name__ == "__main__":
    # custom_test()
    mini_grader()
    # unit_tests.testID3AndEvaluate()
    # unit_tests.testID3AndTest()
    unit_tests.testPruning()
    # unit_tests.testPruningOnHouseData('house_votes_84.data')