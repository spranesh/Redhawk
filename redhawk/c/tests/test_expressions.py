#!/usr/bin/env python

""" Test Expressions """

import test_utils

def GetNthExpressionInFirstFunction(n, filename="expressions.c"):
  t = test_utils.SetUp("expressions.c")
  return test_utils.ConvertTree(t.children()[0].body.block_items[n-1])

def TestExpression1():
  """ Test 2 + 3 * 5; """
  return GetNthExpressionInFirstFunction(1)

def TestExpression2():
  """ Test a + b * c; """
  return GetNthExpressionInFirstFunction(2)

def TestExpression3():
  """ Test a << 2; """
  return GetNthExpressionInFirstFunction(3)

def TestExpression4():
  """ Test (a - 2) * (b + c) / d; """ 
  return GetNthExpressionInFirstFunction(4)

def TestExpression5():
  """ Test a%b; """
  return GetNthExpressionInFirstFunction(5)

def TestExpression6():
  """ Test (c >> 3) * d;"""
  return GetNthExpressionInFirstFunction(6)

def TestExpression7():
  """ Test (a | b) ^ (c & d);"""
  return GetNthExpressionInFirstFunction(7)

def TestExpression8():
  """ Test (a && b) || (c && d);"""
  return GetNthExpressionInFirstFunction(8)

def TestExpression9():
  """ Test (a < b) && (c <= d) || (e > f) && (g > h);"""
  return GetNthExpressionInFirstFunction(9)

def TestExpression10():
  """ Test a == b;"""
  return GetNthExpressionInFirstFunction(10)

def TestExpression11():
  """ Test a != b; """
  return GetNthExpressionInFirstFunction(11)
