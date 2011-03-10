#!/usr/bin/env python
# encoding: utf-8
import cPickle, os, getpass
HOME = os.environ['HOME']


class Config:
    def __init__(self, namespace, configFile):
        # set some local instance vars
        self.namespace = namespace
        self.configFile = configFile
        self._load()
        
    def _load(self):
        try:
            self.pickle = cPickle.load(open(self.configFile))
            if not self.pickle.get(self.namespace):
                self.pickle[self.namespace] = {}
        except (EOFError, IOError):
            #looks like this file doesn't exist. let's create it.
            cPickle.dump({}, open(self.configFile, "w"))
            self.pickle = {}
            self.pickle[self.namespace] = {}
        self.data = self.pickle[self.namespace]
    
    def _dump(self):
        self.pickle[self.namespace] = self.data
        cPickle.dump(self.pickle, open(self.configFile, "w"))

    def get(self, item, question=None, autoPrompt=True, silentInput=False, defaultValue=None):
        '''item - key of data you'd like back
           question - if autoprompting the user, what do you want to ask?
                      If you don't specify a question, the item name is used.
           autoPrompt - default True. If the key isn't found, prompt the user.'''
        if self.data.get(item):
            return self.data[item]
        if defaultValue:
            return self.put(item, defaultValue)
        if autoPrompt:
            return self.prompt(item, question, silentInput)
        return None

    def put(self, item, value):
        if value:
            self.data[item] = value
            self._dump()
        return value

    def prompt(self, item, question, silentInput=False):
        ask = question if question else "%s: " % item.title()
        if silentInput:
            userInput = getpass.getpass(ask)
        else:
            userInput = raw_input(ask)
        return self.put(item, userInput)
