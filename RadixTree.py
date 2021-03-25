from Node import *
import numpy as np

class RadixTree:
    """
    A class used to store strings as a Radix Tree

    Attributes
    ----------

    root: Node
        a node object with an empty string as a value, the root of the Radix Tree
        and is always initialized

    Methods
    -------

    add_string(string: str)
        Adds the given string to the tree.

    add_multiple(data: Iterable)
        Adds every element of data to the tree

    parents(target: str)
        returns a list of parents of the given string. It may not be in the tree

    kids(target: str)
        returns a list of kids of the given string
    """
    def __init__(self, data=None,from_save=False):
        """
        Initializes root as an empty string Node
        and adds each string in data parameter to the tree using
        add_string method

        Parameters
        ----------

        data: iterable
            Any iterable containing strings that should be stored in the Radix Tree

        """

        self.root = Node('')
        if data is None:
            return

        if isinstance(data,str):
            if data == "":
                return
            self.add(data)
            return

        if from_save:
            self._load(data)
        else:
            for string in data:
                if string == "":
                    continue
                self.add(string)

    def __len__(self):
        return self._search_for_ends_count(self.root)

    def __iter__(self):
        output = '0'
        counter = 0
        inner_count = -1
        while output != '':
            output = ''
            for i in range(len(self.root.children)):
                output, inner_count = self._search_for_end_by_num(self.root.children[i], counter, inner_count, '')
                if output != '':
                    break
            counter += 1
            inner_count = -1
            if output != '':
                yield output

    def __contains__(self, target):
        """
        Checks if the target string is stored in the tree

        Parameter
        ---------

        target: str
            a string to be checked

        Returns
        -------

        True - if target is in the tree
        False - otherwise
        """
        # get down to the last node till there's no more valid children
        temp_root = self.root
        closest_kid = ''
        character = 1
        left_cursor = 0
        found_kid = False
        while character <= len(target):
            next_node = temp_root.child(target[left_cursor:character])
            if next_node:
                found_kid = True
                temp_root = next_node
                closest_kid += target[left_cursor:character]
                left_cursor = character

            character += 1
        else:
            if not found_kid and target != '':
                return False
            if left_cursor == len(target) and temp_root.end:
                return True
            else:
                return False

    def __set__(self, instance, data):
        self.__init__(data)

    def add(self, string:str):
        """
        Adds the input string to the tree according to the Radix Tree structure

        Parameter
        ----------

        string: str
            the string to be added to the tree
        """

        # this function adds each character of the code step by step according to the Radix Tree concept
        temp_root = self.root
        left_cursor = 0
        character = 1
        ever_found_node = False
        # descending till the first error appears
        while character <= len(string):
            child = temp_root.child_starts_with(string[left_cursor:character])
            if child:
                ever_found_node = True
                child_backup = child
                # handles repetitive string addition
                if character == len(string):
                    # jumps to the node that already has the string written
                    # means that the 'end' indicator is not falsely placed on the node above
                    temp_root = child_backup
            else:
                if ever_found_node:
                    temp_root = child_backup
                    if character - left_cursor > len(child_backup.value):
                        left_cursor = character - 1
                        ever_found_node = False
                        continue
                    else:
                        lower_part = Node(temp_root.value[character - left_cursor - 1:])
                        lower_part.children = temp_root.children
                        lower_part.end = temp_root.end
                        temp_root.value = temp_root.value[:character - left_cursor - 1]
                        temp_root.children = [lower_part, Node(string[character - 1:])]
                        temp_root.end = False
                        temp_root = temp_root.children[-1]
                        character = len(string) + 1
                else:
                    temp_root.add_node(string[character - 1:])
                    temp_root = temp_root.children[-1]
                    character = len(string) + 1

            character += 1
        else:
            temp_root.set_ending(True)

    def add_multiple(self, data):
        """
        Adds every string in data to the tree

        Parameter
        ---------

        data: iterable
            An iterable containing strings to be added to already initialized tree
        """
        for code in data:
            self.add(code)

    def parents(self, target):
        """

        Searches for any strings stored in tree that are hierarchically higher
        than the input string. Outputs them as a list

        Parameter
        ---------

        target: str
            A string the parents of which are required

        Returns
        -------

        output: list of str
            A list containing all of the parent strings found.
            Returns an empty list if no parents found

        """

        # the function simply descends from the root down to the target collecting all the possible 'end's
        output = []
        parent = ''
        temp_root = self.root
        character = 1
        left_cursor = 0
        while character < len(target):
            next_node = temp_root.child(target[left_cursor:character])
            if next_node:
                parent += next_node.value
                temp_root = next_node
                left_cursor = character
                if temp_root.end:
                    output.append(parent)
            character += 1

        return output

    def kids(self, target):
        """

        Searches for any strings stored in tree that are hierarchically lower
        than the input string. Outputs them as a list

        Parameter
        ---------

        target: str
            A string the kids of which are required.
            Is not required to be in the tree

        Returns
        -------

        output: list of str
            A list containing all of the parent strings found.
            Returns an empty list if no parents found

        """

        output = []
        closest_kid = ''

        # get down to the last node till there's no more valid children
        temp_root = self.root
        character = 1
        left_cursor = 0
        found_kid = False
        while character <= len(target):
            next_node = temp_root.child(target[left_cursor:character])
            if next_node:
                found_kid = True
                temp_root = next_node
                closest_kid += target[left_cursor:character]
                left_cursor = character

            character += 1
        else:
            if not found_kid and target != '':
                return output
            if left_cursor != len(target):
                temp_root = temp_root.child_starts_with(target[left_cursor:])
                closest_kid += temp_root.value

        # consider removing
        # if len(closest_kid) > len(target):
        #    output += [closest_kid]

        # search for ends from the node found
        for i in range(len(temp_root.children)):
            output += self._search_for_ends_save_values(temp_root.children[i], closest_kid)

        return output

    def structural_parents(self, target):
        """

        Searches for any strings formed by nodes in the tree that are hierarchically higher
        than the input. Outputs them as a list

        Parameter
        ---------

        target: str
            A string the parents of which are required

        Returns
        -------

        output: list of str
            A list containing all of the parent strings found.
            Returns an empty list if no parents found

        """

        # the function simply descends from the root down to the target collecting all the possible 'end's
        output = []
        parent = ''
        temp_root = self.root
        character = 1
        left_cursor = 0
        while character < len(target):
            next_node = temp_root.child(target[left_cursor:character])
            if next_node:
                parent += next_node.value
                temp_root = next_node
                left_cursor = character
                output.append(parent)
            character += 1

        return output

    def structural_kids(self, target):
        """

        Searches for any strings formed by nodes of the tree that are hierarchically lower
        than the input string. Outputs them as a list

        Parameter
        ---------

        target: str
            A string the kids of which are required.
            Is not required to be in the tree

        Returns
        -------

        output: list of str
            A list containing all of the parent strings found.
            Returns an empty list if no parents found

        """

        output = []
        closest_kid = ''

        # get down to the last node till there's no more valid children
        temp_root = self.root
        character = 1
        left_cursor = 0
        found_kid = False
        while character <= len(target):
            next_node = temp_root.child(target[left_cursor:character])
            if next_node:
                found_kid = True
                temp_root = next_node
                closest_kid += target[left_cursor:character]
                left_cursor = character

            character += 1
        else:
            if not found_kid and target != '':
                return output
            if left_cursor != len(target):
                temp_root = temp_root.child_starts_with(target[left_cursor:])
                closest_kid += temp_root.value

        # consider removing
        # if len(closest_kid) > len(target):
        #    output += [closest_kid]

        # search for ends from the node found
        for i in range(len(temp_root.children)):
            output += self._search_for_ends_save_values(temp_root.children[i], closest_kid)

        return output

    def export(self,filename=None):
        queue = [[self.root,0]]
        count = 0
        result = []
        for node, id_ in queue:
            if not len(node.children):
                continue
            for child in node.children:
                count += 1
                queue.append([child,count])
                result.append([id_,child.value,int(child.end)])
        if filename:
            np.save(filename,result)
        return result

    def _search_for_nodes_values(self, start, parent):

        output = []
        temp_root = start
        kid = parent + temp_root.value
        output.append(kid)

        for i in range(len(temp_root.children)):
            output += self._search_for_nodes_values(temp_root.children[i],kid)
        return output

    def _search_for_ends_save_values(self, start, parent):
        # a recurrent function that checks if the code can be ended at this point,
        # adds it to the output list and performs the same operations on the heirs

        output = []
        temp_root = start
        kid = parent + temp_root.value
        if temp_root.end:
            output = [kid]

        for i in range(len(temp_root.children)):
            output += self._search_for_ends_save_values(temp_root.children[i], kid)
        return output

    def _search_for_ends_count(self, start):
        # a recurrent function that checks if the code can be ended at this point,
        # adds it to the output list and performs the same operations on the heirs

        output = 0
        temp_root = start
        if temp_root.end:
            output += 1

        for i in range(len(temp_root.children)):
            output += self._search_for_ends_count(temp_root.children[i])
        return output

    def _search_for_end_by_num(self,
                               start, number_of_el,
                               counter, value):
        # a recurrent function that adds current Node.value
        # to the value arg,
        # checks if the code can be ended at this point,
        # increments the counter if True,
        # breaks if counter matches the wanted number
        # -------
        # returns the output string and counter (to keep on searching if reached the dead end)

        temp_root = start
        if temp_root.end:
            counter = counter + 1
        value = value + temp_root.value
        if counter == number_of_el:
            return value, counter
        else:
            output = ''
        for i in range(len(temp_root.children)):
            output, counter = self._search_for_end_by_num(temp_root.children[i], number_of_el, counter, value)
            if output != '':
                break
        return output, counter

    def _load(self,data):
        queue = {0:self.root}
        count = 0
        for parent, val, end in data:
            parent = int(parent)
            end = int(end)
            count += 1
            new = Node(val,end)
            queue[parent].children.append(new)
            queue[count] = new

