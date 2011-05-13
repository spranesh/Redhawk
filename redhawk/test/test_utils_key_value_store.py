#!/usr/bin/env python
import redhawk.utils.key_value_store as KV
import redhawk.scripts.script_util as S
import redhawk

import nose.tools

import glob
import os
import shelve
import sys
import tempfile

PREFIX = "redhawk-key-value-store-test"

""" Test the key value store module."""
def GetTempFile():
  return tempfile.mktemp(prefix=PREFIX)

def setUp():
  os.chdir(tempfile.gettempdir())
  return

def tearDown():
  for f in glob.glob(PREFIX + "*"):
    os.remove(f)
  return

@nose.tools.raises(AssertionError)
def TestCreateNewStoreOverExistingStore():
  temp_file = GetTempFile()
  fp = open(temp_file, 'w')
  fp.close()
  KV.CreateNewStore(temp_file, redhawk.GetVersion())

@nose.tools.raises(AssertionError)
def TestRemoveEmptyStore():
  temp_file = GetTempFile()
  KV.RemoveExistingStore(temp_file)

def TestCreateAndRemoveStores():
  temp_file = GetTempFile()
  KV.CreateNewStore(temp_file, redhawk.GetVersion())
  store = KV.KeyValueStore(temp_file, redhawk.GetVersion())
  assert(store.GetVersion() == redhawk.GetVersion())
  store.Close()
  KV.RemoveExistingStore(temp_file)
  assert(not os.path.exists(temp_file))

def TestIsValidStore():
  temp_file = GetTempFile()

  KV.CreateNewStore(temp_file, redhawk.GetVersion())
  assert(KV.IsValidStore(temp_file) == True)

  fp = open(temp_file, 'w')
  fp.close()
  assert(KV.IsValidStore(temp_file) == False)

def TestNiceInitKeyValueStore():
  temp_file = GetTempFile()

  KV.CreateNewStore(temp_file, redhawk.GetVersion())
  store = KV.KeyValueStore(temp_file, redhawk.GetVersion())
  return

@nose.tools.nottest
def TestBadVersionInitKeyValueStore():
  temp_file = GetTempFile()

  KV.CreateNewStore(temp_file, redhawk.GetVersion())
  store = shelve.open(temp_file, 'c')
  store[KV.VERSION_KEY] = '0.0.0'
  store = KV.KeyValueStore(temp_file, redhawk.GetVersion())
  return

class TestKeyValueStore:
  def setUp(self):
    setUp()
    self.temp_file = GetTempFile()
    KV.CreateNewStore(self.temp_file, redhawk.GetVersion())
    store = shelve.open(self.temp_file, 'c')
    store['dog'] = 'woof'
    store['cat'] = 'meow'
    store.close()

    self.store = KV.KeyValueStore(self.temp_file, redhawk.GetVersion())
    return

  def tearDown(self):
    self.store.Close()
    tearDown()

  def TestClearStore(self):
    assert(self.store.HasKey('dog'))
    assert(self.store.HasKey('cat'))
    self.store.ClearStore()
    assert(not self.store.HasKey('dog'))
    assert(not self.store.HasKey('cat'))
    assert(self.store.GetVersion() == redhawk.GetVersion())

  def TestClose(self):
    pass

  def TestHasKey(self):
    assert(self.store.HasKey('dog'))
    assert(self.store.HasKey('cat'))
    assert(not self.store.HasKey('pig'))

  def TestGet(self):
    assert(self.store.Get('dog') == 'woof')
    assert(self.store.Get('cat') == 'meow')

  def TestSet(self):
    assert(not self.store.HasKey('pig'))
    self.store.Set('pig', 'grunt')
    assert(self.store.Get('pig') == 'grunt')

  def TestRetainOnClose(self):
    self.store.Set('pig', 'grunt')
    self.store.Close()
    self.store = KV.KeyValueStore(self.temp_file, redhawk.GetVersion())
    assert(self.store.Get('pig') == 'grunt')

  def TestWrite(self):
    self.store.Set('pig', 'grunt')
    self.store.Write()
    assert(self.store.Get('pig') == 'grunt')
    store2 = KV.KeyValueStore(self.temp_file, redhawk.GetVersion())
    assert(store2.Get('pig') == 'grunt')
    store2.Close()

  def TestRemoveKey(self):
    assert(self.store.HasKey('dog'))
    self.store.RemoveKey('dog')
    assert(not self.store.HasKey('dog'))

  def TestGetKeys(self):
    keys = list(self.store.GetKeys())
    assert(len(keys) == 2)
    assert('dog' in keys)
    assert('cat' in keys)

  def TestChangeVersion(self):
    self.store.Close()
    store = shelve.open(self.temp_file, 'c')
    store[KV.VERSION_KEY] = '0.0.0'
    store.close()

    temp_file = GetTempFile()
    fp = sys.stderr
    sys.stderr = sys.stdout

    print "Expected Error :"
    self.store = KV.KeyValueStore(self.temp_file, redhawk.GetVersion())

    sys.stderr = fp

    assert(self.store.GetVersion() == redhawk.GetVersion())

