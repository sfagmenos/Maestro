# COMS W4115 - PROGRAMMING LANGUAGES AND TRANSLATORS
# Professor A. Aho
#
# Team 14, Maestro: An agile job orchestration language
# Team Mentor: A. Aho
#
# Team members:
#
# V. Atlidakis, ea2615, Project Manager
# G. Koloventzos, gk2409, System Integrator
# M. Lecuyer, ml3302, Language Guru
# Y. Lu, yl3033, Verification and validation person
# A. Swaminathan, as4522, System architect
#
# File: ast.py
# Description: Abstract Syntax Tree


class Node(object):

    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children
        self.leaf = leaf

    def traverse(self):
        childTree = []
        if isinstance(self.children, types.ListType):
            for child in self.children:
                if child.children:
                    childTree.append(child.traverse())
                else:
                    childTree.append(child)
        else:
            if self.children:
                childTree = self.children.traverse()
            else:
                childTree = self.children

        return [self.leaf, childTree]
