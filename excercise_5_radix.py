from dataclasses import dataclass, field


@dataclass
class St_node:
    """
    Represents a single node in the radix tree.
    """
    s_label: str
    b_is_word: bool = False
    lst_children: list = field(default_factory=list)


class Cl_radix_tree:
    """
    A radix tree (compressed prefix tree) implementation.
    """

    def __init__(self):
        self.st_root = St_node(s_label="")
        return

    def insert(self, i_s_word: str):

        st_node = self.st_root

        while True:
            b_found_match = False

            for st_child in st_node.lst_children:

                n_prefix_len = self._common_prefix(
                    st_child.s_label,
                    i_s_word
                )

                if n_prefix_len == 0:
                    continue

                b_found_match = True

                # Full child match → descend
                if n_prefix_len == len(st_child.s_label):

                    st_node = st_child
                    i_s_word = i_s_word[n_prefix_len:]

                    # Entire word consumed
                    if i_s_word == "":
                        st_node.b_is_word = True
                        return

                    break

                # Partial match → split
                return self._split_and_insert(
                    st_node,
                    st_child,
                    n_prefix_len,
                    i_s_word
                )

            if b_found_match:
                continue

            # No matching child → create leaf
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

        s_prefix = i_st_child.s_label[:i_n_prefix_len]
        s_child_suffix = i_st_child.s_label[i_n_prefix_len:]
        s_new_suffix = i_s_word[i_n_prefix_len:]

        # Intermediate node
        st_node_mid = St_node(s_label=s_prefix)

        # Replace old child
        i_st_parent.lst_children.remove(i_st_child)
        i_st_parent.lst_children.append(st_node_mid)

        # Old child becomes suffix child
        i_st_child.s_label = s_child_suffix
        st_node_mid.lst_children.append(i_st_child)

        # If inserted word ends exactly at prefix
        if s_new_suffix == "":
            st_node_mid.b_is_word = True

        # Otherwise add remaining suffix
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

        lst_words = list()

        for st_child in i_st_node.lst_children:

            s_word = i_s_prefix + st_child.s_label

            # Current node forms a word
            if st_child.b_is_word:
                lst_words.append(s_word)

            # Collect recursive results
            lst_words.extend(
                Cl_radix_tree._walk(st_child, s_word)
            )

        return lst_words

    def to_list(self) -> list[str]:
        """
        Reconstruct all stored words from the radix tree.

        Returns
        -------
        list[str]
            All words currently stored in the tree.
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

    

