
import os
import time
import glob
import logging

from . import utils


class BaseNode(object):

    def __init__(self, name, submit=None, extra_lines=None, dag=None,
                 verbose=0):

        # Validate user input
        if extra_lines and not isinstance(extra_lines, (str, list, tuple)):
            raise TypeError('extra_lines must be of type str, list, or tuple')
        elif extra_lines and isinstance(extra_lines, str):
            extra_lines = [extra_lines]

        self.name = utils.string_rep(name)
        if submit is not None:
            self.submit = submit
        elif os.getenv('PYCONDOR_SUBMIT_DIR'):
            self.submit = os.getenv('PYCONDOR_SUBMIT_DIR')
        else:
            self.submit = os.getcwd()
        self.extra_lines = extra_lines
        self.dag = dag
        if dag is not None:
            dag._add_node(self)
        self._built = False

        self.parents = []
        self.children = []

        # Set up logger
        self.logger = logging.getLogger(self.__module__)

    def _get_fancyname(self):

        date = time.strftime('%Y%m%d')
        file_pattern = os.path.join(self.submit,
                                    '{}_{}_??.submit'.format(self.name, date))
        submit_number = len(glob.glob(file_pattern)) + 1
        fancyname = self.name + '_{}_{:02d}'.format(date, submit_number)

        return fancyname

    def _hasparent(self, node):
        return node in self.parents

    def add_parent(self, node):
        """Adds node to parents list

        Parameters
        ----------
        node : BaseNode
            Job or Dagman to append to the parents list.

        Returns
        -------
        self : object
            Returns self.

        """
        # Ensure that node is a BaseNode
        if not isinstance(node, BaseNode):
            raise TypeError(
                    'add_parent() is expecting a Job or Dagman instance.'
                    ' Got an object of type {}'.format(type(node)))

        # Don't bother continuing if node is already in the parents list
        if self._hasparent(node):
            return self

        # Add node to existing parents
        self.parents.append(node)
        self.logger.debug(
            'Added {} as a parent for {}'.format(node.name, self.name))

        # Add self instance as a child to the new parent node
        node.add_child(self)

        return self

    def add_parents(self, nodes):
        """Adds nodes to the parents list

        Parameters
        ----------
        nodes : list or tuple
            List of nodes to append to the parents list

        Returns
        -------
        self : object
            Returns self.

        """
        # Check that nodes is a list/tuple of BaseNode objects
        if (isinstance(nodes, (list, tuple)) and
                all([isinstance(node, BaseNode) for node in nodes])):
            for node in nodes:
                self.add_parent(node)
        else:
            raise TypeError('add_parents() is expecting an iterable of '
                            'Job and/or Dagman objects')

        return self

    def _haschild(self, node):
        return node in self.children

    def add_child(self, node):
        """Adds node to children list

        Parameters
        ----------
        node : BaseNode
            Job or Dagman to append to the children list.

        Returns
        -------
        self : object
            Returns self.

        """
        # Ensure that node is a BaseNode
        if not isinstance(node, BaseNode):
            raise TypeError(
                    'add_child() is expecting a Job or Dagman instance.'
                    ' Got an object of type {}'.format(type(node)))

        # Don't bother continuing if node is already in the children list
        if self._haschild(node):
            return self

        # Add node to existing children
        self.children.append(node)
        self.logger.debug(
            'Added {} as a child for {}'.format(node.name, self.name))
        # Add this BaseNode instance as a parent to the new child node
        node.add_parent(self)

        return self

    def add_children(self, nodes):
        """Adds nodes to the children list

        Parameters
        ----------
        nodes : list or tuple
            List of nodes to append to the children list

        Returns
        -------
        self : object
            Returns self.

        """
        # Check that nodes is a list/tuple of BaseNode objects
        if (isinstance(nodes, (list, tuple)) and
                all([isinstance(node, BaseNode) for node in nodes])):
            for node in nodes:
                self.add_child(node)
        else:
            raise TypeError('add_children() is expecting an iterable of '
                            'Job and/or Dagman objects')

        return self

    def haschildren(self):
        """Checks for any children nodes

        Returns
        -------
        bool
            Returns whether or not this node has any child nodes.

        """
        return bool(self.children)

    def hasparents(self):
        """Checks for any parent nodes

        Returns
        -------
        bool
            Returns whether or not this node has any parent nodes.

        """
        return bool(self.parents)
