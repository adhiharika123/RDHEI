
class HuffmanTree:
    def __init__(self, n):
        size = 2 * n - 1
        self.parent = [0] * size
        self.left = [0] * size
        self.right = [0] * size
        self.root = size - 1

def build_tree(freqs, leaves):
    n = len(freqs)
    freqs = freqs + [float('inf')] * (2 * n - 1 - n)  # Extend freq list with inf to size 2n-1
    tree = HuffmanTree(n)

    for i in range(n):
        tree.parent[i] = 0

    for i in range(n, 2 * n - 1):
        min_freqs = [float('inf'), float('inf')]
        min_nodes = [-1, -1]
        for j in range(i):
            if tree.parent[j] == 0:
                if freqs[j] < min_freqs[0]:
                    min_freqs[1] = min_freqs[0]
                    min_nodes[1] = min_nodes[0]
                    min_freqs[0] = freqs[j]
                    min_nodes[0] = j
                elif freqs[j] < min_freqs[1]:
                    min_freqs[1] = freqs[j]
                    min_nodes[1] = j
        tree.parent[min_nodes[0]] = i
        tree.parent[min_nodes[1]] = i
        tree.left[i] = min_nodes[0]
        tree.right[i] = min_nodes[1]
        freqs[i] = min_freqs[0] + min_freqs[1]

    tree.root = 2 * n - 2  # zero-based index
    for i in range(n):
        tree.left[i] = -leaves[i]
    return tree

def huffman_encoding(freqs):
    """
    Build Huffman codes based on input frequency list.

    Args:
        freqs (list of int): Frequencies for symbols.

    Returns:
        tuple: codes list (symbol index ordered), dict list with (symbol index, code string)
    """
    n = len(freqs)
    sorted_tuples = sorted(enumerate(freqs), key=lambda x: x[1])
    indices = [t[0] for t in sorted_tuples]
    sorted_freqs = [t[1] for t in sorted_tuples]

    leaves = indices.copy()
    tree = build_tree(sorted_freqs.copy(), leaves)

    dict_list = [None] * n
    codes = [None] * n

    for i in range(n):
        code = ''
        node = i
        while node != tree.root:
            parent = tree.parent[node]
            if node == tree.left[parent]:
                code = '0' + code
            else:
                code = '1' + code
            node = parent
        dict_list[i] = (indices[i], code)
        codes[i] = code

    return codes, dict_list
