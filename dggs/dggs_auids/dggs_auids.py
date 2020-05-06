import base64
import functools
import hashlib
import zlib

import networkx as nx
from networkx.generators.trees import NIL
from networkx.utils import generate_unique_node


def generate_BP(T, root, pars, root_name, nil_name, with_opening_par):
    """
    It returns a "balanced parenthesis" string representation of the tree T, including the source
    of the nodes (not only the parenthesis).
    :param pars: The style of parentheses can be chosen (a string with two chars, e.g. "()")
    :param root_name: The root node name can be chosen (string with one char).
    :param nil_name: The name for the nodes that are the string terminators in the tree/trie (string with one char)
    :param with_opening_par: You can choose if the BP has the opening parentheses or not (boolean). If you choose False
    the source parameter of the nodes of the Tree will be used instead (must be possible).
    """
    assert (len(pars) == 2)
    assert (len(root_name) == 1)
    assert (len(nil_name) == 1)

    def _generate_BP_node(T, node, pars, nil_name, with_opening_par):
        pref = pars[0] if with_opening_par else ""
        # The NIL node is a terminator of each string in the preffix tree; I do need to include it in the BP representation
        # as it is the only way to distinguish the trie for [N123] and the trie for [N12,N123], for instance.
        if node != NIL:
            s = pref + str(T.nodes[node]['source'])
            for son in T.adj[node]:
                s = s + _generate_BP_node(T, son, pars, nil_name, with_opening_par)
            s = s + pars[1]
        else:
            s = pref + nil_name + pars[1]
        return s

    pref = pars[0] if with_opening_par else ""
    s = pref + root_name
    for son in T.adj[root]:
        s = s + _generate_BP_node(T, son, pars, nil_name, with_opening_par)
    s = s + pars[1]
    return s


def hash_id(id, digest_size=20):
    """
    Takes an id (a string) and returns a blake2b hash with digest_size, encoded as
    a utf-8 urlsafe base64 encoded string
    """
    m = hashlib.blake2b(id.encode(), digest_size=digest_size)
    hash_b64 = base64.urlsafe_b64encode(m.digest())
    return (hash_b64.decode("utf-8"))


def compress_id(id):
    """
    Returns a compression (zlib; as a bytes object) of id (must be a utf-8 string).
    """
    id_bytes = id.encode("utf-8")
    id_comp = zlib.compress(id_bytes)
    return id_comp


def decompress_id_bytes(id_bytes):
    """
    Returns a utf-8 string which is id_bytes (bytes object) decompressed.
    """
    id_decomp = zlib.decompress(id_bytes)
    return id_decomp.decode("utf-8")


def bp_auid_to_preffix_tree(bp_auid, pars, nil_name, with_opening_par):
    # Init the tree with its root and the NIL "pseudo-leaf"
    t = nx.DiGraph()
    r = generate_unique_node()
    t.add_node(r, source=None)
    t.add_node(NIL, source=NIL)
    # And populate with the contents of lbp
    current_node = r
    populate_with_bp_auid(bp_auid, pars, nil_name, with_opening_par, t, r, True)
    return (t, r)


def populate_with_bp_auid(bp_auid, pars, nil_name, with_opening_par, t, current_node, going_down):
    while len(bp_auid) > 0:
        if with_opening_par and bp_auid[0] == pars[0]:
            going_down = True
            node_source, bp_auid = process_node_source(bp_auid[1:], pars, nil_name, '')
            new_node = generate_unique_node()
            t.add_node(new_node, source=node_source)
            t.add_edge(current_node, new_node)
            current_node = new_node
        elif bp_auid[0] == pars[1]:
            if going_down:
                t.add_edge(current_node, NIL)
                going_down = False  # Add NIL only as a leaf
            current_node = next(t.predecessors(current_node))  # The only parent, this is a tree
            bp_auid = bp_auid[1:]
        else:
            going_down = True
            node_source = "" if bp_auid[0] == nil_name else bp_auid[0]
            bp_auid = bp_auid[1:]
            new_node = generate_unique_node()
            t.add_node(new_node, source=node_source)
            t.add_edge(current_node, new_node)
            current_node = new_node


def process_node_source(bp_auid, pars, nil_name, node_source):
    if bp_auid[0] != pars[0] and bp_auid[0] != bp_auid[1]:
        suf = "" if bp_auid[0] == nil_name else bp_auid[0]
        return process_node_source(bp_auid[1:], pars, nil_name, node_source + suf)
    else:
        return (node_source, bp_auid)
    raise ValueError("Parenthesis " + pars + " are not properly balanced in bp_auid")


def preffix_tree_to_ids(T, root):
    ids = []
    for node in T.predecessors(NIL):
        id = ''
        while node != root:
            id = str(T._node[node]['source']) + id
            node = next(T.predecessors(node))
        ids.append(id)
    return sorted(ids)


def cuids_to_bp_auid(cuids, pars="{}", root_name="R", nil_name="$", with_opening_par=False):
    """
    Takes a list of cell unique identifiers (cuids) and returns a tuple with:
    - A string representation of that list of cuids that can be used as an area unique identifier (AUID),
      based on a trie created from the sorted(cuids) and expressed as a balanced parenthesis string with or without the opening parenthesis
    - A blake2b hash of that string.
    - A compressed version of that string (as a bytes object)
    - The trie (networkx object)
    - The root of the trie (networkx object)
    """
    # Sorting the ids is necessary to prevent that for instance ['N21', 'N22'] and ['N22', 'N21'] give
    # different results
    sorted_cuids = sorted(cuids)
    t, r = nx.prefix_tree(sorted_cuids)  # A Prefix_Tree is essentially another name for a trie
    auid = generate_BP(t, r, pars, root_name, nil_name, with_opening_par)
    hashed = hash_id(auid)
    auid_compressed = compress_id(auid)
    return (auid, hashed, auid_compressed, t, r)


def cuids_to_concat_auid(cuids):
    """
    Takes a list of cell unique identifiers (cuids) and returns a tuple with:
    - A string representation of that list of cuids that can be used as an area unique identifier (AUID) based on a concatenation of the sorted(cuids)
    - A blake2b hash of that string.
    - A compressed version of that string (as a bytes object)
    """
    sorted_cuids = sorted(cuids)
    auid = functools.reduce(lambda x, y: x + y, sorted_cuids)  # Just concatenate the ids
    hashed = hash_id(auid)
    auid_compressed = compress_id(auid)
    return (auid, hashed, auid_compressed)


def bp_auid_to_cuids(bp_auid, pars="{}", root_name='R', nil_name='$', with_opening_par=True):
    """
    Takes a string with a bp string auid and returns the list of ids that are encoded
    in that auid.
    """
    # The part with the root name in the bp_auid is irrelevant: it will always be our
    # root node (with source None) in the tree, and it does not change at all the area encoded
    pref_len = 1 if with_opening_par else 0
    t, r = bp_auid_to_preffix_tree(bp_auid[len(root_name) + pref_len:-1], pars, nil_name, with_opening_par)
    return preffix_tree_to_ids(t, r)
