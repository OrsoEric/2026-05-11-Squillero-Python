from dataclasses import dataclass, field


@dataclass
class St_node:
    """
    Single node used by the radix tree.

    A radix tree (also called a compressed trie or compact prefix tree)
    stores strings by grouping common prefixes together. Unlike a classic
    trie where each character is represented by a separate node, a radix
    tree compresses chains of single-child nodes into a single string
    segment.

    Example
    -------
    If the tree stores:

        "test"
        "team"

    a normal trie might store:

        t -> e -> s -> t
               └-> a -> m

    while a radix tree stores compressed labels:

        "te"
         ├─ "st"
         └─ "am"

    Parameters
    ----------
    s_label : str
        String fragment represented by this node.

        The full word represented by a path is reconstructed by
        concatenating labels from the root to a terminal node.

    b_is_word : bool, default=False
        Indicates whether the path ending at this node forms
        a complete stored word.

        Important:
        ----------
        A node may simultaneously:
            * represent a complete word
            * have children extending that word

        Example:
            "test"
            "testing"

        The node for "test" is a valid word while also having
        a child containing "ing".

    lst_children : list[St_node]
        Child nodes extending the current prefix.

    Notes
    -----
    The root node of the tree usually contains an empty label ("").
    """

    s_label: str
    b_is_word: bool = False
    lst_children: list = field(default_factory=list)


