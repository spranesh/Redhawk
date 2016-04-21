#!/usr/bin/env python

""" Implementation of a key value store, with version-numbers.
This is used by redhawk.common.get_ast.py for storing trees.

This Abstraction assumes that Permissions to read and write from the datastore
are in place.
"""

from __future__ import absolute_import
import redhawk

try:
    import anydbm
except ImportError:
    # anydbm was renamed to dbm in Python 3
    import dbm as anydbm

import logging
import os
import shelve
import sys

VERSION_KEY = '__redhawk__version__'

""" The following cases exist:
(Calleee checks for permissions).

* The store does not exist - Create it.
* The store is corrupted - Delete it.
* The store version number is wrong - Throw it away.
* Everything is alright.
"""

# Shelve open, and close abstraction barriers.
def _OpenStore(store_file):
  return shelve.open(store_file, 'c', protocol=-1)

def _CloseStoreObject(store_object):
  store_object.close()


# Utility Functions for creating, removing, and validating stores.
def CreateNewStore(store_file, version):
  """ Creates a new functioning store.
  The path should not exist before the function is called."""
  assert(os.path.exists(store_file) == False)
  store = _OpenStore(store_file)
  store[VERSION_KEY] = version
  _CloseStoreObject(store)
  assert(os.path.exists(store_file) == True)
  return None


def RemoveExistingStore(store_file):
  """ Removes an existing store. (`rm`s it).
  The path should exist before the function is called."""
  assert(os.path.exists(store_file) == True)
  os.remove(store_file)
  assert(os.path.exists(store_file) == False)
  return None


def IsValidStore(store_file):
  """ This merely checks that the store is not corrupt. It does NOT check for
  the version of the store."""
  try:
    store = _OpenStore(store_file)
    _CloseStoreObject(store)
  except anydbm.error as e:
    return False
  return True


class KeyValueStore:
  """ This Class assumes that the store is functioning, and not corrupt."""
  def __init__(self, store_file, version):
    self.version = version
    self.store_file = store_file
    self.store = _OpenStore(store_file)

    if (VERSION_KEY not in self.store or
      self.store[VERSION_KEY] != version):
        logging.error("Versions of redhawk do not match. Clearing database.\n")
        self.ClearStore()
    return

  def ClearStore(self):
    _CloseStoreObject(self.store)
    RemoveExistingStore(self.store_file)
    CreateNewStore(self.store_file, redhawk.GetVersion())
    self.store = shelve.open(self.store_file)
    return

  def Close(self):
    _CloseStoreObject(self.store)

  def Write(self):
    _CloseStoreObject(self.store)
    self.store = _OpenStore(self.store_file)

  def GetVersion(self):
    return self.store[VERSION_KEY]

  def HasKey(self, key):
    return key in self.store

  def Get(self, key):
    assert(key != VERSION_KEY)
    return self.store[key]

  def Set(self, key, value):
    assert(key != VERSION_KEY)
    self.store[key] = value

  def RemoveKey(self, key):
    self.store.pop(key)

  def GetKeys(self):
    return (i for i in self.store.keys() if i != VERSION_KEY)
