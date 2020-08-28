class Node:
    """
    A class that stores the assigned value and a list of children,
    the simplest building block of a tree

    Attributes
    ----------

    value
        stores the data the Node should contain

    children: list
        stores an indicator value (0 by default) in its zero position,
        after it Node objects are appended if any

    Methods
    -------

    add_node(value)
        creates a new Node object using the input value and
        appends it to the children's list

    add_indicator(indicator)
        sets children[0] to the indicator value

    child(value)
        returns the first child node with the same value as input value,
        if fails in search returns False

    child_starts_with(value)
        returns the first child node which value begins with input value,
        if fails in search returns False

    """
    def __init__(self, value):
        """
        Initializes value attribute with value parameter
        and children attribute with the default [0] list

        Parameters
        ----------

        value
            Any object or value the Node should store

        """
        self.value = value
        # the first element in children list is devoted to indicator, which can take any value
        self.children = [0]

    def add_node(self, value):
        """
        Initializes a new Node object using value parameter
        and appends it to the children's list

        Parameters
        ----------

        value
            Any object or value the child-Node should store
        """
        # to add a child of a particular value to self
        self.children.append(Node(value))

    def add_indicator(self, indicator):
        """
        Sets the value of 0th position of children's list to the indicator parameter

        Parameters
        ----------

        indicator
            Any object or value the Node should be marked with
        """
        self.children[0] = indicator

    def child(self, value):
        """
        Searches for the child-Node with the value as in the value parameter

        Parameters
        ----------

        value
            Any object or value the required child-Node should store

        Returns
        -------
        Node: a child-Node that has the value as in the value parameter
        False: in case no proper child was found
        """
        # checking the presence of a given value, in true case return the node desired
        check_range = range(1, len(self.children))

        for i in check_range:
            if value == self.children[i].value:
                return self.children[i]
        else:
            return False

    def child_starts_with(self, value):
        """
        Searches for the first child-Node which value begins with the value parameter.
        The Nodes' values have to support slicing

        Parameters
        ----------

        value
            Any object or value the required child-Node value should begin with

        Returns
        -------
        Node: a child-Node that has the value as in the value parameter
        False: in case no proper child was found

        """
        # checking the presence of at least one child that starts with given value, return the desired child
        length = len(value)
        check_range = range(1, len(self.children))
        for i in check_range:
            if self.children[i].value[:length] == value:
                return self.children[i]
        else:
            return False