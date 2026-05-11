from dataclasses import dataclass, field

@dataclass
class St_node:
    """
    Represents a single node in the radix tree.

    Fields
    ------
    s_label : str
        The substring (edge label) stored at this node. This is the compressed
        fragment of the path from the parent to this node.

    lst_children : list[St_node]
        The list of child nodes. Each child represents a further substring
        branching from this node. Children are stored as a list because the
        branching factor is typically small and linear search is acceptable.
    """
    s_label: str
    lst_children: list = field(default_factory=list)


class Cl_radix_tree:
    """
    A radix tree (compressed prefix tree) implementation.

    This structure stores strings in a compact form by merging common prefixes.
    Each node contains a substring (s_label), and children represent further
    substrings branching from that prefix.

    Key invariants:
    - No two siblings may start with the same character.
    - Each node's s_label is non-empty except for the root.
    - Insertions may cause node splitting when partial prefix matches occur.
    """
    def __init__(self):
        """Initialize the radix tree with an empty root node."""
        self.st_root = St_node(s_label="")
        return

    def insert(self, i_s_word: str):
        """
        Insert a word into the radix tree.

        Parameters
        ----------
        i_s_word : str
            The string to insert. The algorithm walks down the tree, matching
            prefixes against existing children. If a partial match occurs, the
            child is split into a prefix node and a suffix node.
        """
        st_node = self.st_root
        
        while True:
            b_found_match = False   # Track whether any child matched

            for st_child in st_node.lst_children:
                n_prefix_len = self._common_prefix(st_child.s_label, i_s_word)

                if n_prefix_len == 0:
                    # No common prefix → try next child
                    continue

                # A matching child was found
                b_found_match = True

                # Case 1: full match of child label → descend
                if n_prefix_len == len(st_child.s_label):
                    st_node = st_child
                    i_s_word = i_s_word[n_prefix_len:]

                    # Entire word consumed → insertion complete
                    if i_s_word == "":
                        return

                    # Continue outer while-loop
                    # (no break needed)
                    # We simply stop scanning siblings
                    # by forcing the for-loop to end early
                    break

                # Case 2: partial match → split
                return self._split_and_insert(st_node, st_child, n_prefix_len, i_s_word)

            # If we matched a child and broke out of the for-loop,
            # continue the while-loop to descend further.
            if b_found_match:
                continue

            # No matching child found → create new leaf
            st_node.lst_children.append(St_node(s_label=i_s_word))
            return

    def _split_and_insert(self, i_st_parent, i_st_child, i_n_prefix_len, i_s_word):
        """
        Split a child node when a partial prefix match occurs.

        Example:
            Existing child label: "roman"
            New word:             "romulus"
            Common prefix:        "rom"

        This function:
        - Creates a new intermediate node with label "rom"
        - Moves the old child under it with suffix "an"
        - Adds a new child for the remaining part of the inserted word ("ulus")

        Parameters
        ----------
        i_st_parent : St_node
            The parent node containing the child to be split.

        i_st_child : St_node
            The child node whose label partially matches the new word.

        i_n_prefix_len : int
            Length of the common prefix.

        i_s_word : str
            The full word being inserted.
        """
        # Extract prefix and suffixes
        s_prefix = i_st_child.s_label[:i_n_prefix_len]
        s_child_suffix = i_st_child.s_label[i_n_prefix_len:]
        s_new_suffix = i_s_word[i_n_prefix_len:]

        # Create intermediate node holding the common prefix
        mid = St_node(s_label=s_prefix)

        # Replace old child with the new intermediate node
        i_st_parent.lst_children.remove(i_st_child)
        i_st_parent.lst_children.append(mid)

        # Old child becomes a child of the intermediate node
        i_st_child.s_label = s_child_suffix
        mid.lst_children.append(i_st_child)

        # Insert new branch for the remainder of the inserted word
        if s_new_suffix != "":
            mid.lst_children.append(St_node(s_label=s_new_suffix))

        return

    def _common_prefix(self, i_s_left: str, i_s_right: str) -> int:
        """
        Compute the length of the common prefix between two strings.

        Parameters
        ----------
        a, b : str
            Strings to compare.

        Returns
        -------
        int
            Number of matching characters from the start.
        """
        n_index = 0
        while n_index < len(i_s_left) and n_index < len(i_s_right) and i_s_left[n_index] == i_s_right[n_index]:
            n_index += 1
        return n_index

    def display(self, i_st_node=None, i_s_indent=""):
        """
        Recursively print the structure of the radix tree.

        Parameters
        ----------
        node : St_node or None
            Node to display. If None, starts from the root.

        indent : str
            Indentation prefix for pretty-printing.
        """
        if i_st_node is None:
            i_st_node = self.st_root

        for st_child in i_st_node.lst_children:
            print(f"{i_s_indent}- '{st_child.s_label}'")
            self.display(st_child, i_s_indent + "  ")

if __name__ == "__main__":

    cl_tree = Cl_radix_tree()

    for s_data in ["roman", "romulus", "robert", "teletubbies", "romani"]:
        cl_tree.insert(s_data)

    cl_tree.display()