class Cl_radix_tree:
    """
    Radix tree (compressed trie) implementation.

    Overview
    --------
    A radix tree is a space-optimized trie specialized for storing
    strings efficiently when many words share common prefixes.

    Instead of storing one character per node, consecutive characters
    are compressed into larger string fragments.

    Example
    -------
    Inserting the words:

        "test"
        "team"
        "toast"

    produces a structure conceptually similar to:

        root
        ├─ "t"
            ├─ "e"
            │   ├─ "st"  [WORD]
            │   └─ "am"  [WORD]
            └─ "oast"    [WORD]

    Advantages
    ----------
    Compared to a classic trie:

    * Fewer nodes
    * Reduced memory usage
    * Faster traversal in many cases
    * Efficient prefix matching

    Core Idea
    ---------
    Every edge stores a string fragment instead of a single character.

    During insertion:
        1. Find the longest common prefix between the remaining
           word portion and existing child labels.
        2. Depending on the match:
            * no match      -> create new child
            * full match    -> descend further
            * partial match -> split existing node

    Time Complexity
    ---------------
    Let:
        n = length of inserted/searched word

    Typical complexity:
        O(n)

    Worst case:
        O(n * c)

    where c is the number of siblings checked at each level.

    Space Complexity
    ----------------
    O(total stored characters)

    The compression typically reduces node count substantially compared
    to a normal trie.

    Terminology
    -----------
    Prefix:
        Starting substring shared by multiple words.

    Compressed edge:
        A node label containing multiple characters.

    Split:
        Operation performed when a partial prefix match occurs.
    """

    def __init__(self):
        """
        Create an empty radix tree.

        The root node contains an empty string and does not represent
        a real stored word.
        """

        self.st_root = St_node(s_label="")
        return

    def insert(self, i_s_word: str):
        """
        Insert a word into the radix tree.

        Algorithm
        ---------
        The insertion process repeatedly compares the remaining part
        of the word against the labels of the current node's children.

        Three possible situations may occur:

        1. No common prefix
        -------------------
        No child shares a prefix with the word.

        Action:
            Create a new leaf node containing the entire remaining word.

        Example:
            Existing:
                "test"

            Insert:
                "banana"

            Result:
                separate branch added

        ------------------------------------------------------------

        2. Full child match
        -------------------
        The child's label fully matches the beginning of the word.

        Action:
            Descend into that child and continue processing the
            remaining suffix.

        Example:
            Child label:
                "test"

            Word:
                "testing"

            Remaining suffix:
                "ing"

        ------------------------------------------------------------

        3. Partial match
        ----------------
        Only part of the child label matches.

        Action:
            Split the existing node into:
                * common prefix node
                * old suffix child
                * new suffix child

        Example:
            Existing child:
                "testing"

            Insert:
                "tester"

            Common prefix:
                "test"

            Split into:
                "test"
                ├─ "ing"
                └─ "er"

        Parameters
        ----------
        i_s_word : str
            Word to insert into the tree.

        Notes
        -----
        Duplicate insertions are allowed but do not create duplicate
        nodes. The terminal marker is simply set again.
        """

        st_node = self.st_root

        while True:

            b_found_match = False

            for st_child in st_node.lst_children:

                # Determine how many leading characters are shared
                # between the child label and the remaining word.
                n_prefix_len = self._common_prefix(
                    st_child.s_label,
                    i_s_word
                )

                # No shared prefix -> try next child.
                if n_prefix_len == 0:
                    continue

                b_found_match = True

                # -------------------------------------------------
                # CASE 1:
                # Full child match.
                #
                # Example:
                #     child = "test"
                #     word  = "testing"
                #
                # We descend into the child and continue inserting
                # the remaining suffix "ing".
                # -------------------------------------------------
                if n_prefix_len == len(st_child.s_label):

                    st_node = st_child

                    # Remove matched prefix from the remaining word.
                    i_s_word = i_s_word[n_prefix_len:]

                    # Entire word consumed.
                    #
                    # Example:
                    #     inserting "test"
                    #     existing path already contains "test"
                    #
                    # Mark node as terminal.
                    if i_s_word == "":
                        st_node.b_is_word = True
                        return

                    break

                # -------------------------------------------------
                # CASE 2:
                # Partial match.
                #
                # Example:
                #     existing child = "testing"
                #     new word       = "tester"
                #
                # Common prefix:
                #     "test"
                #
                # Requires node splitting.
                # -------------------------------------------------
                return self._split_and_insert(
                    st_node,
                    st_child,
                    n_prefix_len,
                    i_s_word
                )

            # A child matched and traversal should continue.
            if b_found_match:
                continue

            # -----------------------------------------------------
            # CASE 3:
            # No matching child exists.
            #
            # Create a new leaf node containing the entire
            # remaining suffix.
            # -----------------------------------------------------
            st_node.lst_children.append(
                St_node(
                    s_label=i_s_word,
                    b_is_word=True
                )
            )

            return

    def _split_and_insert(
        self,
        i_st_parent,
        i_st_child,
        i_n_prefix_len,
        i_s_word
    ):
        """
        Split an existing node due to a partial prefix match.

        Why Splitting Is Needed
        -----------------------
        Suppose the tree already contains:

            "testing"

        and we insert:

            "tester"

        The existing child label:

            "testing"

        partially matches the new word:

            "tester"

        Shared prefix:
            "test"

        Existing suffix:
            "ing"

        New suffix:
            "er"

        The original node must therefore be transformed into:

            "test"
            ├─ "ing"
            └─ "er"

        Parameters
        ----------
        i_st_parent : St_node
            Parent containing the child being split.

        i_st_child : St_node
            Existing child node that partially matched.

        i_n_prefix_len : int
            Length of the shared prefix.

        i_s_word : str
            Word currently being inserted.

        Steps
        -----
        1. Extract shared prefix.
        2. Create intermediate node containing that prefix.
        3. Replace old child with intermediate node.
        4. Convert old child into suffix node.
        5. Add new suffix branch if needed.
        """

        # Shared prefix between old child and new word.
        s_prefix = i_st_child.s_label[:i_n_prefix_len]

        # Remaining suffix from the original child.
        s_child_suffix = i_st_child.s_label[i_n_prefix_len:]

        # Remaining suffix from the inserted word.
        s_new_suffix = i_s_word[i_n_prefix_len:]

        # Create intermediate prefix node.
        st_node_mid = St_node(s_label=s_prefix)

        # Replace original child with intermediate node.
        i_st_parent.lst_children.remove(i_st_child)
        i_st_parent.lst_children.append(st_node_mid)

        # Transform original child into suffix node.
        i_st_child.s_label = s_child_suffix

        # Attach old suffix branch.
        st_node_mid.lst_children.append(i_st_child)

        # If the inserted word ends exactly at the prefix,
        # the intermediate node itself becomes a valid word.
        #
        # Example:
        #     existing = "testing"
        #     inserted = "test"
        if s_new_suffix == "":
            st_node_mid.b_is_word = True

        # Otherwise create another suffix branch.
        #
        # Example:
        #     existing = "testing"
        #     inserted = "tester"
        else:
            st_node_mid.lst_children.append(
                St_node(
                    s_label=s_new_suffix,
                    b_is_word=True
                )
            )

        return

    def _common_prefix(
        self,
        i_s_left: str,
        i_s_right: str
    ) -> int:
        """
        Compute the length of the common prefix shared by two strings.

        Example
        -------
        left:
            "testing"

        right:
            "tester"

        common prefix:
            "test"

        returned value:
            4

        Parameters
        ----------
        i_s_left : str
            First string.

        i_s_right : str
            Second string.

        Returns
        -------
        int
            Number of leading characters shared by both strings.

        Complexity
        ----------
        O(min(len(left), len(right)))
        """

        n_index = 0

        while (
            n_index < len(i_s_left)
            and n_index < len(i_s_right)
            and i_s_left[n_index] == i_s_right[n_index]
        ):
            n_index += 1

        return n_index

    def display(
        self,
        i_st_node=None,
        i_s_indent=""
    ):
        """
        Print a visual representation of the radix tree.

        Example Output
        --------------
        - 'te'
          - 'st' [WORD]
          - 'am' [WORD]

        Parameters
        ----------
        i_st_node : St_node | None
            Node currently being displayed.

            If None, traversal starts at the root.

        i_s_indent : str
            Indentation used for recursive formatting.

        Notes
        -----
        This is primarily intended for debugging and educational
        visualization.
        """

        if i_st_node is None:
            i_st_node = self.st_root

        for st_child in i_st_node.lst_children:

            s_marker = " [WORD]" if st_child.b_is_word else ""

            print(
                f"{i_s_indent}- '{st_child.s_label}'{s_marker}"
            )

            self.display(
                st_child,
                i_s_indent + "  "
            )

    @staticmethod
    def _walk(i_st_node, i_s_prefix):
        """
        Recursively reconstruct words stored beneath a node.

        Algorithm
        ---------
        Because radix tree nodes store only fragments, full words are
        reconstructed by concatenating labels encountered during traversal.

        Example
        -------
        Path:
            "te" -> "st"

        Reconstructed word:
            "test"

        Parameters
        ----------
        i_st_node : St_node
            Current traversal node.

        i_s_prefix : str
            Prefix accumulated from parent nodes.

        Returns
        -------
        list[str]
            All complete words reachable from the node.
        """

        lst_words = list()

        for st_child in i_st_node.lst_children:

            # Reconstruct full prefix for this branch.
            s_word = i_s_prefix + st_child.s_label

            # Current node forms a complete stored word.
            if st_child.b_is_word:
                lst_words.append(s_word)

            # Recursively collect descendant words.
            lst_words.extend(
                Cl_radix_tree._walk(st_child, s_word)
            )

        return lst_words

    def to_list(self) -> list[str]:
        """
        Reconstruct all words stored in the radix tree.

        Returns
        -------
        list[str]
            List containing every stored word.

        Example
        -------
        >>> tree = Cl_radix_tree()
        >>> tree.insert("test")
        >>> tree.insert("team")
        >>> tree.to_list()
        ['test', 'team']

        Notes
        -----
        The traversal is depth-first and reconstructs words by
        concatenating node labels along each path.
        """

        lst_words = self._walk(self.st_root, "")

        return lst_words



if __name__ == "__main__":

    cl_tree = Cl_radix_tree()

    for s_data in ["teletubbies", "roman", "romulus", "robert", "romani", "tele"]:
        print(f"ADDING: {s_data}")
        cl_tree.insert(s_data)
        print("=========TREE STRUCTURE=========")
        cl_tree.display()
        
    print("=========RECONSTRUCTED WORDS=========")
    print(cl_tree.to_list())

    

