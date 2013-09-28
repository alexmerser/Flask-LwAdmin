#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'

from flask import url_for
from flask_wtf import Form
from flask_lwadmin import ConfigurationError


class ConfigParser:
    NO_URL = 0
    URL_INTERNAL = 1
    URL_EXTERNAL = 2
    URL_METHOD = 3

    def __init__(self):
        self.list_configuration = dict(
            actions=[],
            object_actions=[],
            batch={},
            filter={}
        )

    def configure(self, configuration):
        if 'list' in configuration.keys():
            if 'actions' in configuration['list'].keys():
                self.parse_list_actions(configuration['list']['actions'])

            if 'object_actions' in configuration['list'].keys():
                self.parse_list_object_actions(configuration['list']['object_actions'])

            if 'batch' in configuration['list'].keys():
                self.parse_batch(configuration['list']['batch'])

            if 'filter' in configuration['list'].keys():
                self.parse_filter(configuration['list']['filter'])

    def parse_list_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['actions'].append(parsed)

    def parse_list_object_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['object_actions'].append(parsed)

    def parse_action(self, action):
        if not all(k in action for k in ('key', 'label')):
            raise ConfigurationError('Wrong configuration format for list actions element')

        if 'type' not in action.keys():
            action['type'] = self.NO_URL

        if 'credential' not in action.keys():
            action['credential'] = None

        return action

    def parse_batch(self, batch_elemet):
        pass

    def parse_filter(self, filter_elemet):
        pass

    def is_list_actions(self):
        return True if self.list_configuration.get('actions', []) else False

    def get_list_actions(self):
        actions = self.list_configuration.get('actions', [])
        for action in actions:
            pre = action.copy()
            if pre['type'] == self.URL_INTERNAL:
                pre['url'] = url_for(pre['url'])
            if pre['key'] == 'delete':
                pre['form'] = Form()
            yield pre

    def is_list_object_actions(self):
        return True if self.list_configuration.get('object_actions', []) else False

    def get_list_object_actions(self):
        actions = self.list_configuration.get('object_actions', [])
        for action in actions:
            pre = action.copy()
            if pre['type'] == self.URL_INTERNAL:
                pre['url'] = url_for(pre['url'])
            yield pre

    def is_batch(self):
        return True if self.list_configuration.get('batch', {}) else False

    def is_filter(self):
        return True if self.list_configuration.get('filter', {}) else False
